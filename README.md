# Xoder

<p align="center">
  <strong>A customizable Python agent harness—with a complete terminal coding agent included.</strong>
</p>

<p align="center">
  English
  · <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="#quickstart">Quickstart</a>
  ·
  <a href="#make-xoder-yours">Customize</a>
  ·
  <a href="#architecture">Architecture</a>
  ·
  <a href="#build-with-the-harness">Library</a>
</p>

Xoder provides reusable primitives for building tool-using agents around your
own models, tools, workflows, and interfaces. It also ships with a complete
terminal coding agent that exercises those primitives in a real application:
an interactive TUI, file and shell tools, persistent sessions, model
configuration, skills, extensions, prompts, and themes.

Use Xoder as a terminal agent, adapt the included coding workflow, or embed the
portable `xoder_agent` harness in an application of your own.

> **Project status:** Xoder `0.0.0` is an early release and requires Python 3.12
> or newer. Public APIs and workflows may change as the project develops.

## What is Xoder?

Xoder is inspired by
[Pi's minimalist and extensible agent-harness architecture](https://github.com/earendil-works/pi).
It brings the same separation between model providers, a portable agent
runtime, and a complete coding application to a typed Python codebase.

Xoder is deliberately two things:

| Use Xoder as | What you get |
| --- | --- |
| A reusable agent harness | A provider-neutral agent loop, typed messages and events, tool execution, steering and follow-up queues, cancellation, and portable session primitives. |
| A working coding agent | A Textual TUI, print mode, file and shell tools, provider login and selection, durable sessions, extensions, skills, prompts, themes, rendering, and export. |

The coding agent is a reference application for the harness, not the boundary
of what the harness can become.

<!-- XODER_DEMO_GIF_PLACEHOLDER: insert docs/images/xoder-demo.gif here after capture. -->

## Why Xoder?

Many agent applications couple the model loop, tools, state, and interface into
one product-specific runtime. Xoder keeps those responsibilities separate so
you can replace one without rewriting the others.

- **Bring your own models.** Provider adapters normalize model streams into a
  provider-neutral event contract.
- **Bring your own tools.** Tools use explicit JSON schemas, async executors,
  structured results, and optional renderers.
- **Bring your own workflow.** Compose the harness directly or customize the
  included coding agent with Python extensions, skills, prompt templates, and
  project instructions.
- **Bring your own interface.** Consume typed events in the built-in TUI, print
  and JSON renderers, transcripts, or another frontend.
- **Keep state inspectable.** Sessions use durable JSONL records that can be
  resumed, branched, compacted, and exported.

## Make Xoder yours

Xoder exposes customization at several levels:

| Surface | How to customize it |
| --- | --- |
| Providers and models | Select built-in providers with `/login` and `/model`, overlay `~/.xoder/catalog.toml`, or connect a custom OpenAI-compatible endpoint. |
| Tools and workflow hooks | Load Python extensions that register tools and slash commands or intercept lifecycle, tool-call, and tool-result events. |
| Agent behavior and context | Use `AGENTS.md`, skills, prompt templates, project resources, and custom system instructions. |
| Presentation | Add message and tool renderers, notifications, dialogs, prompt-adjacent widgets, key handlers, or custom themes. |
| Applications | Import `xoder_agent`, supply a provider and tools, and consume its event stream from your own service or frontend. |

Personal customizations live under `~/.xoder/`. Project-specific resources can
live under `.xoder/` or the interoperable `.agents/` layout.

## Quickstart

Xoder requires Python 3.12 or newer. Install the `xoder` CLI from PyPI with
[uv](https://docs.astral.sh/uv/):

```bash
uv tool install xoder-ai==0.0.0
xoder --version
```

If `uv` is not installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Start Xoder in the project you want it to work on:

```bash
xoder --cwd /path/to/project
```

Connect a model provider and choose a model from the TUI:

```text
/login
/model
```

Then ask Xoder to work:

```text
explain the architecture of this project
```

For scripts and one-off prompts, use print mode:

```bash
xoder -p "summarize this repository"
xoder --cwd /path/to/project -p "find the CLI entry point"
```

To run Xoder from a source checkout instead:

```bash
git clone https://github.com/BANGHlxbackout/Xoder.git
cd Xoder
uv sync --dev
uv run xoder --version
```

## Architecture

```text
xoder_coding  →  xoder_agent  →  xoder_ai
```

| Package | Responsibility |
| --- | --- |
| `xoder_ai` | Provider adapters and provider-neutral model streaming. |
| `xoder_agent` | Portable messages, tools, events, agent loop, harness, queues, cancellation, and session primitives. |
| `xoder_coding` | The reference coding application: CLI, TUI, resources, provider configuration, tools, skills, extensions, rendering, and persistence. |

The central boundary is:

```text
AgentHarness = reusable agent runtime
AgentSession = coding-agent environment
TUI          = one possible frontend
```

`xoder_agent` does not depend on Textual, Rich rendering, application
configuration paths, slash commands, or coding-specific resource loading.
Frontends and applications communicate with it through typed events and
provider-neutral contracts.

## Build with the harness

Install the same PyPI distribution as a project dependency:

```bash
uv add xoder-ai==0.0.0
# or: python -m pip install xoder-ai==0.0.0
```

The harness accepts any object that implements the `ModelProvider` protocol
and any collection of `AgentTool` definitions. This deterministic example runs
locally without credentials; replace `FakeProvider` with the provider used by
your application.

```python
import asyncio

from xoder_ai import AssistantDoneEvent, AssistantStartEvent, FakeProvider
from xoder_agent import (
    AgentHarness,
    AgentHarnessConfig,
    AssistantMessage,
    message_text,
)


async def main() -> None:
    reply = AssistantMessage(content="Hello from Xoder", model="demo", stop_reason="stop")
    provider = FakeProvider(
        [[
            AssistantStartEvent(partial=AssistantMessage(model="demo")),
            AssistantDoneEvent(reason="stop", message=reply),
        ]]
    )
    harness = AgentHarness(
        AgentHarnessConfig(
            provider=provider,
            model="demo",
            system="You are a helpful project agent.",
            tools=[],
        )
    )

    async for _ in harness.prompt("Hello"):
        pass
    print(message_text(harness.messages[-1]))


asyncio.run(main())
```

The same harness can drive a terminal UI, a background service, a test fixture,
or a frontend with different rendering rules.

## Extend the coding agent

Extensions are ordinary Python modules with a `setup(xoder)` entry point. They
can register tools and slash commands, observe agent and session events,
intercept tool calls and results, send custom messages, and extend TUI
presentation.

Run the included custom-tool example directly:

```bash
uv run xoder -x examples/extensions/hello_tool.py
```

Two small examples show the public extension boundary:

- [`hello_tool.py`](examples/extensions/hello_tool.py) registers a typed tool.
- [`permission_gate.py`](examples/extensions/permission_gate.py) blocks
  selected dangerous shell commands before execution.

See the [extensions guide](src/xoder_coding/data/docs/extensions.md) for loading
locations, hooks, and implementation guidance.

## What ships today

- Interactive Textual TUI and non-interactive print mode.
- Built-in `read`, `write`, `edit`, and `bash` coding tools.
- Multiple model-provider adapters and custom OpenAI-compatible endpoints,
  including local endpoints that implement the protocol.
- Durable sessions under `~/.xoder/sessions/`, with resume, branching,
  compaction, statistics, and export.
- Slash commands for provider login, model selection, sessions, resources,
  themes, and other runtime controls.
- Project instructions and resources from `AGENTS.md`, `.xoder/`, and
  `.agents/`.
- Skills, prompt templates, Python extensions, custom renderers, and TUI themes.
- Rich, plain-text, JSON, transcript, and custom event consumers.

## Engineering principles

- **Small layers beat magic.** Each package has one explicit responsibility.
- **Events are the contract.** Providers, tools, sessions, renderers, and
  frontends meet at typed event boundaries.
- **The core stays portable.** Coding policy and UI dependencies remain outside
  the reusable harness.
- **Tools are ordinary typed functions.** Schemas and structured results stay
  visible and testable.
- **Sessions are durable and inspectable.** Runtime history remains readable
  instead of being hidden in an opaque database.
- **Tests do not require live models.** Fake providers and tools exercise the
  agent loop deterministically.

## Documentation

Until the dedicated Xoder website is available, repository-owned references
live with the packaged source:

- [Documentation index](src/xoder_coding/data/docs/README.md)
- [Architecture](src/xoder_coding/data/docs/architecture.md)
- [CLI](src/xoder_coding/data/docs/cli.md)
- [Extensions](src/xoder_coding/data/docs/extensions.md)
- [Models and providers](src/xoder_coding/data/docs/models.md)
- [Skills and prompt templates](src/xoder_coding/data/docs/skills.md)
- [TUI](src/xoder_coding/data/docs/tui.md)

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for architecture boundaries, local setup,
testing expectations, and pull request guidance.

```bash
uv sync --dev
XODER_TEST_HOME="$(mktemp -d)"
HOME="$XODER_TEST_HOME" \
USERPROFILE="$XODER_TEST_HOME" \
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

Report bugs and propose changes through
[GitHub Issues](https://github.com/BANGHlxbackout/Xoder/issues).

## License

Xoder is distributed under the [MIT License](LICENSE).
