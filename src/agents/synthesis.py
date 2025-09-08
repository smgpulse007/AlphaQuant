from typing import Dict, Any
from src.scoring.rubric import score


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    # Combine sections into market_scan and propose trades
    analysis = state.get("analysis", {})
    market_scan = {
        "macro": analysis.get("macro"),
        "cross_asset": analysis.get("cross_asset"),
        "sectors": analysis.get("sectors"),
        "technicals": analysis.get("technicals"),
        "flows": analysis.get("flows"),
        "politicians": analysis.get("politicians"),
        "event_map": [],
    }

    # Dummy scoring input
    s_inputs = {"macro": 0.6, "sector": 0.7, "fund": 0.65, "tech": 0.6, "flow": 0.55, "cat": 0.5, "ai": 0.5, "pol": 0.52}
    scr = score(s_inputs)

    trades = [
        {
            "ticker": "MSFT",
            "direction": "Call",
            "strategy": "Diagonal",
            "expiry": "2026-01-16",
            "strikes": [550, 620],
            "cost": 980,
            "delta": 0.32,
            "pop": round(scr["score"] / 100, 2),
            "confidence": int(scr["score"] * 0.95),
            "thesis": "AI infra leadership; favorable macro regime (placeholder)",
            "key_levels": {"support": 402, "resistance": 435},
            "catalysts": ["10-Q 2025-10-25"],
            "hedge_alt": "Put spread on QQQ",
            "why_now": "Momentum with improving flows (placeholder)",
            "citations": [
                {"url": "https://fred.stlouisfed.org/series/CPIAUCSL"},
                {"url": "https://finance.yahoo.com/quote/MSFT"},
            ],
        }
    ]

    state["output"] = {
        "meta": state.get("meta", {}),
        "regime": {"tag": "Range", "notes": "Stub regime classifier"},
        "market_scan": market_scan,
        "trades": trades,
        "audit": {"double_source": False, "all_timestamps_pt": True},
    }
    return state

