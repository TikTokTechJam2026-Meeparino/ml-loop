"""One candidate's bounded repair session; the orchestrator executes proposals."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from difflib import unified_diff

from agent.graph.node import RecoveryEvent
from agent.mutation.mutation import CodeMutationEngine
from agent.mutation.prompts import EditFeedback, build_edit_messages
from agent.recovery.prompts import repair_requirement


class RecoveryExhausted(RuntimeError):
    """No further repair proposals are allowed for this candidate."""


@dataclass(frozen=True)
class RepairProposal:
    attempt: int
    files: dict[str, str]
    raw_diff: str


class RecoveryEngine:
    """Create one instance per candidate, optionally restoring completed events.

    Each valid repair request consumes an attempt, even if the model call fails,
    its edits cannot be applied, or it returns NO_CHANGES. A proposed edit must
    receive record_result() before another request. Success closes the session.
    No files, Git state, nodes, or execution jobs are modified here. The caller
    enforces global deadlines, persists events, and supplies redacted diagnostics.
    Token usage remains unknown because CodeMutationEngine returns files only.
    """

    def __init__(self, mutation: CodeMutationEngine | None = None, *, max_attempts: int = 3,
                 history: Sequence[RecoveryEvent] = ()) -> None:
        if type(max_attempts) is not int or max_attempts < 0:
            raise ValueError("max_attempts must be a nonnegative integer")
        events = list(history)
        if len(events) > max_attempts:
            raise ValueError("history exceeds repair allowance")
        for index, event in enumerate(events, 1):
            if (not isinstance(event, RecoveryEvent) or event.attempt != index
                    or type(event.succeeded) is not bool
                    or (event.succeeded and index != len(events))):
                raise ValueError("history must contain consecutive completed repair attempts")
        self.mutation = mutation if mutation is not None else CodeMutationEngine()
        self.max_attempts = max_attempts
        self._events = events
        self._pending: tuple[RepairProposal, str] | None = None

    @property
    def events(self) -> list[RecoveryEvent]:
        return list(self._events)

    @property
    def remaining_attempts(self) -> int:
        if self._events and self._events[-1].succeeded:
            return 0
        return self.max_attempts - len(self._events) - int(self._pending is not None)

    def propose(self, files: Mapping[str, str], *, hypothesis: str, diagnostics: str,
                constraints: str, model: str | None = None,
                max_tokens: int | None = None,
                feedback: EditFeedback | None = None) -> RepairProposal | None:
        """Return repaired files, or None for NO_CHANGES (a failed attempt).

        Provider/edit errors propagate after recording a failed attempt. Invalid
        caller inputs consume no attempt. A proposal is not a successful repair
        until the orchestrator runs it and records the result.
        """
        if self._pending is not None:
            raise RuntimeError("Record the pending repair outcome before proposing another")
        if self.remaining_attempts <= 0:
            raise RecoveryExhausted("Candidate repair allowance is exhausted or repair succeeded")
        requirement = repair_requirement(hypothesis, diagnostics, constraints)
        if not isinstance(files, Mapping):
            raise TypeError("files must be a filename-to-content mapping")
        snapshot = dict(files)
        build_edit_messages(requirement, snapshot)
        attempt = len(self._events) + 1
        try:
            updated = self.mutation.mutate(requirement, snapshot, model=model, max_tokens=max_tokens,
                                           feedback=feedback)
        except Exception:
            self._events.append(RecoveryEvent(attempt, diagnostics, False))
            raise
        if updated == snapshot:
            self._events.append(RecoveryEvent(attempt, diagnostics, False))
            return None
        diff = "".join(
            "".join(line if line.endswith("\n") else line + "\n\\ No newline at end of file\n"
                    for line in unified_diff(snapshot[path].splitlines(keepends=True),
                                 updated[path].splitlines(keepends=True),
                                 fromfile=f"a/{path}", tofile=f"b/{path}"))
            for path in snapshot if snapshot[path] != updated[path]
        )
        proposal = RepairProposal(attempt, updated, diff)
        self._pending = (proposal, diagnostics)
        return proposal

    def record_result(self, *, succeeded: bool) -> RecoveryEvent:
        """Record whether execution AND evaluation of the pending repair succeeded."""
        if type(succeeded) is not bool:
            raise TypeError("succeeded must be a boolean")
        if self._pending is None:
            raise RuntimeError("No pending repair proposal")
        proposal, diagnostics = self._pending
        event = RecoveryEvent(proposal.attempt, diagnostics, succeeded, proposal.raw_diff)
        self._events.append(event)
        self._pending = None
        return event
