from typing import Any, Dict


class State(dict):
    """Simple state carrier for the orchestrator graph."""

    def get_section(self, name: str) -> Dict[str, Any]:
        return self.setdefault(name, {})

