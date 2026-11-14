import json
import argparse
from src.orchestrator.graph import app


def main():
    parser = argparse.ArgumentParser(description="Run the offline placeholder pipeline; no market data is fetched.")
    parser.add_argument("--summary", action="store_true", help="Show only demo scope and citation coverage.")
    args = parser.parse_args()
    req = {
        "mode": "B",
        "budget": 5000,
        "risk": "High",
        "horizon_months": [3, 12],
        "current_positions": [],
        "preferences": {"avoid": [], "focus": ["AI infra", "semis"]},
    }
    out = app.run(req)
    if args.summary:
        out = {"synthetic": out["meta"]["synthetic"], "execution": out["meta"]["execution"],
               "timestamp_zone": out["meta"]["timestamp_zone"], "audit": out["audit"]}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

