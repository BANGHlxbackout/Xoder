# Contributing to Xoder

Thanks for helping improve Xoder. The project is both a usable terminal coding
agent and a readable example of how coding agents are built. Contributions
should improve the tool while preserving its small, explicit architecture.

## Project architecture

Xoder is organized around three layers:

```text
xoder_ai      provider/model streaming layer
xoder_agent   portable agent harness, loop, tools, events, sessions
xoder_coding  CLI app, resources, skills, extensions, commands, TUI integration
```

The key boundary is:

```text
AgentHarness = reusable agent brain
AgentSession = coding-agent environment
TUI = one possible frontend
```

Please keep these principles in mind:

- **Small layers beat magic.** Each package should have one clear job.
- **Events are the contract.** The harness emits typed events; UI and renderers
  consume them.
- **The core stays portable.** `xoder_agent` should not depend on the CLI,
  Textual, Rich, local configuration paths, or application resource loading.
- **Tools are ordinary typed functions.** Prefer explicit schemas and structured
  results.
- **Sessions are durable and inspectable.** Avoid changes that make history hard
  to read, resume, or export.
- **Documentation follows implementation.** Update the repository and bundled
  reference documents when user-facing behavior changes.

## Local development

Use `uv` so Python commands run in the project environment:

```bash
uv sync --dev
uv run xoder --version
uv run xoder
uv run xoder -p "explain this repo"
```

To expose the checkout as a global `xoder` command:

```bash
uv tool install --editable --force .
```

Repeat that command after changes to package metadata, dependencies, or entry
points.

## Checks before submitting

Run relevant focused tests while developing, then run the complete checks when
practical:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

Tests that may write runtime settings or diagnostics must use the same isolated
temporary directory for `HOME` and `USERPROFILE`.

## Where changes belong

- Provider integrations, model adapters, and provider-neutral streaming belong
  in `xoder_ai`.
- Agent-loop behavior, tool abstractions, events, messages, harnesses, and
  portable session primitives belong in `xoder_agent`.
- CLI behavior, slash commands, TUI integration, local configuration,
  resources, skills, prompt templates, and coding tools belong in
  `xoder_coding`.
- Textual-specific code should stay behind the TUI layer.
- Rich rendering should not leak into the reusable harness.

If a change crosses layers, prefer a small typed boundary over importing
application-specific details into core code.

## Adding a provider or model

The built-in provider catalog is data, not code. Edit
`src/xoder_coding/data/catalog.toml`; each `[[providers]]` table declares the
provider kind, base URL, models, defaults, context windows, and thinking
configuration.

For personal or unreleased providers, create `~/.xoder/catalog.toml` with the
same schema. It is overlaid on the built-in catalog and does not require a code
change.

## Testing expectations

- Add or update tests for behavior changes.
- Use fake providers and fake tools for deterministic agent-loop tests.
- Keep core tests free of provider-specific assumptions.
- Add focused regression tests for bugs.
- Test public examples through the real extension loader when possible.

## Documentation expectations

Update `README.md` for top-level user guidance. More detailed repository-owned
references live under:

```text
src/xoder_coding/data/docs/
```

Keep public documentation aligned with implemented behavior and avoid linking to
services or releases that do not exist.

## Release preparation

The intended distribution name is `xoder-ai`, but it is not yet published to
PyPI. Version changes and publication are explicit maintainer actions, not side
effects of ordinary commits.

When preparing a future release, keep the version in `pyproject.toml` aligned
with the bundled Xoder release-note entry, run the full test and build suite,
inspect wheel metadata and contents, and verify an independent installation.
Publishing requires separate maintainer authorization and release configuration.

## Pull request guidelines

Good Xoder pull requests are small, focused, and easy to review. Include:

- the motivation for the change
- a summary of behavior changes
- tests or checks you ran
- screenshots or terminal output for TUI/CLI changes when useful
- notes about compatibility, migrations, configuration, or provider behavior

Avoid unrelated refactors. For a larger design change, open an issue first at
<https://github.com/BANGHlxbackout/Xoder/issues>.
