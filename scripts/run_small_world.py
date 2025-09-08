import json
from src.orchestrator.graph import app


def main():
    req = {
        "mode": "B",
        "budget": 5000,
        "risk": "High",
        "horizon_months": [3, 12],
        "current_positions": [],
        "preferences": {"avoid": [], "focus": ["AI infra", "semis"]},
    }
    out = app.run(req)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

