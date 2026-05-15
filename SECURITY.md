# Security Policy

AgentGuard is a local static scanner. It does not send repository contents, file names, findings, or environment values to any remote service.

## Reporting security issues

Please open a private security advisory if this project is hosted on GitHub. If advisories are not enabled yet, open an issue with a minimal description and ask for a private contact path before sharing sensitive details.

## Scope

Useful reports include:

- False negatives for clearly risky agent instructions
- Parser or path traversal bugs
- Unsafe behavior in the CLI
- Supply-chain concerns in packaging or CI

False positives are also welcome as normal issues, especially when they affect common agent setup files.
