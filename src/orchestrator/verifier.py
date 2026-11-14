"""Offline citation-coverage checks; these do not verify source content or truth."""
from typing import Any, Dict
from urllib.parse import urlsplit
import ipaddress
import re


def _citation_hosts(citations: Any) -> tuple[set[str], int]:
    if citations is None:
        return set(), 0
    if not isinstance(citations, list):
        return set(), 1
    hosts: set[str] = set()
    invalid = 0
    for citation in citations:
        url = citation.get("url") if isinstance(citation, dict) else None
        try:
            if not isinstance(url, str) or any(character.isspace() for character in url):
                raise ValueError("Invalid citation URL")
            parsed = urlsplit(url)
            if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
                raise ValueError("Expected an HTTP(S) citation without credentials")
            _ = parsed.port
            host = parsed.hostname.rstrip(".").lower().encode("idna").decode("ascii")
            if host.startswith("www."):
                host = host[4:]
            try:
                host = str(ipaddress.ip_address(host))
            except ValueError:
                labels = host.split(".")
                if len(host) > 253 or any(not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label) for label in labels):
                    raise ValueError("Invalid citation host")
            hosts.add(host)
        except (ValueError, UnicodeError):
            invalid += 1
    return hosts, invalid


def audit_report(report: Dict[str, Any]) -> Dict[str, Any]:
    """Check two distinct citation hostnames for each claim-bearing report item.

    No URLs are fetched. Hostnames are a structural coverage heuristic, not
    proof of independent publishers, corroboration, retrieval, or claim truth.
    """
    if not isinstance(report, dict):
        raise ValueError("Report must be a JSON object.")
    market_scan = report.get("market_scan", {})
    trades = report.get("trades", [])
    if not isinstance(market_scan, dict) or not isinstance(trades, list):
        raise ValueError("market_scan must be an object and trades must be a list.")
    items: list[tuple[str, Any]] = []
    for name, section in market_scan.items():
        if section is None:
            continue
        if isinstance(section, dict):
            if set(section) - {"facts", "highlights", "contradictions", "citations"}:
                raise ValueError("Unsupported claim fields in a report section.")
            for key in ("facts", "highlights", "contradictions"):
                values = section.get(key)
                if values is not None and (not isinstance(values, list) or any(not isinstance(value, str) or not value.strip() for value in values)):
                    raise ValueError("Claim fields must be lists of nonempty strings or null.")
            if any(section.get(key) for key in ("facts", "highlights", "contradictions")):
                items.append((f"section:{name}", section.get("citations")))
        elif isinstance(section, list):
            if section:
                items.append((f"section:{name}", None))
        else:
            raise ValueError("Report sections must be objects, lists, or null.")
    for index, trade in enumerate(trades):
        if not isinstance(trade, dict):
            raise ValueError("Each trade must be an object.")
        items.append((f"trade:{index}", trade.get("citations")))

    coverage = []
    warnings = []
    for item, citations in items:
        hosts, invalid = _citation_hosts(citations)
        passed = len(hosts) >= 2 and invalid == 0
        coverage.append({"item": item, "distinct_hosts": len(hosts),
                         "invalid_citations": invalid, "passed": passed})
        if not passed:
            warnings.append(f"citation coverage: {item} needs two valid distinct hostnames; found {len(hosts)}, invalid {invalid}")
    if not coverage:
        warnings.append("citation coverage: no claim-bearing sections or trades to check")
    return {
        "double_source": bool(coverage) and all(item["passed"] for item in coverage),
        "coverage_policy": "two_distinct_http_hosts_per_claim_item",
        "citation_coverage": coverage,
        "source_content_verified": False,
        "all_timestamps_pt": False,
        "warnings": warnings,
    }


def verify(state: Dict[str, Any]) -> Dict[str, Any]:
    output = state.get("output", {})
    audit = audit_report(output)
    meta = state.setdefault("meta", {})
    prior = [warning for warning in meta.get("warnings", [])
             if not warning.startswith("citation coverage:")]
    meta["warnings"] = prior + audit["warnings"]
    output["audit"] = audit
    output["meta"] = meta
    state["output"] = output
    return state

