from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .scanner import Finding


GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.1-8b-instant"


class GroqError(RuntimeError):
    """Raised when optional Groq explanation generation fails."""


def explain_findings(findings: list[Finding], *, model: str = DEFAULT_MODEL) -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise GroqError("GROQ_API_KEY is not set")
    if not findings:
        return "No findings to explain."

    payload = {
        "model": model,
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You explain static security scanner findings for developers. "
                    "Be concise, practical, and avoid exaggeration."
                ),
            },
            {
                "role": "user",
                "content": build_prompt(findings),
            },
        ],
    }
    request = Request(
        GROQ_CHAT_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=30) as response:
            body = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise GroqError(f"Groq API returned HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise GroqError(f"Could not reach Groq API: {exc.reason}") from exc
    except TimeoutError as exc:
        raise GroqError("Groq API request timed out") from exc

    try:
        return body["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise GroqError("Groq API returned an unexpected response shape") from exc


def build_prompt(findings: list[Finding]) -> str:
    lines = [
        "Explain these AgentGuard findings and suggest safe remediation steps.",
        "Do not ask for secrets, tokens, or environment values.",
        "",
    ]
    for finding in findings[:20]:
        lines.extend(
            [
                f"- {finding.severity.name.lower()} {finding.rule_id}",
                f"  location: {finding.path}:{finding.line}",
                f"  description: {finding.description}",
                f"  matched: {finding.matched}",
            ]
        )
    if len(findings) > 20:
        lines.append(f"- {len(findings) - 20} additional findings omitted")
    return "\n".join(lines)
