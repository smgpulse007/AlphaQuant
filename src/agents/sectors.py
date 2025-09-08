from typing import Dict, Any


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    # TODO: sector RS, breadth, factor tilts
    state.setdefault("analysis", {})["sectors"] = {
        "facts": ["Tech leadership persists (placeholder)"],
        "citations": [
            {"url": "https://www.spglobal.com"},
            {"url": "https://www.ssga.com/us/en/individual/etfs"},
        ],
    }
    return state

