# Launch Plan

## Positioning

Short description:

> AgentGuard is a zero-dependency CLI that scans repos for risky AI-agent instructions before you run Codex, Claude Code, Cursor, Copilot, Goose, or other coding agents.

One-line hook:

> Your repo can prompt your coding agent. AgentGuard checks those prompts before they check you.

## First release checklist

- Create the GitHub repository as `agentguard`.
- Add topics: `ai-agents`, `security`, `cli`, `mcp`, `codex`, `claude`, `cursor`, `developer-tools`.
- Publish v0.1.0 with the current CLI, README, tests, and GitHub Actions workflow.
- Add a short demo GIF or terminal recording to the README.
- Open three starter issues: SARIF output, GitHub Action wrapper, and rule allowlists.
- Ask for false positive reports from developers using agent instruction files.

## Launch channels

- Hacker News: "Show HN: AgentGuard - scan repos for risky AI-agent instructions"
- Reddit: r/programming, r/cybersecurity, r/LocalLLaMA, r/ClaudeAI, r/OpenAI
- X/LinkedIn: demo screenshot plus a concrete unsafe `AGENTS.md` example
- GitHub Discussions: ask maintainers which agent config files should be scanned next

## What to build next

1. `--sarif` output so findings can appear in GitHub code scanning.
2. A `uses: owner/agentguard-action@v1` GitHub Action.
3. A curated rules page with examples and remediation guidance.
4. MCP server risk checks for command permissions and remote endpoints.
5. Allowlist comments for intentional findings in trusted internal repos.
