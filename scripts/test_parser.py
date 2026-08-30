"""Offline parser checks: python scripts/test_parser.py."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.mutation.parser import EditError, apply_edits, parse_edits


def block(filename, search, replacement, fence="```", newline="\n"):
    return (
        f"FILE: {filename}{newline}{fence}python{newline}"
        f"<<<<<<< SEARCH{newline}{search}{newline}"
        f"======={newline}{replacement}{newline}>>>>>>> REPLACE{newline}{fence}{newline}"
    )


class ParserTests(unittest.TestCase):
    def test_multiple_files_literal_matching(self):
        files = {"model.py": "x = a[0] + b.*\n", "unchanged.py": "keep", "train.py": "lr=1"}
        output = block("model.py", "a[0] + b.*", "a[1]") + block("train.py", "lr=1", "lr=2")
        updated = apply_edits(files, output)
        self.assertEqual(updated, {"model.py": "x = a[1]\n", "unchanged.py": "keep", "train.py": "lr=2"})
        self.assertEqual(files["model.py"], "x = a[0] + b.*\n")

    def test_sequential_edits(self):
        output = block("a.py", "one", "two") + block("a.py", "two", "three")
        self.assertEqual(apply_edits({"a.py": "one"}, output), {"a.py": "three"})

    def test_failure_leaves_originals_unchanged(self):
        files = {"a.py": "one"}
        with self.assertRaises(EditError):
            apply_edits(files, block("a.py", "one", "two") + block("a.py", "missing", "three"))
        self.assertEqual(files, {"a.py": "one"})

    def test_ambiguous_including_overlapping(self):
        for content, search in [("one one", "one"), ("aaa", "aa")]:
            with self.subTest(content=content), self.assertRaises(EditError):
                apply_edits({"a.py": content}, block("a.py", search, "x"))

    def test_empty_file_and_deletion(self):
        self.assertEqual(apply_edits({"a.py": ""}, block("a.py", "", "x\n")), {"a.py": "x\n"})
        self.assertEqual(apply_edits({"a.py": "x\ny\n"}, block("a.py", "x\n", "")), {"a.py": "y\n"})
        with self.assertRaises(EditError):
            apply_edits({"a.py": "x"}, block("a.py", "", "y"))

    def test_no_changes_copies(self):
        files = {"a.py": "x"}
        result = apply_edits(files, "NO_CHANGES\n")
        self.assertEqual(result, files)
        self.assertIsNot(result, files)

    def test_invalid_output_rejected(self):
        valid = block("a.py", "x", "y")
        for output in ["", "explanation\n" + valid, valid + "trailing prose", valid[:-5],
                       valid.replace("=======", "======"), valid + "FILE: broken.py\n```python\n",
                       valid.replace("<<<<<<< SEARCH", "<<<<<<< SEARCH\n=======")]:
            with self.subTest(output=output), self.assertRaises(EditError):
                parse_edits(output)

    def test_unknown_and_unsafe_filenames(self):
        with self.assertRaises(EditError):
            apply_edits({"a.py": "x"}, block("b.py", "x", "y"))
        for filename in ["../a.py", "/a.py", "C:/a.py", "a/../b.py"]:
            with self.subTest(filename=filename), self.assertRaises(EditError):
                parse_edits(block(filename, "x", "y"))

    def test_long_fences_and_marker_like_code(self):
        source = 'example = "```"\nmarker = "======="'
        edit = parse_edits(block("a.py", source, "pass", fence="````"))[0]
        self.assertEqual(edit.search, source)

    def test_crlf_preserved(self):
        output = block("a.py", "x\r\ny", "a\r\nb", newline="\r\n")
        self.assertEqual(apply_edits({"a.py": "x\r\ny\r\n"}, output), {"a.py": "a\r\nb\r\n"})

    def test_exact_whitespace_and_final_newline(self):
        for suffix in ["", "\n"]:
            self.assertEqual(apply_edits({"a.py": "  x" + suffix}, block("a.py", "  x", "  y")),
                             {"a.py": "  y" + suffix})
        with self.assertRaises(EditError):
            apply_edits({"a.py": "a\r\nb"}, block("a.py", "a\nb", "x"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
