# Xoder architecture

Xoder preserves Pi's separation of concerns:

```text
AgentHarness = reusable agent brain
AgentSession = coding-agent environment
TUI = one possible frontend
```

Packages:

- `xoder_ai`: provider/model streaming and provider-neutral events.
- `xoder_agent`: portable harness, loop, tools, messages, events, and sessions.
- `xoder_coding`: CLI application, resources, skills, extensions, commands, persistence, rendering, and TUI integration.

Keep `xoder_agent` independent of Typer, Rich, Textual, application resource locations, and provider-specific assumptions. Prefer typed data models, explicit async boundaries, deterministic fakes, and small abstractions.

Before broad architectural changes in an Xoder checkout, read `CONTRIBUTING.md`, the relevant package implementation, and its tests.
