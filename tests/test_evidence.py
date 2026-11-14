import copy
from datetime import datetime, timedelta
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from src.orchestrator.graph import app
from src.orchestrator.verifier import audit_report, verify


def report(urls):
    return {"market_scan": {"macro": {"facts": ["Synthetic claim"],
            "citations": [{"url": url} for url in urls]}}, "trades": []}


class CitationCoverageTests(unittest.TestCase):
    def test_two_hosts_pass_coverage_but_never_verify_truth(self):
        result = audit_report(report(["https://a.example/1", "https://b.example/2"]))
        self.assertTrue(result["double_source"])
        self.assertFalse(result["source_content_verified"])
        self.assertEqual(result["warnings"], [])

    def test_two_paths_on_one_host_do_not_count_twice(self):
        result = audit_report(report(["https://a.example/1", "https://a.example/2"]))
        self.assertFalse(result["double_source"])
        self.assertEqual(result["citation_coverage"][0]["distinct_hosts"], 1)

    def test_host_variants_are_collapsed(self):
        result = audit_report(report(["https://WWW.A.EXAMPLE./1", "http://a.example:8080/2#x"]))
        self.assertFalse(result["double_source"])

    def test_ipv6_variants_are_collapsed(self):
        result = audit_report(report(["http://[::1]/1", "http://[0:0:0:0:0:0:0:1]/2"]))
        self.assertEqual(result["citation_coverage"][0]["distinct_hosts"], 1)

    def test_missing_citation_field_is_not_skipped(self):
        value = report(["https://a.example", "https://b.example"])
        value["market_scan"]["politicians"] = {"highlights": ["Synthetic disclosure"]}
        result = audit_report(value)
        self.assertFalse(result["double_source"])
        self.assertEqual(len(result["citation_coverage"]), 2)
        self.assertIn("section:politicians", result["warnings"][0])

    def test_empty_report_does_not_vacuously_pass(self):
        for value in [{}, {"market_scan": {}, "trades": []}, {"market_scan": {"macro": None}}]:
            with self.subTest(value=value):
                self.assertFalse(audit_report(value)["double_source"])

    def test_invalid_urls_cannot_satisfy_coverage(self):
        for url in ["ftp://b.example", "not a URL", "https://user:fixture@b.example", "https://b.example:bad", "https://bad%20host/", "https://bad host", "https://-bad.example", "https://", "https://[invalid]"]:
            with self.subTest(url=url):
                result = audit_report(report(["https://a.example", url]))
                self.assertFalse(result["double_source"])
                self.assertEqual(result["citation_coverage"][0]["invalid_citations"], 1)

    def test_malformed_citations_are_reported(self):
        for citations in ["https://a.example", [None], [{"url": 7}]]:
            with self.subTest(citations=citations):
                value = report([])
                value["market_scan"]["macro"]["citations"] = citations
                self.assertFalse(audit_report(value)["double_source"])

    def test_event_lists_and_trades_require_coverage(self):
        value = report(["https://a.example", "https://b.example"])
        value["market_scan"]["event_map"] = ["Synthetic event"]
        value["trades"] = [{"ticker": "DEMO"}]
        result = audit_report(value)
        self.assertFalse(result["double_source"])
        self.assertEqual(len(result["warnings"]), 2)

    def test_malformed_shapes_raise_instead_of_passing(self):
        for value in [[], {"trades": {}}, {"trades": [7]}, {"market_scan": []},
                      {"market_scan": {"macro": 7}}, {"market_scan": {"macro": {"facts": "claim"}}},
                      {"market_scan": {"macro": {"analysis": "unsupported claim"}}},
                      {"market_scan": {"macro": {"facts": [""]}}}]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                audit_report(value)

    def test_audit_does_not_mutate_the_input_report(self):
        value = report(["https://a.example", "https://b.example"])
        original = copy.deepcopy(value)
        audit_report(value)
        self.assertEqual(value, original)

    def test_repeated_pipeline_verification_does_not_duplicate_warnings(self):
        state = {"meta": {"warnings": ["upstream fixture warning"]}, "output": report([])}
        verify(state)
        first = copy.deepcopy(state["meta"]["warnings"])
        verify(state)
        self.assertEqual(state["meta"]["warnings"], first)
        self.assertIs(state["meta"], state["output"]["meta"])

    def test_fixture_pipeline_is_explicit_utc_and_network_free(self):
        with patch("socket.socket", side_effect=AssertionError("Network forbidden")):
            output = app.run({"mode": "B"})
        self.assertTrue(output["meta"]["synthetic"])
        self.assertEqual(output["meta"]["execution"], "fixture_pipeline")
        for key in ["started_at", "completed_at"]:
            self.assertEqual(datetime.fromisoformat(output["meta"][key]).utcoffset(), timedelta(0))
        self.assertFalse(output["audit"]["double_source"])
        self.assertFalse(output["audit"]["all_timestamps_pt"])
        self.assertTrue(any("politicians" in warning for warning in output["meta"]["warnings"]))

    def test_cli_exit_status_distinguishes_coverage_and_invalid_input(self):
        with tempfile.TemporaryDirectory(prefix="alpha-evidence-test-") as directory:
            target = Path(directory) / "report.json"
            for contents, expected in [
                (json.dumps(report(["https://a.example", "https://b.example"])), 0),
                (json.dumps(report([])), 1), ("fixture-private-invalid-json", 2),
                ("x" * 1048577, 2),
                ('{"trades": [], "trades": []}', 2),
                ('{"meta": {"value": NaN}}', 2),
                ("[" * 2000 + "0" + "]" * 2000, 2),
            ]:
                target.write_text(contents, encoding="utf-8")
                result = subprocess.run([sys.executable, "-m", "scripts.verify_report", str(target)],
                                        capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, expected, result.stderr)
                self.assertNotIn("fixture-private-invalid-json", result.stdout + result.stderr)
                if expected < 2:
                    self.assertFalse(json.loads(result.stdout)["source_content_verified"])

    def test_documented_module_commands_work(self):
        for module, args in [("scripts.evidence_demo", []), ("scripts.run_small_world", ["--summary"])]:
            result = subprocess.run([sys.executable, "-m", module, *args], capture_output=True,
                                    text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
