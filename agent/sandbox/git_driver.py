"""Git-backed lifecycle management for candidate pipeline workspaces."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Mapping, Sequence


def sanitize_branch_name(name: str) -> str:
    """Turn a label into a conservative lowercase ASCII branch name.

    Preserve slash-separated namespaces, replacing punctuation and whitespace
    with hyphens and dropping empty components. Raise ValueError if nothing
    usable remains. This is lossy and does not guarantee uniqueness; callers
    should include a node ID when distinct labels must produce distinct names.
    ``branch_from`` validates names independently and never calls this helper.
    """
    if not isinstance(name, str):
        raise TypeError("Branch name must be text")
    parts = []
    for component in name.lower().split("/"):
        part = re.sub(r"[^a-z0-9_-]+", "-", component)
        part = re.sub(r"-+", "-", part).strip("-")
        if part:
            parts.append(part)
    if not parts:
        raise ValueError("Branch name must contain an ASCII letter, digit, or underscore")
    return "/".join(parts)


class GitDriver:
    """Manage the independent Git repository used by the search loop."""

    def __init__(self, workspace_dir: str | Path = "workspace") -> None:
        self.workspace_dir = Path(workspace_dir).resolve()

    def _git(self, *args: str) -> str:
        # Never let Git walk upward and operate on the outer agent repository.
        if args[0] != "init" and not (self.workspace_dir / ".git").is_dir():
            raise RuntimeError(f"Workspace is not an independent Git repository: {self.workspace_dir}")
        result = subprocess.run(
            ["git", *args],
            cwd=self.workspace_dir,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return result.stdout

    def _commit_sha(self, revision: str) -> str:
        return self._git("rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}").strip()

    def _workspace_file(self, filename: str) -> Path:
        relative = Path(filename)
        if (not filename or not relative.parts or relative.anchor
                or ".." in relative.parts or ":" in filename
                or any(part.lower() == ".git" for part in relative.parts)):
            raise ValueError(f"Expected a workspace-relative path, got {filename!r}")

        destination = (self.workspace_dir / relative).resolve()
        try:
            destination.relative_to(self.workspace_dir)
        except ValueError as exc:
            raise ValueError(f"Path escapes the workspace: {filename!r}") from exc
        if any(part.lower() == ".git" for part in destination.relative_to(self.workspace_dir).parts):
            raise ValueError("Git metadata cannot be accessed as a source file")
        return destination

    def init_workspace(self, template_dir: str | Path) -> str:
        """Create or resume the workspace and return its current commit SHA.

        An existing repository is resumed unchanged. A populated directory without
        Git metadata is rejected so that interrupted or user-created files are not
        silently overwritten.
        """
        git_dir = self.workspace_dir / ".git"
        if git_dir.is_dir():
            return self._commit_sha("HEAD")

        template = Path(template_dir).resolve()
        if not template.is_dir():
            raise FileNotFoundError(f"Template directory does not exist: {template}")
        if template == self.workspace_dir or template in self.workspace_dir.parents:
            raise ValueError("Workspace cannot be inside the template directory")

        sources = [source for source in template.rglob("*")
                   if not any(part.lower() == ".git" for part in source.relative_to(template).parts)]
        if any(source.is_symlink() for source in sources):
            raise ValueError("Template must not contain symbolic links")

        if self.workspace_dir.exists() and any(self.workspace_dir.iterdir()):
            raise RuntimeError(
                f"Workspace exists but is not a Git repository: {self.workspace_dir}"
            )

        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        for source in sources:
            if source.is_file():
                relative = source.relative_to(template)
                destination = self.workspace_dir / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)

        self._git("init")
        # Keep commits usable in clean machines/CI without changing global config.
        self._git("config", "user.name", "ML Loop")
        self._git("config", "user.email", "ml-loop@localhost")
        self._git("add", "-A")
        self._git("commit", "--allow-empty", "-m", "node_00: genesis")
        return self._commit_sha("HEAD")

    def reset_hard(self) -> None:
        """Discard changes to tracked files."""
        self._git("reset", "--hard")

    def clean_untracked(self) -> None:
        """Remove untracked files and directories, preserving ignored artifacts."""
        self._git("clean", "-fd")

    def checkout_commit(self, commit_sha: str) -> None:
        """Check out a commit with a detached HEAD."""
        self._git("checkout", "--detach", self._commit_sha(commit_sha))

    def branch_from(self, parent_commit_sha: str, new_branch_name: str) -> None:
        """Create and check out a branch rooted at an explicit commit."""
        self._git("check-ref-format", "--branch", new_branch_name)
        self._git("checkout", "-b", new_branch_name, self._commit_sha(parent_commit_sha))

    def read_active_files(self, file_list: Sequence[str]) -> dict[str, str]:
        """Read UTF-8 source files from the active workspace."""
        files = {}
        for filename in file_list:
            with self._workspace_file(filename).open(encoding="utf-8", newline="") as stream:
                files[filename] = stream.read()
        return files

    def write_files(self, updated_files: Mapping[str, str]) -> None:
        """Replace each file atomically (the batch is not a filesystem transaction)."""
        pending: list[tuple[Path, Path]] = []
        try:
            for filename, content in updated_files.items():
                if not isinstance(content, str):
                    raise TypeError(f"Content for {filename!r} must be text")
                destination = self._workspace_file(filename)
                destination.parent.mkdir(parents=True, exist_ok=True)
                handle, temporary_name = tempfile.mkstemp(
                    dir=destination.parent, prefix=f".{destination.name}.", suffix=".tmp"
                )
                temporary = Path(temporary_name)
                pending.append((temporary, destination))
                with os.fdopen(handle, "w", encoding="utf-8", newline="") as stream:
                    stream.write(content)

            for temporary, destination in pending:
                os.replace(temporary, destination)
        finally:
            for temporary, _ in pending:
                temporary.unlink(missing_ok=True)

    def commit_node(self, node_id: str, message: str) -> str:
        """Commit all workspace changes and return the resulting commit SHA."""
        self._git("add", "-A")
        subject = f"{node_id}: {message}" if message else node_id
        self._git("commit", "-m", subject)
        return self._commit_sha("HEAD")

    def get_diff(self, parent_sha: str, child_sha: str) -> str:
        """Return the unified diff between two commits."""
        return self._git("diff", "--no-ext-diff", "--no-color",
                         self._commit_sha(parent_sha), self._commit_sha(child_sha), "--")
