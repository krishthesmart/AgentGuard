# Contributing

Thanks for helping improve AgentGuard.

## Good first contributions

- Add a risky instruction pattern with a test.
- Add a new agent-facing file location to the scanner.
- Improve CLI output without adding dependencies.
- Add sample unsafe fixtures for documentation.

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests
agentguard scan . --fail-on critical
```

Keep changes small and include a test for scanner behavior changes.
