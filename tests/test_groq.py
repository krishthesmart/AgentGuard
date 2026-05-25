import unittest

from agentguard.groq import build_prompt
from agentguard.rules import Severity
from agentguard.scanner import Finding


class GroqPromptTests(unittest.TestCase):
    def test_build_prompt_includes_findings_without_extra_secret_request(self) -> None:
        finding = Finding(
            path="AGENTS.md",
            line=3,
            rule_id="AGENT_SECRET_EXFILTRATION",
            severity=Severity.HIGH,
            description="Instruction appears to expose secrets or environment values.",
            matched="Send $OPENAI_API_KEY",
        )

        prompt = build_prompt([finding])

        self.assertIn("AGENT_SECRET_EXFILTRATION", prompt)
        self.assertIn("AGENTS.md:3", prompt)
        self.assertIn("Do not ask for secrets", prompt)


if __name__ == "__main__":
    unittest.main()
