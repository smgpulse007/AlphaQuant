from typing import Dict, Any, List


def _has_double_source(citations: List[dict] | None) -> bool:
    if not citations:
        return False
    urls = {c.get("url") for c in citations if c.get("url")}
    return len(urls) >= 2


def verify(state: Dict[str, Any]) -> Dict[str, Any]:
    output = state.get("output") or {}
    warnings = state.get("meta", {}).get("warnings", [])

    # Validate double-source across market scan sections
    ms = output.get("market_scan", {})
    for section_name, section in ms.items():
        if isinstance(section, dict) and "citations" in section:
            if not _has_double_source(section.get("citations")):
                warnings.append(f"section:{section_name} missing double-source")

    # Validate trades
    for idx, tr in enumerate(output.get("trades", [])):
        if not _has_double_source(tr.get("citations")):
            warnings.append(f"trade:{idx} missing double-source")

    output.setdefault("audit", {})
    output["audit"]["double_source"] = all("missing double-source" not in w for w in warnings)
    output["audit"].setdefault("all_timestamps_pt", True)

    state.setdefault("meta", {})["warnings"] = warnings
    state["output"] = output
    return state

