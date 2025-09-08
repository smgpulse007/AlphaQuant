from typing import Dict, Any
from datetime import datetime, timezone


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    # TODO: fetch macro series (FRED/Treasury) and compute curves/breakevens
    now = datetime.now(timezone.utc).astimezone().isoformat()
    state.setdefault("analysis", {})["macro"] = {
        "facts": [f"CPI latest reading placeholder @ {now}"],
        "citations": [
            {"url": "https://fred.stlouisfed.org/series/CPIAUCSL"},
            {"url": "https://www.bls.gov/cpi/"},
        ],
    }
    return state
