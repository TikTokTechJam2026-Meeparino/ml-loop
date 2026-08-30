"""Shared wall-clock budget for one sequential search run."""

import time

from agent.llm.client import LLMClient, LLMError


class BudgetExhausted(LLMError):
    """The search allowance (excluding finalization reserve) is exhausted."""


class RunBudget:
    def __init__(self, started_at: float, total_s: float, reserve_s: float):
        self.deadline = started_at + total_s
        self.reserve_s = reserve_s
        self.monotonic_deadline = time.monotonic() + max(0, self.deadline - time.time())

    def remaining(self, *, final: bool = False) -> float:
        remaining = min(self.deadline - time.time(), self.monotonic_deadline - time.monotonic())
        return max(0.0, remaining - (0 if final else self.reserve_s))

    def allowance(self, limit: float, *, final: bool = False) -> float:
        remaining = min(limit, self.remaining(final=final))
        if remaining <= 0:
            raise BudgetExhausted("Run time budget exhausted")
        return remaining


class BudgetClient:
    """Bind engine calls to the shared deadline without changing engine APIs.

    Real LLMClient requests bound transport timeouts and retry sleeps. Injected
    test/custom clients must enforce their own interruption; their outputs are
    rejected if they return after the deadline. No worker thread is left running.
    """

    def __init__(self, client, budget: RunBudget, max_prompt_chars: int, *, on_request=None, on_response=None, audit=None, profile=None):
        self.client = client
        self._injected_client = client
        self._profiles = {}
        self.profile = profile
        self.budget = budget
        self.max_prompt_chars = max_prompt_chars
        self.last_usage = None
        self.last_elapsed_s = None
        self.on_request = on_request
        self.on_response = on_response
        self.audit = audit

    def _audit(self, event, **data):
        if self.audit is not None:
            try:
                self.audit(event, **data)
            except Exception:
                pass

    def complete(self, messages, *, model=None, max_tokens=None):
        remaining = self.budget.allowance(float("inf"))
        self.last_usage = None
        self.last_elapsed_s = None
        if sum(len(m["content"]) for m in messages) > self.max_prompt_chars:
            raise ValueError("Prompt exceeds configured character budget")
        selected_profile = self.profile() if callable(self.profile) else self.profile
        if self._injected_client is None:
            if selected_profile not in self._profiles:
                self._profiles[selected_profile] = LLMClient.from_env(profile=selected_profile)
            self.client = self._profiles[selected_profile]
        if self.on_request is not None:
            self.on_request()
        remaining = self.budget.allowance(float("inf"))
        kwargs = dict(model=model, max_tokens=max_tokens)
        if isinstance(self.client, LLMClient):
            kwargs["deadline"] = time.monotonic() + remaining
            kwargs["audit"] = self._audit
        started = time.monotonic()
        config = getattr(self.client, 'config', None)
        self._audit('model.request', messages=messages, model=model or getattr(config, 'model', None),
                    profile=selected_profile, reasoning_effort=getattr(config, 'reasoning_effort', None),
                    max_tokens=max_tokens, remaining_s=remaining)
        try:
            response = self.client.complete(messages, **kwargs)
        except Exception as exc:
            self.last_elapsed_s = time.monotonic() - started
            self._audit('model.failed', error=exc, elapsed_s=self.last_elapsed_s)
            raise
        self.last_elapsed_s = time.monotonic() - started
        self._audit('model.response', response=response, elapsed_s=self.last_elapsed_s)
        self.last_usage = response.usage.total_tokens if response.usage is not None else None
        if self.on_response is not None:
            self.on_response(response)
        self.budget.allowance(float("inf"))
        return response
