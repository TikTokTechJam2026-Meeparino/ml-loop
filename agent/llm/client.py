"""Provider-independent, synchronous text generation through LiteLLM.

One client represents one provider credential/endpoint. Override the model per
call within that provider, or construct a new client to change credentials.
No prompts, API keys, or raw provider exceptions are logged by this module.
"""

from __future__ import annotations

import math
import os
import random
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence


class LLMError(RuntimeError):
    """Sanitized request failure safe to include in agent run logs."""


@dataclass(frozen=True)
class LLMConfig:
    model: str
    api_key: str = field(default="", repr=False)
    api_base: str | None = None
    timeout: float = 60.0
    max_retries: int = 2
    max_tokens: int = 1024

    def __post_init__(self) -> None:
        if not self.model.strip() or "<" in self.model:
            raise ValueError("Set LLM_MODEL to a provider/model identifier.")
        if not math.isfinite(self.timeout) or self.timeout <= 0:
            raise ValueError("LLM_TIMEOUT must be finite and positive.")
        if self.max_retries < 0 or self.max_tokens <= 0:
            raise ValueError("Retries must be nonnegative and max tokens positive.")

    @classmethod
    def from_env(cls, env_file: str | Path | None = None) -> LLMConfig:
        """Read root .env without overriding existing process environment values."""
        try:
            from dotenv import load_dotenv
        except ImportError:
            raise LLMError("Install dependencies: python -m pip install -r requirements.txt") from None
        path = Path(env_file) if env_file else Path(__file__).resolve().parents[2] / ".env"
        load_dotenv(path, override=False)
        return cls(
            model=os.getenv("LLM_MODEL", ""),
            api_key=os.getenv("LLM_API_KEY", "").strip(),
            api_base=os.getenv("LLM_API_BASE", "").strip() or None,
            timeout=float(os.getenv("LLM_TIMEOUT", "60")),
            max_retries=int(os.getenv("LLM_MAX_RETRIES", "2")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "1024")),
        )


@dataclass(frozen=True)
class TokenUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


@dataclass(frozen=True)
class LLMResponse:
    text: str
    model: str
    usage: TokenUsage | None
    finish_reason: str | None
    attempts: int


def _completion(**kwargs: Any) -> Any:
    # Lazy import permits injected offline transports without installing SDKs.
    try:
        import litellm
    except ImportError:
        raise LLMError("Install dependencies: python -m pip install -r requirements.txt") from None
    return litellm.completion(**kwargs)


def _get(value: Any, name: str, default: Any = None) -> Any:
    return value.get(name, default) if isinstance(value, Mapping) else getattr(value, name, default)


def _transient(exc: Exception) -> bool:
    status = getattr(exc, "status_code", None)
    return (
        status in (408, 429, 500, 502, 503, 504)
        or isinstance(exc, (TimeoutError, ConnectionError))
        or type(exc).__name__ in {"Timeout", "APITimeoutError", "APIConnectionError"}
    )


class LLMClient:
    """Text-only client with bounded retries and returned-token accounting.

    Totals count provider-reported usage from received responses, not failed
    requests that might nevertheless have been billed. Not thread-safe.
    """

    def __init__(
        self,
        config: LLMConfig,
        *,
        transport: Callable[..., Any] = _completion,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.config = config
        self._transport = transport
        self._sleep = sleep
        self.total_usage = TokenUsage()
        self.responses_without_usage = 0

    @classmethod
    def from_env(cls, env_file: str | Path | None = None) -> LLMClient:
        return cls(LLMConfig.from_env(env_file))

    def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
        model: str | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return self.complete(messages, model=model, max_tokens=max_tokens)

    def complete(
        self,
        messages: Sequence[Mapping[str, str]],
        *,
        model: str | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        selected_model = self.config.model if model is None else model
        limit = self.config.max_tokens if max_tokens is None else max_tokens
        if not selected_model.strip() or "<" in selected_model or limit <= 0:
            raise ValueError("A configured model and positive max_tokens are required.")
        if self.config.api_key == "<YOUR-API-KEY>":
            raise ValueError("Replace LLM_API_KEY in .env before making a live request.")
        if not messages or any(
            m.get("role") not in {"system", "user", "assistant"}
            or not isinstance(m.get("content"), str)
            or not m["content"].strip()
            for m in messages
        ):
            raise ValueError("Provide nonempty text messages with system, user, or assistant roles.")
        kwargs: dict[str, Any] = {
            "model": selected_model,
            "messages": [dict(m) for m in messages],
            "max_tokens": limit,
            "timeout": self.config.timeout,
            "num_retries": 0,  # This wrapper owns the retry budget.
            "stream": False,
        }
        if self.config.api_key:
            kwargs["api_key"] = self.config.api_key
        if self.config.api_base:
            kwargs["api_base"] = self.config.api_base

        for attempt in range(1, self.config.max_retries + 2):
            try:
                raw = self._transport(**kwargs)
                break
            except LLMError:
                raise
            except Exception as exc:
                if not _transient(exc) or attempt > self.config.max_retries:
                    # Never expose provider exception text: it can contain secrets.
                    raise LLMError(
                        f"LLM request failed after {attempt} attempt(s). "
                        "Check credentials, model, endpoint, quota, and connectivity."
                    ) from None
                self._sleep(min(2 ** (attempt - 1), 16) + random.uniform(0, 0.25))

        usage_raw = _get(raw, "usage")
        usage = None
        if usage_raw is not None:
            prompt_tokens = int(_get(usage_raw, "prompt_tokens", 0) or 0)
            completion_tokens = int(_get(usage_raw, "completion_tokens", 0) or 0)
            usage = TokenUsage(
                prompt_tokens,
                completion_tokens,
                int(_get(usage_raw, "total_tokens", prompt_tokens + completion_tokens)
                    or prompt_tokens + completion_tokens),
            )
            self.total_usage = TokenUsage(
                self.total_usage.prompt_tokens + usage.prompt_tokens,
                self.total_usage.completion_tokens + usage.completion_tokens,
                self.total_usage.total_tokens + usage.total_tokens,
            )
        else:
            self.responses_without_usage += 1
        choices = _get(raw, "choices", [])
        if not choices:
            raise LLMError("Provider returned no completion choices.")
        text = _get(_get(choices[0], "message"), "content")
        if not isinstance(text, str) or not text.strip():
            raise LLMError("Provider returned no text; check the token limit or model response type.")
        return LLMResponse(
            text=text,
            model=_get(raw, "model") or selected_model,
            usage=usage,
            finish_reason=_get(choices[0], "finish_reason"),
            attempts=attempt,
        )
