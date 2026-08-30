"""Deterministic queued LLM responses for offline engine and agent tests."""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable, Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass

from agent.llm.client import LLMResponse


@dataclass(frozen=True)
class MockRequest:
    messages: list[dict[str, str]]
    model: str | None
    max_tokens: int | None


class MockLLMClient:
    """Implement complete() without credentials, SDK imports, or network calls.

    Each call consumes one queued string, LLMResponse, or exception. Strings
    become successful text responses with unknown token usage. Explicit
    LLMResponse objects preserve their metadata (including finish reason).
    Exceptions are raised as supplied, without retries. Queue exhaustion raises
    AssertionError so unexpected extra calls cannot silently pass a test.

    Requests are recorded before consuming the queue, including failing calls.
    These in-memory snapshots may contain source code; nothing is logged to disk.
    This mock does not simulate provider behavior, billing, or token accounting.
    """

    def __init__(
        self,
        responses: Iterable[str | LLMResponse | Exception],
        *,
        model: str = "mock/model",
    ) -> None:
        if isinstance(responses, (str, bytes)):
            raise TypeError("Pass a sequence of responses, not a bare string.")
        queued = list(responses)
        if any(not isinstance(item, (str, LLMResponse, Exception)) for item in queued):
            raise TypeError("Responses must be strings, LLMResponse objects, or exceptions.")
        self._responses = deque(queued)
        self.model = model
        self.requests: list[MockRequest] = []

    @property
    def remaining_responses(self) -> int:
        return len(self._responses)

    def complete(
        self,
        messages: Sequence[Mapping[str, str]],
        *,
        model: str | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        self.requests.append(MockRequest(
            messages=deepcopy([dict(message) for message in messages]),
            model=model,
            max_tokens=max_tokens,
        ))
        if not self._responses:
            raise AssertionError("MockLLMClient response queue exhausted.")
        response = self._responses.popleft()
        if isinstance(response, Exception):
            raise response
        if isinstance(response, LLMResponse):
            return response
        return LLMResponse(
            text=response,
            model=self.model if model is None else model,
            usage=None,
            finish_reason="stop",
            attempts=1,
        )
