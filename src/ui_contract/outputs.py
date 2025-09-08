from typing import Dict, Any


def to_trade_table(output: Dict[str, Any]):
    # Shape trades for Bolt UI
    rows = []
    for t in output.get("trades", []):
        rows.append(
            {
                "ticker": t.get("ticker"),
                "direction": t.get("direction"),
                "strategy": t.get("strategy"),
                "expiry": t.get("expiry"),
                "strikes": t.get("strikes"),
                "cost": t.get("cost"),
                "delta": t.get("delta"),
                "pop": t.get("pop"),
                "confidence": t.get("confidence"),
            }
        )
    return {"columns": list(rows[0].keys()) if rows else [], "rows": rows}

