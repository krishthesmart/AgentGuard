from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .rules import RULES, Rule, Severity


AGENT_FILE_NAMES = {
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "copilot-instructions.md",
    ".mcp.json",
    "mcp.json",
    "mcp.config.json",
}

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "target",
    ".next",
    ".turbo",
}


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule_id: str
    severity: Severity
    description: str
    matched: str

    def to_json(self) -> dict[str, object]:
        data = asdict(self)
        data["severity"] = self.severity.name.lower()
        return data


def scan_repo(root: Path) -> list[Finding]:
    root = root.resolve()
    if not root.exists():
        raise FileNotFoundError(f"path does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"path is not a directory: {root}")

    findings: list[Finding] = []
    for path in iter_agent_files(root):
        findings.extend(scan_file(root, path))
    return sorted(findings, key=lambda item: (-item.severity, item.path, item.line))


def iter_agent_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if not path.is_file():
            continue
        if is_agent_file(path):
            yield path


def is_agent_file(path: Path) -> bool:
    parts = path.parts
    if path.name in AGENT_FILE_NAMES:
        return True
    if ".cursor" in parts and "rules" in parts:
        return True
    if ".vscode" in parts and path.name == "mcp.json":
        return True
    return False


def scan_file(root: Path, path: Path, rules: Iterable[Rule] = RULES) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")

    findings: list[Finding] = []
    relative = str(path.relative_to(root))
    for line_number, line in enumerate(text.splitlines(), start=1):
        for rule in rules:
            match = rule.pattern.search(line)
            if match:
                findings.append(
                    Finding(
                        path=relative,
                        line=line_number,
                        rule_id=rule.rule_id,
                        severity=rule.severity,
                        description=rule.description,
                        matched=_clean_match(match.group(0)),
                    )
                )
    return findings


def highest_severity(findings: Iterable[Finding]) -> Severity | None:
    highest: Severity | None = None
    for finding in findings:
        if highest is None or finding.severity > highest:
            highest = finding.severity
    return highest


def _clean_match(value: str) -> str:
    return " ".join(value.strip().split())
