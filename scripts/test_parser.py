"""Offline parser checks: python scripts/test_parser.py."""

import sys
import re
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

    def test_ambiguous_context_supports_safe_correction(self):
        source = 'if resume:\n    model = FM()\nelse:\n    model = FM()\n'
        files = {'train.py': source}
        with self.assertRaises(EditError) as caught:
            apply_edits(files, block('train.py', '    model = FM()', '    model = FFM()'))
        message = str(caught.exception)
        self.assertIn('Exact occurrence at line 2', message)
        self.assertIn('Exact occurrence at line 4', message)
        self.assertIn('1: if resume:', message)
        self.assertIn('3: else:', message)
        corrected = (block('train.py', 'if resume:\n    model = FM()', 'if resume:\n    model = FFM()')
                     + block('train.py', 'else:\n    model = FM()', 'else:\n    model = FFM()'))
        self.assertEqual(apply_edits(files, corrected)['train.py'], source.replace('FM()', 'FFM()'))
        self.assertEqual(files['train.py'], source)

    def test_missing_match_hint_does_not_apply_fuzzy_edit(self):
        files = {'config.py': 'DEFAULTS = dict(k=16, lr=0.001)\n'}
        with self.assertRaises(EditError) as caught:
            apply_edits(files, block('config.py', 'DEFAULTS = dict(k=16, lr=0.01)', 'wrong'))
        self.assertIn('NOT an exact match', str(caught.exception))
        self.assertIn('lr=0.001', str(caught.exception))
        self.assertNotIn('wrong', files['config.py'])

    def test_hints_use_sequential_source_and_are_bounded(self):
        files = {'a.py': 'first\nsecond\n'}
        output = block('a.py', 'first', 'second') + block('a.py', 'second', 'last')
        with self.assertRaises(EditError) as caught:
            apply_edits(files, output)
        self.assertIn('Exact occurrence at line 1', str(caught.exception))
        self.assertIn('Exact occurrence at line 2', str(caught.exception))
        self.assertEqual(files['a.py'], 'first\nsecond\n')
        with self.assertRaises(EditError) as caught:
            apply_edits({'a.py': ('x' * 1000 + '\n') * 100}, block('a.py', 'x' * 1000, 'y'))
        self.assertLess(len(str(caught.exception)), 6000)
        self.assertIn('Additional exact occurrences omitted', str(caught.exception))

    def test_line_ending_hint_preserves_strictness(self):
        with self.assertRaises(EditError) as caught:
            apply_edits({'a.py': 'x\r\ny'}, block('a.py', 'x\ny', 'z'))
        self.assertIn('Line-ending mismatch', str(caught.exception))

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

    def test_logged_rejections_identify_missing_markers_and_fence(self):
        fixtures = Path(__file__).parent / "fixtures" / "edit_rejections"
        for attempt in (1, 2):
            output = (fixtures / f"attempt_{attempt}.txt").read_text(encoding="utf-8")
            with self.subTest(attempt=attempt), self.assertRaises(EditError) as caught:
                parse_edits(output)
            message = str(caught.exception)
            self.assertIn("Block 1 (model.py)", message)
            self.assertIn("Missing marker lines: <<<<<<< SEARCH", message)
            self.assertIn(">>>>>>> REPLACE", message)
            self.assertIn("Closing code fence reached before all required markers", message)
            expected_found = "found []" if attempt == 1 else "found ['=======']"
            self.assertIn(expected_found, message)

    def test_marker_position_order_and_frame_diagnostics(self):
        valid = block("a.py", "x", "y")
        cases = [
            (valid.replace("<<<<<<< SEARCH", "=======\n<<<<<<< SEARCH"), "duplicated or out of order"),
            (valid.replace("<<<<<<< SEARCH", "extra\n<<<<<<< SEARCH"), "first line"),
            (valid.replace(">>>>>>> REPLACE", ">>>>>>> REPLACE\nextra"), "last"),
            (valid + "FILE: broken.py\n```python\n", "Block 2 (broken.py)"),
            (valid + block("b.py", "x", "y").replace("<<<<<<< SEARCH\n", ""), "Block 2 (b.py)"),
        ]
        for output, message in cases:
            with self.subTest(message=message), self.assertRaisesRegex(EditError, re.escape(message)):
                parse_edits(output)

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
