from datetime import datetime, timezone
from typing import Dict, Any

from src.agents import (
    discovery,
    crawler,
    normalizer,
    entities,
    macro,
    cross_asset,
    sectors,
    technicals,
    flows,
    politicians,
    synthesis,
)
from src.orchestrator.verifier import verify


class AppGraph:
    def __init__(self):
        self.pipeline = [
            ("discover", discovery.run),
            ("crawl", crawler.run),
            ("normalize", normalizer.run),
            ("entities", entities.run),
            ("macro", macro.run),
            ("cross_asset", cross_asset.run),
            ("sectors", sectors.run),
            ("technicals", technicals.run),
            ("flows", flows.run),
            ("politicians", politicians.run),
            ("synthesis", synthesis.run),
            ("verify", verify),
        ]

    def run(self, req: Dict[str, Any]) -> Dict[str, Any]:
        state: Dict[str, Any] = {
            "input": req,
            "meta": {"started_at": datetime.now(timezone.utc).astimezone().isoformat(), "warnings": []},
        }
        for name, fn in self.pipeline:
            state = fn(state)
        state["meta"]["completed_at"] = datetime.now(timezone.utc).astimezone().isoformat()
        # Ensure output meta reflects completed_at
        if isinstance(state.get("output"), dict):
            out = state["output"]
            out.setdefault("meta", {})
            out["meta"]["completed_at"] = state["meta"]["completed_at"]
            return out
        return state


app = AppGraph()
