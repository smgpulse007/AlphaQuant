from typing import Dict, Any


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    # TODO: IVR/IVP, skew, OI shifts, dealer gamma, max pain
    state.setdefault("analysis", {})["flows"] = {
        "facts": ["Options OI up in mega-cap tech (placeholder)"],
        "citations": [
            {"url": "https://www.cboe.com"},
            {"url": "https://www.theocc.com"},
        ],
    }
    return state

