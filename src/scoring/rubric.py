from typing import Dict


def score(inputs: Dict[str, float]) -> Dict[str, float]:
    w = {"macro": 0.15, "sector": 0.12, "fund": 0.22, "tech": 0.18, "flow": 0.12, "cat": 0.12, "ai": 0.07, "pol": 0.02}
    s = sum(inputs.get(k, 0.0) * w[k] for k in w)
    band = "strong" if s >= 0.80 else ("moderate" if s >= 0.60 else "low")
    return {"score": round(s * 100, 1), "band": band}

