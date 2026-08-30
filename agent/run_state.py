"""Generation checkpoints: state, tree and memory publish through one pointer."""

import json
from pathlib import Path
import uuid

from agent.graph.memory import ExplorationMemory
from agent.graph.tree import SearchTree
from agent.reporting import write_report
from agent.sandbox.lease import file_lease


class RunStore:
    def __init__(self, directory):
        self.directory = Path(directory).resolve()

    def lock(self):
        """OS-held lock is released on process death; no stale-lock deletion."""
        return file_lease(self.directory / "run.lock")

    def save(self, state, tree, memory):
        generation = uuid.uuid4().hex
        folder = self.directory / "snapshots" / generation
        folder.mkdir(parents=True)
        if tree is not None:
            tree.save(folder / "tree.json")
        memory.save(folder / "memory.json")
        write_report(state, folder / "state.json")
        write_report({"version": 1, "generation": generation}, self.directory / "current.json")

    def load(self):
        pointer = json.loads((self.directory / "current.json").read_text(encoding="utf-8"))
        generation = pointer["generation"]
        if pointer["version"] != 1 or len(generation) != 32 or any(c not in "0123456789abcdef" for c in generation):
            raise ValueError("Invalid run checkpoint pointer")
        folder = self.directory / "snapshots" / generation
        state = json.loads((folder / "state.json").read_text(encoding="utf-8"))
        if state["version"] != 1:
            raise ValueError("Unsupported run state version")
        tree = SearchTree.load(folder / "tree.json") if (folder / "tree.json").exists() else None
        return state, tree, ExplorationMemory.load(folder / "memory.json")
