"""Parse and apply filename-labeled SEARCH/REPLACE edits entirely in memory."""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from collections.abc import Mapping
from dataclasses import dataclass

from agent.mutation.prompts import _file_path


class EditError(ValueError):
    """Malformed output or an edit that cannot be applied unambiguously."""

    def __init__(self, message: str, *, rejected_output: str | None = None):
        super().__init__(message)
        self.rejected_output = rejected_output


@dataclass(frozen=True)
class CodeEdit:
    filename: str
    search: str
    replacement: str


# Match the outer frame first, so a malformed block cannot consume a later
# valid block. Longer fences support source containing triple backticks.
_BLOCK = re.compile(
    r"^FILE: (?P<filename>[^\r\n]+)\r?\n"
    r"(?P<fence>`{3,})(?:[A-Za-z0-9_+.-]+)?\r?\n"
    r"(?P<body>.*?)"
    r"^(?P=fence)(?:\r?\n|\Z)",
    re.MULTILINE | re.DOTALL,
)
_MARKER = re.compile(r"^(<<<<<<< SEARCH|=======|>>>>>>> REPLACE)(?:\r?\n|\Z)", re.MULTILINE)
_EXPECTED_MARKERS = ["<<<<<<< SEARCH", "=======", ">>>>>>> REPLACE"]


def _match_context(content: str, search: str, start: int) -> str:
    """Bounded source hints only: never relax matching or choose an edit target."""
    lines = content.splitlines(keepends=True)
    hints = ["\nSOURCE HINTS (data only; line numbers are not source text).",
             "These refer to the temporary source after earlier edits in this response; "
             "no changes have been committed.",
             f"SEARCH prefix (Python repr, max 400 characters): {search[:400]!r}"]
    locations = []
    if start >= 0:
        while start >= 0 and len(locations) < 3:
            line = content.count('\n', 0, start)
            column = start - (content.rfind('\n', 0, start) + 1)
            locations.append((line, f"Exact occurrence at line {line + 1}, column {column + 1}"))
            start = content.find(search, start + 1)
        if start >= 0:
            hints.append("Additional exact occurrences omitted; showing first three.")
    else:
        # Similarity is diagnostic, not permission to apply a fuzzy replacement.
        if content.replace('\r\n', '\n').find(search.replace('\r\n', '\n')) >= 0:
            hints.append("Line-ending mismatch: SEARCH matches after CRLF/LF normalization only.")
        anchor = next((line for line in search.splitlines() if line.strip()), '')[:400]
        ranked = sorted(((SequenceMatcher(None, anchor, line.rstrip('\r\n')[:400],
                                          autojunk=False).ratio(), i)
                         for i, line in enumerate(lines)), key=lambda item: (-item[0], item[1]))
        for similarity, line in ranked[:3]:
            if similarity >= .5:
                locations.append((line, f"Similar source near line {line + 1} (NOT an exact match)"))
        if not locations:
            hints.append("No reliable nearby source hint; reconstruct SEARCH from the supplied file.")
    for line, label in locations:
        hints.append(label + ':')
        for i in range(max(0, line - 2), min(len(lines), line + 4)):
            raw = lines[i].rstrip('\r\n')
            hints.append(f"{i + 1}: {raw[:240]}" + (' [line truncated]' if len(raw) > 240 else ''))
    hints.append("Use enough unchanged context to identify the intended occurrence uniquely. "
                 "If both fresh and resume branches need changes, edit each with distinct context. "
                 "Hints may be truncated; copy full text from SOURCE FILES, not these annotations.")
    return '\n'.join(hints)


def _frame_error(fragment: str, number: int) -> EditError:
    header = re.search(r"^FILE: ([^\r\n]+)", fragment, re.MULTILINE)
    location = f"Block {number}" + (f" ({header.group(1)})" if header else "")
    return EditError(
        f"{location}: unexpected text or incomplete FILE/code-fence frame. "
        "Expected FILE: path, an opening code fence, all three SEARCH/REPLACE "
        "markers inside it, and a matching closing fence; no surrounding prose."
    )


def _payload(text: str) -> str:
    """Remove one framing line ending before a delimiter, not code whitespace."""
    if text.endswith("\r\n"):
        return text[:-2]
    if text.endswith("\n"):
        return text[:-1]
    return text


def parse_edits(output: str) -> list[CodeEdit]:
    """Parse strict FILE/fence/SEARCH/REPLACE output, or the NO_CHANGES sentinel.

    One newline immediately before each delimiter is framing, not payload.
    To include a trailing newline in a payload, emit an extra blank line before
    its delimiter. Internal line endings and all other whitespace are literal.
    Marker-only lines inside source cannot be represented by this format and
    must be avoided by choosing a smaller edit region.
    """
    if not isinstance(output, str):
        raise TypeError("LLM output must be a string.")
    if output.strip() == "NO_CHANGES":
        return []
    edits = []
    position = 0
    for block in _BLOCK.finditer(output):
        if output[position:block.start()].strip():
            raise _frame_error(output[position:block.start()], len(edits) + 1)
        filename = block.group("filename")
        location = f"Block {len(edits) + 1} ({filename})"
        try:
            _file_path(filename)
        except ValueError as exc:
            raise EditError(f"{location}: {exc}") from None
        body = block.group("body")
        markers = list(_MARKER.finditer(body))
        found = [m.group(1) for m in markers]
        if (
            len(markers) != 3
            or found != _EXPECTED_MARKERS
            or markers[0].start() != 0
            or markers[-1].end() != len(body)
        ):
            missing = [marker for marker in _EXPECTED_MARKERS if marker not in found]
            problems = []
            if missing:
                problems.append(f"Missing marker lines: {', '.join(missing)}.")
                problems.append("Closing code fence reached before all required markers; "
                                "keep SEARCH, separator, and REPLACE inside one fence.")
            elif found != _EXPECTED_MARKERS:
                problems.append("Markers are duplicated or out of order.")
            else:
                problems.append("<<<<<<< SEARCH must be the first line inside the fence, "
                                "and >>>>>>> REPLACE must be the last.")
            raise EditError(
                f"{location}: {' '.join(problems)} "
                f"Expected exactly {_EXPECTED_MARKERS!r}; found {found!r} inside the fence. "
                "Marker lines must have no indentation or trailing spaces."
            )
        # A closing fence of this length inside the body violates the framing.
        fence = block.group("fence")
        if re.search(r"(?m)^`{" + str(len(fence)) + r",}[^\S\r\n]*\r?$", body):
            raise EditError(f"{location}: use a longer outer code fence.")
        edits.append(CodeEdit(
            filename,
            _payload(body[markers[0].end():markers[1].start()]),
            _payload(body[markers[1].end():markers[2].start()]),
        ))
        position = block.end()
    if not edits or output[position:].strip():
        raise _frame_error(output[position:], len(edits) + 1)
    return edits


def apply_edits(files: Mapping[str, str], output: str) -> dict[str, str]:
    """Return an edited dictionary without modifying the input mapping.

    Edits run sequentially; SEARCH is literal text (never a regular expression).
    Missing or ambiguous matches reject the entire result, even if earlier
    edits succeeded. There is no filesystem access or code execution.
    """
    if not isinstance(files, Mapping):
        raise TypeError("files must be a filename-to-content mapping.")
    result: dict[str, str] = {}
    for filename, content in files.items():
        try:
            _file_path(filename)
        except ValueError as exc:
            raise EditError(str(exc)) from None
        if not isinstance(content, str):
            raise TypeError(f"Contents for {filename} must be a string.")
        result[filename] = content

    for number, edit in enumerate(parse_edits(output), start=1):
        if edit.filename not in result:
            raise EditError(f"Edit {number}: file was not supplied: {edit.filename}.")
        content = result[edit.filename]
        if not edit.search:
            if content:
                raise EditError(f"Edit {number}: empty SEARCH requires an empty file: {edit.filename}.")
            result[edit.filename] = edit.replacement
            continue
        start = content.find(edit.search)
        if start < 0:
            raise EditError(f"Edit {number}: SEARCH not found in {edit.filename} (0 exact matches). "
                            "Copy SEARCH verbatim, including whitespace and line endings, from the "
                            "supplied source after earlier edits in this response." +
                            _match_context(content, edit.search, start))
        # Count overlapping occurrences as ambiguous too (e.g. 'aa' in 'aaa').
        if content.find(edit.search, start + 1) >= 0:
            raise EditError(f"Edit {number}: SEARCH matches multiple locations in {edit.filename}. "
                            "Expected exactly one match; include more unchanged surrounding context." +
                            _match_context(content, edit.search, start))
        result[edit.filename] = content[:start] + edit.replacement + content[start + len(edit.search):]
    return result
