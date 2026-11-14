"""Reproducible, network-free walkthrough of actual citation policy decisions."""
from src.orchestrator.verifier import audit_report


def main():
    print("AlphaQuant / synthetic citation-coverage walkthrough")
    print("No source retrieval, model inference, or trading.\n")
    for label, citations, expected in [
        ("Two URLs, same hostname", [{"url": "https://a.example/one"}, {"url": "https://a.example/two"}], False),
        ("Two distinct hostnames", [{"url": "https://a.example/one"}, {"url": "https://b.example/two"}], True),
        ("Missing citations", [], False),
    ]:
        report = {"market_scan": {"macro": {"facts": ["Synthetic claim"], "citations": citations}}, "trades": []}
        result = audit_report(report)
        assert result["double_source"] is expected
        assert not result["source_content_verified"]
        item = result["citation_coverage"][0]
        print(f"{label}: {'PASS' if result['double_source'] else 'FAIL'}")
        print(f"  distinct hosts: {item['distinct_hosts']}; source content verified: false")
    empty = audit_report({})
    assert not empty["double_source"]
    print("Empty report: FAIL (no claims to check)")
    print("\nPASS means citation coverage only; it does not establish truth.")


if __name__ == "__main__":
    main()
