from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .scanner import Finding, scan_repo
from .rules import Severity


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentguard",
        description="Scan repositories for risky AI-agent instructions and config patterns.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="scan a repository")
    scan.add_argument("path", nargs="?", default=".", help="repository path to scan")
    scan.add_argument("--json", action="store_true", help="print JSON output")
    scan.add_argument(
        "--fail-on",
        choices=["low", "medium", "med", "high", "critical"],
        default="high",
        help="exit 1 when findings at this severity or higher are present",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":
        return run_scan(args.path, json_output=args.json, fail_on=args.fail_on)

    parser.error(f"unknown command: {args.command}")
    return 2


def run_scan(path: str, *, json_output: bool, fail_on: str) -> int:
    try:
        findings = scan_repo(Path(path))
        threshold = Severity.parse(fail_on)
    except Exception as exc:
        print(f"agentguard: {exc}", file=sys.stderr)
        return 2

    if json_output:
        print(json.dumps([finding.to_json() for finding in findings], indent=2))
    else:
        print_human(findings)

    if any(finding.severity >= threshold for finding in findings):
        return 1
    return 0


def print_human(findings: list[Finding]) -> None:
    if not findings:
        print("No risky agent instructions found.")
        return

    for index, finding in enumerate(findings):
        if index:
            print()
        print(f"{finding.severity.label():<5} {finding.rule_id}  {finding.path}:{finding.line}")
        print(f"      {finding.description}")
        print(f"      matched: {finding.matched}")
