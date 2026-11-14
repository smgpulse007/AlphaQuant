"""Validate citation coverage without fetching URLs or executing agents."""
import argparse
import json
from pathlib import Path
import sys

from src.orchestrator.verifier import audit_report


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key.")
        result[key] = value
    return result


def invalid_constant(_value):
    raise ValueError("Non-finite JSON number.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="JSON report, at most 1 MiB")
    args = parser.parse_args(argv)
    try:
        with args.report.open("rb") as stream:
            data = stream.read(1048577)
        if len(data) > 1048576:
            raise ValueError("Report exceeds 1 MiB.")
        report = json.loads(data, object_pairs_hook=unique_object, parse_constant=invalid_constant)
        audit = audit_report(report)
    except (OSError, ValueError, UnicodeError, RecursionError):
        print(json.dumps({"error": "Unreadable, oversized, or invalid report JSON/shape."}), file=sys.stderr)
        return 2
    print(json.dumps(audit, indent=2))
    return 0 if audit["double_source"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
