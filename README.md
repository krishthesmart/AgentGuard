# AgentGuard

AgentGuard is a small CLI that scans a repository for risky AI-agent instructions and config patterns before you hand the repo to Codex, Claude Code, Cursor, Copilot, Goose, or another coding agent.

It looks for files agents commonly read, including `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, `.github/copilot-instructions.md`, and MCP config files. The scanner flags patterns such as secret exfiltration, hidden instruction overrides, unsafe shell bootstraps, and guidance that tells agents to skip tests or ignore security checks.

## Why this exists

AI coding agents are becoming part of normal development workflows. That also means repositories can contain instructions that influence agent behavior. Some are harmless project notes. Some are stale. Some are unsafe.

AgentGuard gives maintainers a fast, local preflight check:

```bash
agentguard scan .
```

No network calls. No API keys. No telemetry.

## Install

From a local checkout:

```bash
python -m pip install -e .
```

Then run:

```bash
agentguard scan /path/to/repo
```

You can also run without installing:

```bash
python -m agentguard scan .
```

## Example

```text
HIGH  AGENT_SECRET_EXFILTRATION  AGENTS.md:12
      Instruction appears to expose secrets or environment values.
      matched: send $OPENAI_API_KEY to

MED   AGENT_SKIP_VALIDATION  CLAUDE.md:7
      Instruction asks the agent to bypass tests, review, or security checks.
      matched: skip tests
```

## CLI

```bash
agentguard scan [PATH] [--json] [--fail-on low|medium|high|critical]
```

Examples:

```bash
agentguard scan .
agentguard scan . --json
agentguard scan . --fail-on high
```

Exit codes:

- `0`: no findings at or above the configured failure threshold
- `1`: findings met the failure threshold
- `2`: CLI usage or scan error

## What it scans

AgentGuard checks likely agent-facing files:

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `.cursor/rules/**`
- `.github/copilot-instructions.md`
- `.mcp.json`
- `mcp.json`
- `mcp.config.json`
- `.vscode/mcp.json`

It skips common dependency and build directories such as `.git`, `node_modules`, `dist`, `build`, `.venv`, and `target`.

## Roadmap

- GitHub Action for pull request checks
- SARIF output for code scanning alerts
- Rule allowlists for trusted internal repos
- MCP server risk classification
- Inline remediation suggestions

## Contributing

Issues and pull requests are welcome. Good contributions are small, reproducible, and include a test case when they change scanner behavior.

## License

MIT
