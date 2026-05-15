from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
import re


class Severity(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

    @classmethod
    def parse(cls, value: str) -> "Severity":
        normalized = value.strip().upper()
        if normalized == "MED":
            normalized = "MEDIUM"
        return cls[normalized]

    def label(self) -> str:
        if self is Severity.MEDIUM:
            return "MED"
        return self.name


@dataclass(frozen=True)
class Rule:
    rule_id: str
    severity: Severity
    description: str
    pattern: re.Pattern[str]


RULES: tuple[Rule, ...] = (
    Rule(
        "AGENT_SECRET_EXFILTRATION",
        Severity.HIGH,
        "Instruction appears to expose secrets or environment values.",
        re.compile(
            r"(send|post|upload|exfiltrate|share|paste).{0,80}"
            r"(\$[A-Z0-9_]*(KEY|TOKEN|SECRET|PASSWORD)|"
            r"env(?:ironment)? variables?|\.env|credentials?)",
            re.IGNORECASE,
        ),
    ),
    Rule(
        "AGENT_IGNORE_HIGHER_PRIORITY",
        Severity.HIGH,
        "Instruction tries to override system, developer, or security instructions.",
        re.compile(
            r"(ignore|bypass|override|disregard).{0,60}"
            r"(system|developer|security|safety|policy|previous|higher.priority)",
            re.IGNORECASE,
        ),
    ),
    Rule(
        "AGENT_SKIP_VALIDATION",
        Severity.MEDIUM,
        "Instruction asks the agent to bypass tests, review, or security checks.",
        re.compile(
            r"(skip|do not run|don't run|avoid|disable).{0,50}"
            r"(tests?|lint|type.?check|review|security|validation)",
            re.IGNORECASE,
        ),
    ),
    Rule(
        "AGENT_UNSAFE_BOOTSTRAP",
        Severity.MEDIUM,
        "Instruction contains a shell bootstrap pattern that deserves review.",
        re.compile(
            r"(curl|wget).{0,120}(\|\s*(sh|bash)|bash\s*-c|sh\s*-c)",
            re.IGNORECASE,
        ),
    ),
    Rule(
        "AGENT_HIDDEN_INSTRUCTION",
        Severity.LOW,
        "Instruction uses wording commonly associated with prompt injection.",
        re.compile(
            r"(hidden instruction|secret instruction|do not reveal|"
            r"never mention this instruction|silently)",
            re.IGNORECASE,
        ),
    ),
    Rule(
        "MCP_REMOTE_SERVER",
        Severity.LOW,
        "MCP config references a remote server; verify trust and permissions.",
        re.compile(r'"url"\s*:\s*"https?://', re.IGNORECASE),
    ),
)
