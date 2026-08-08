# Contributing to Xoder

Thanks for helping improve Xoder. Xoder is a customizable Python agent harness
with a complete terminal coding agent as its reference application.
Contributions should keep the reusable core portable, the extension boundaries
explicit, and the included coding workflow reliable.

## Before you start

For a focused fix or small feature:

1. Read the implementation and tests closest to the behavior you want to
   change.
2. Confirm which Xoder layer owns the behavior.
3. Add or update a focused test.
4. Run the relevant checks before opening a pull request.

For a change that introduces a new abstraction, crosses package boundaries,
changes a public extension contract, or alters persisted data, open an issue
first so the design and compatibility boundary can be agreed on.

## Project architecture

Xoder is organized around three layers:

```text
xoder_ai      provider/model streaming layer
xoder_agent   portable agent harness, loop, tools, events, and sessions
xoder_coding  reference coding app, resources, extensions, commands, and TUI
```

The central boundary is:

```text
AgentHarness = reusable agent runtime
AgentSession = coding-agent environment
TUI          = one possible frontend
```

Keep these principles in mind:

- **Small layers beat magic.** Each package should have one clear job.
- **Events are the contract.** The harness emits typed events; applications,
  renderers, and UI layers consume them.
- **The core stays portable.** `xoder_agent` must not depend on the CLI,
  Textual, Rich, application configuration paths, or coding-specific resource
  loading.
- **Provider behavior stays outside the core.** `xoder_agent` owns the
  provider protocol; adapters and provider-specific parsing belong in
  `xoder_ai`.
- **Tools are ordinary typed functions.** Prefer explicit JSON schemas, async
  executors, structured results, and deterministic behavior.
- **Sessions are durable and inspectable.** Avoid changes that make history
  difficult to read, resume, branch, migrate, or export.
- **Documentation follows implementation.** Public claims must describe
  behavior that exists and is tested.

## Where changes belong

| Change | Package |
| --- | --- |
| Provider adapters, streaming parsers, retries, authentication inputs, and normalized model events | `xoder_ai` |
| Agent-loop behavior, messages, tools, queues, typed events, harnesses, and portable session primitives | `xoder_agent` |
| CLI behavior, slash commands, TUI integration, local state paths, resources, provider configuration, coding tools, and persistence | `xoder_coding` |
| User-facing extension examples | `examples/extensions/` |
| Repository and packaged reference documentation | `README.md` and `src/xoder_coding/data/docs/` |

Textual-specific code should remain behind the TUI and extension UI boundaries.
Rich rendering should not leak into `xoder_agent`. If a change crosses layers,
prefer a small typed contract over importing application-specific code into the
portable core.

## Local development

Xoder requires Python 3.12 or newer. Use [uv](https://docs.astral.sh/uv/) so
commands run in the project environment:

```bash
uv sync --dev
uv run xoder --version
uv run xoder
uv run xoder -p "explain this repository"
```

To expose the checkout as a global `xoder` command:

```bash
uv tool install --editable --force .
```

Repeat the editable-tool installation after dependency, package metadata, or
entry-point changes.

## Testing

Start with the smallest test set that proves the behavior:

| Area | Typical tests |
| --- | --- |
| Harness, tools, events, and agent loop | `tests/test_agent_harness.py`, `tests/test_agent_loop.py`, `tests/test_pi_event_protocol.py` |
| Provider streaming and compatibility | `tests/test_xoder_ai.py`, `tests/test_provider_runtime.py` |
| Sessions and persistence | `tests/test_session.py`, `tests/test_session_manager.py`, `tests/test_coding_session.py` |
| Extensions | `tests/test_extensions.py` and the real public examples |
| CLI and commands | `tests/test_cli.py`, `tests/test_commands.py` |
| TUI behavior | `tests/test_tui_*.py` with deterministic fake providers |
| Packaging and public documentation | `tests/test_package_metadata.py`, `tests/test_example_extensions.py` |

Tests that may write settings, credentials, logs, diagnostics, or sessions must
use the same isolated temporary directory for `HOME` and `USERPROFILE`:

```bash
XODER_TEST_HOME="$(mktemp -d)"
HOME="$XODER_TEST_HOME" \
USERPROFILE="$XODER_TEST_HOME" \
uv run pytest
```

Use fake providers and fake tools for automated agent-loop tests. Unit and
integration tests should not require a real model account or API key.

Before submitting a substantial change, keep using the isolated test home and
run:

```bash
HOME="$XODER_TEST_HOME" \
USERPROFILE="$XODER_TEST_HOME" \
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

Run `uv build` and inspect the wheel and source distribution when changing
package metadata, bundled resources, entry points, or release behavior.

## Extending Xoder

### Providers and models

The built-in provider catalog is data, not code. Edit
`src/xoder_coding/data/catalog.toml` when an existing adapter already supports
the provider protocol. Each `[[providers]]` table declares the provider kind,
base URL, models, defaults, context windows, and thinking configuration.

Do not guess model identifiers, limits, modalities, pricing, or protocol
behavior. Verify provider facts against primary documentation and add focused
catalog or adapter tests.

Personal and unreleased provider entries belong in
`~/.xoder/catalog.toml`, not in a source contribution.

### Agent harness

Changes to `xoder_agent` affect every application that embeds the harness.
Keep async boundaries explicit, preserve provider-neutral types, and use fake
providers and tools to demonstrate event ordering, cancellation, queues, tool
execution, and error behavior.

Do not move coding policy, local path conventions, renderer logic, or TUI
dependencies into the harness for convenience.

### Python extensions

Extensions can register tools and commands, subscribe to events, intercept tool
calls and results, add custom messages and renderers, and extend supported TUI
surfaces. Treat `xoder_coding.extensions` as a public application boundary:

- keep examples small and executable through the real extension loader
- add lifecycle and failure-path tests for new hooks
- preserve print-mode behavior when no TUI is attached
- document trust and security implications for executable project extensions
- avoid exposing internal runtime objects when a smaller typed interface works

Start with:

- [`hello_tool.py`](examples/extensions/hello_tool.py)
- [`permission_gate.py`](examples/extensions/permission_gate.py)
- [the extensions guide](src/xoder_coding/data/docs/extensions.md)

### Skills, prompts, and themes

Resource changes should preserve user/project precedence, `.xoder` and
`.agents` interoperability, diagnostics, and `/reload` behavior. Update the
corresponding bundled guide and resource-discovery tests.

## Compatibility and safety

- Preserve the provider-neutral contract in `xoder_agent`.
- Treat JSONL session changes as persisted-data changes; include migration or
  compatibility tests when formats evolve.
- Call out public extension API breaks explicitly.
- Do not read, migrate, or delete a user's `~/.xoder` data as a side effect of
  development or tests.
- Never commit credentials, tokens, logs, sessions, exported conversations, or
  local provider configuration.
- Keep destructive tool behavior explicit and test permission or interception
  paths where relevant.

## Documentation expectations

Update [`README.md`](README.md) when the project's top-level positioning,
installation, primary workflows, or public capabilities change. Detailed
repository-owned references live under:

```text
src/xoder_coding/data/docs/
```

Keep documentation aligned with implemented behavior. Do not add links to
websites, packages, releases, or services that are not publicly available.
When the future Xoder website is introduced, update repository and packaged
references together.

## Release process

The PyPI distribution is `xoder-ai`. Version changes and publication are
explicit maintainer actions, not side effects of ordinary pull requests.

For each release:

1. Keep `pyproject.toml` and the bundled release-note entry aligned.
2. Run the complete test, lint, format, type-check, and build suite.
3. Inspect wheel metadata, entry points, package data, and source-distribution
   contents.
4. Verify installation in an independent Python 3.12 environment.
5. Publish only with explicit maintainer authorization and release
   configuration.

## Pull request guidelines

Good Xoder pull requests are focused and easy to review. Include:

- the motivation for the change
- a summary of behavior and contract changes
- tests and checks you ran
- screenshots or terminal output for relevant TUI or CLI changes
- compatibility, migration, provider, configuration, or security notes
- documentation updates for user-visible behavior

Avoid unrelated refactors and formatting churn. Propose larger design changes
through [GitHub Issues](https://github.com/BANGHlxbackout/Xoder/issues) before
implementation.
