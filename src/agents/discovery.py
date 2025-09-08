from typing import Dict, Any


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    # TODO: enumerate sources: APIs, RSS, site adapters based on input mode
    state["sources"] = {
        "macro": ["FRED:CPIAUCSL"],
        "politicians": ["SenateClerk:latest"],
    }
    return state

