"""Offline Git integration checks: python scripts/test_git_driver.py."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.sandbox.git_driver import GitDriver


class GitDriverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.template = self.root / "template"
        self.template.mkdir()
        for name in ("baseline.py", "evaluate.py", "submit.py", "model.py"):
            (self.template / name).write_bytes(b"value = 1\n")
        self.driver = GitDriver(self.root / "workspace")
        self.genesis = self.driver.init_workspace(self.template)
        self.git("config", "core.autocrlf", "false")

    def git(self, *args):
        return subprocess.check_output(
            ["git", *args], cwd=self.driver.workspace_dir, text=True, encoding="utf-8"
        ).strip()

    def test_branch_lifecycle_and_diff(self):
        self.assertEqual(self.git("log", "-1", "--format=%s"), "node_00: genesis")
        self.driver.branch_from(self.genesis, "candidate-a")
        self.driver.write_files({"model.py": "value = 2\n", "features.py": "# café\n"})
        child = self.driver.commit_node("node_01", "change model")
        self.assertEqual(self.git("rev-parse", "HEAD^"), self.genesis)
        diff = self.driver.get_diff(self.genesis, child)
        self.assertIn("-value = 1", diff)
        self.assertIn("+value = 2", diff)
        self.assertTrue(diff.endswith("\n"))
        self.driver.checkout_commit(self.genesis)
        self.assertEqual(self.git("rev-parse", "--abbrev-ref", "HEAD"), "HEAD")
        self.driver.branch_from(self.genesis, "candidate-b")
        self.assertEqual(self.driver.read_active_files(["model.py"]), {"model.py": "value = 1\n"})
        self.assertFalse((self.driver.workspace_dir / "features.py").exists())

    def test_reset_and_clean(self):
        self.driver.write_files({"model.py": "broken", "scratch/temp.py": "junk"})
        self.driver.reset_hard()
        self.driver.clean_untracked()
        self.assertEqual(self.driver.read_active_files(["model.py"])["model.py"], "value = 1\n")
        self.assertFalse((self.driver.workspace_dir / "scratch").exists())
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_resume_does_not_overwrite_dirty_files(self):
        self.driver.write_files({"model.py": "keep this"})
        (self.template / "model.py").write_text("new template")
        self.assertEqual(self.driver.init_workspace(self.template), self.genesis)
        self.assertEqual(self.driver.read_active_files(["model.py"])["model.py"], "keep this")

    def test_invalid_batch_keeps_existing_files(self):
        for bad in ("../outside.py", ".git/config", "C:/outside.py", "."):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.driver.write_files({"model.py": "changed", bad: "bad"})
            self.assertEqual(self.driver.read_active_files(["model.py"])["model.py"], "value = 1\n")
        self.assertEqual(list(self.driver.workspace_dir.glob("*.tmp")), [])

    def test_exact_source_round_trip(self):
        source = "# café\r\nvalue = 2\r\n"
        self.driver.write_files({"model.py": source})
        self.assertEqual(self.driver.read_active_files(["model.py"])["model.py"], source)

    def test_uninitialized_nested_workspace_cannot_touch_parent(self):
        nested = self.driver.workspace_dir / "nested"
        nested.mkdir()
        driver = GitDriver(nested)
        with self.assertRaises(RuntimeError):
            driver.reset_hard()
        (nested / "keep.txt").write_text("keep")
        with self.assertRaises(RuntimeError):
            driver.init_workspace(self.template)
        self.assertEqual((nested / "keep.txt").read_text(), "keep")

    def test_git_errors_propagate(self):
        with self.assertRaises(subprocess.CalledProcessError):
            self.driver.checkout_commit("nonexistent-revision")
        self.assertEqual(self.git("rev-parse", "HEAD"), self.genesis)


if __name__ == "__main__":
    unittest.main(verbosity=2)
