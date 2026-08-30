"""Choose one requirement for CodeMutationEngine without editing code."""

import json
import re
from collections.abc import Mapping, Sequence

from agent.graph.node import SearchNode
from agent.improvement.prompts import build_messages
from agent.llm.client import LLMClient
from agent.mutation.mutation import CompletionClient


class ProposalError(ValueError):
    """The model did not return a complete, usable proposal."""


class ImprovementEngine:
    """Select a change; the caller owns parent selection, mutation and execution.

    Supply the selected node's complete editable source snapshot and the result
    of tree.get_lineage_chain(node_id). Source/commit correspondence, context
    size, redaction, and runtime budget enforcement belong to the caller.
    Context optionally supplies configuration, sibling attempts and memory.
    Share an injected client with mutation to accumulate usage across both.
    No files are read/written, and no mutation or automatic repair is performed.
    """

    def __init__(self, client: CompletionClient | None = None) -> None:
        self.client = client

    def propose(self, files: Mapping[str, str], lineage: Sequence[SearchNode], *,
                objective: str, constraints: str, context: str = "",
                model: str | None = None, max_tokens: int | None = None) -> str:
        """Return a requirement directly usable by mutation.mutate(requirement, files).

        Preserve caller constraints in the returned requirement independently of
        model output. Prompt rules are not a substitute for executor validation.
        Invalid inputs fail before client initialization; provider errors propagate.
        """
        messages = build_messages(files, lineage, objective=objective,
                                  constraints=constraints, context=context)
        if self.client is None:
            self.client = LLMClient.from_env(profile="high")
        response = self.client.complete(messages, model=model, max_tokens=max_tokens)
        if response.finish_reason in {"length", "max_tokens", "content_filter"}:
            raise ProposalError("Proposal was truncated or filtered")
        # Providers may wrap an otherwise valid object despite the prompt. Only
        # unwrap one complete JSON fence; do not recover partial/arbitrary text.
        payload = response.text.strip()
        fenced = re.fullmatch(r"```(?:json)?\s*\n(.*?)\n```", payload, flags=re.DOTALL)
        if fenced is not None:
            payload = fenced.group(1)
        try:
            proposal = json.loads(payload)
        except (ValueError, TypeError) as exc:
            raise ProposalError("Expected a JSON requirement object") from exc
        if (not isinstance(proposal, dict) or set(proposal) != {"requirement"}
                or not isinstance(proposal["requirement"], str)
                or not proposal["requirement"].strip()):
            raise ProposalError("Expected exactly one nonempty requirement string")
        return (f"SELECTED CHANGE\n{proposal['requirement'].strip()}\n\n"
                f"OBJECTIVE\n{objective}\n\nCONSTRAINTS\n{constraints}")
