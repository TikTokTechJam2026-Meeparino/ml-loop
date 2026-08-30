"""Request and apply one code mutation to an in-memory source snapshot."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol

from agent.mutation.parser import EditError, apply_edits
from agent.mutation.prompts import build_edit_messages
from agent.llm.client import LLMClient, LLMResponse


class CompletionClient(Protocol):
    """Minimal interface implemented by LLMClient and offline test doubles."""

    def complete(
        self,
        messages: Sequence[Mapping[str, str]],
        *,
        model: str | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse: ...


class CodeMutationEngine:
    """Compose prompt construction, LLM completion, and exact edit application.

    Without an injected client, load LLMClient from .env on the first valid
    mutation request. Reuse that client so token accounting spans requests.
    Source files are never read, written, or executed here. Provider errors and
    parser EditError exceptions propagate to the caller; no automatic code
    repair requests are made. Transport retries remain the client's concern.
    """

    def __init__(self, client: CompletionClient | None = None) -> None:
        self.client = client

    def mutate(
        self,
        requirement: str,
        files: Mapping[str, str],
        *,
        model: str | None = None,
        max_tokens: int | None = None,
    ) -> dict[str, str]:
        """Return complete updated file contents, including unchanged files.

        Validate inputs before calling the LLM. Apply its edits to the same
        snapshot used in the prompt, leaving the caller's mapping untouched on
        both success and failure. NO_CHANGES returns an unchanged copy.
        """
        if not isinstance(files, Mapping):
            raise TypeError("files must be a filename-to-content mapping.")
        snapshot = dict(files)
        messages = build_edit_messages(requirement, snapshot)
        if self.client is None:
            self.client = LLMClient.from_env()
        response = self.client.complete(messages, model=model, max_tokens=max_tokens)
        # A token-limited output may end after one valid block while omitting
        # other required edits. Do not mistake that partial response for success.
        if response.finish_reason in {"length", "max_tokens", "content_filter"}:
            raise EditError("LLM output was truncated or filtered; no edits were applied.")
        return apply_edits(snapshot, response.text)
