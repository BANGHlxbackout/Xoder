# Xoder

A small, readable terminal coding agent and a working example of how coding
agents are built.

Xoder can read files, edit code, run commands, call model providers, and keep a
durable session history while streaming its work. The codebase is also designed
to be read: each layer has a focused responsibility and communicates through
typed events.

## Architecture

```text
xoder_coding  →  xoder_agent  →  xoder_ai
```

- `xoder_ai` translates model-provider streams into provider-neutral events.
- `xoder_agent` owns the portable agent brain: messages, tools, events, loop,
  harness, and session primitives.
- `xoder_coding` turns the harness into a coding application with a CLI, TUI,
  file and shell tools, provider configuration, skills, extensions, and
  persistent sessions.

The key boundary is:

```text
AgentHarness = reusable brain
AgentSession = coding-agent environment
TUI = one possible frontend
```

The reusable harness does not depend on Textual, Rich, local configuration
paths, slash commands, or rendering. Frontends consume its event stream.

## Install from source

The intended Python distribution name is `xoder-ai`, but it is not yet
published to PyPI. Install the current project from source:

```bash
git clone https://github.com/BANGHlxbackout/Xoder.git
cd Xoder
uv sync --dev
uv run xoder --version
```

If `uv` is not installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

To expose the checkout-backed `xoder` command globally, install it as an
editable tool:

```bash
uv tool install --editable --force .
```

Run that command again after pulling changes that affect package metadata,
dependencies, or entry points. Source edits themselves are visible immediately
through the editable install.

## Quickstart

From the source checkout, start Xoder in the project it should work on:

```bash
uv run xoder --cwd /path/to/project
```

If you installed the editable tool, run:

```bash
cd /path/to/project
xoder
```

Type a request and press **Enter**:

```text
explain what this project does
```

One-shot print mode is useful for scripts and quick prompts:

```bash
uv run xoder -p "summarize the architecture"
uv run xoder --cwd /path/to/project -p "find the CLI entry point"
```

Xoder needs a model provider. Start the TUI, then use `/login` and `/model`:

```text
/login
/model
```

It supports built-in providers and custom OpenAI-compatible endpoints, including
local models. Provider and model definitions live in
[`src/xoder_coding/data/catalog.toml`](src/xoder_coding/data/catalog.toml).
Personal overrides can be placed in `~/.xoder/catalog.toml`.

## Capabilities

- Interactive Textual TUI and non-interactive print mode.
- Built-in `read`, `write`, `edit`, and `bash` tools.
- Durable JSONL sessions under `~/.xoder/sessions/`, with resume and branching.
- Slash commands for login, model selection, sessions, compaction, export,
  themes, and more.
- Project instructions and resources from `AGENTS.md`, `.xoder/`, and
  `.agents/`.
- User skills, prompt templates, extensions, and custom TUI themes.
- Provider-neutral event rendering for Rich, plain text, JSON, transcripts, and
  custom frontends.

## Use Xoder as a library

```python
from xoder_agent import AgentHarness, AgentHarnessConfig

harness = AgentHarness(
    AgentHarnessConfig(
        provider=provider,
        model="my-model",
        system="You are a helpful coding agent.",
        tools=tools,
    )
)

async for event in harness.prompt("Explain this package"):
    print(event)
```

Because the harness emits events instead of rendering UI directly, the same
core can drive the built-in TUI, print mode, or another frontend.

## Documentation

Until a dedicated documentation site exists, use the repository and bundled
reference documents:

- [Documentation index](src/xoder_coding/data/docs/README.md)
- [Architecture](src/xoder_coding/data/docs/architecture.md)
- [CLI](src/xoder_coding/data/docs/cli.md)
- [Extensions](src/xoder_coding/data/docs/extensions.md)
- [Models and providers](src/xoder_coding/data/docs/models.md)
- [Skills](src/xoder_coding/data/docs/skills.md)
- [TUI](src/xoder_coding/data/docs/tui.md)

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for architecture boundaries, testing
expectations, and pull request guidance.

```bash
uv sync --dev
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

Run Xoder from the checkout:

```bash
uv run xoder
uv run xoder -p "explain this repo"
```

Report bugs and request changes through
[GitHub Issues](https://github.com/BANGHlxbackout/Xoder/issues).

## License

Xoder is distributed under the [MIT License](LICENSE).
