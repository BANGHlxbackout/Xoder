# Xoder

<p align="center">
  <strong>一个可定制的 Python agent harness，并内置完整的终端 coding agent。</strong>
</p>

<p align="center">
  <a href="README.md">English</a>
  · 简体中文
</p>

<p align="center">
  <a href="#快速开始">快速开始</a>
  ·
  <a href="#定制-xoder">定制</a>
  ·
  <a href="#架构">架构</a>
  ·
  <a href="#基于-harness-构建">作为库使用</a>
</p>

Xoder 提供一组可复用的 agent 原语，让你围绕自己的模型、工具、工作流和
界面构建能够调用工具的 agent。它同时内置了一个完整的终端 coding agent，
用真实应用验证这些原语：交互式 TUI、文件和 shell 工具、持久化 session、
模型配置、skills、extensions、prompt templates 和 themes。

你可以直接把 Xoder 当作终端 agent 使用，也可以改造内置的 coding 工作流，
或者把可移植的 `xoder_agent` harness 嵌入自己的应用。

> **项目状态：** Xoder `0.0.0` 是早期版本，需要 Python 3.12 或更高版本。
> 随着项目继续开发，公开 API 和工作流仍可能发生变化。

## Xoder 是什么？

Xoder 的灵感来自
[Pi 的极简、可扩展 agent-harness 架构](https://github.com/earendil-works/pi)。
它在类型明确的 Python 代码库中实现相同的职责分离：模型 provider、可移植
agent runtime，以及完整的 coding 应用。

Xoder 有意同时承担两种角色：

| 使用方式 | 你会得到什么 |
| --- | --- |
| 可复用的 agent harness | provider-neutral agent loop、类型化消息和事件、工具执行、steering 与 follow-up 队列、取消机制和可移植 session 原语。 |
| 可运行的 coding agent | Textual TUI、print mode、文件和 shell 工具、provider 登录和选择、持久化 session、extensions、skills、prompts、themes、渲染和导出。 |

内置 coding agent 是 harness 的参考应用，而不是 harness 能力的边界。

<!-- XODER_DEMO_GIF_PLACEHOLDER: insert docs/images/xoder-demo.gif here after capture. -->

## 为什么选择 Xoder？

很多 agent 应用把模型循环、工具、状态和界面耦合在一个产品专用 runtime
中。Xoder 将这些职责拆开，让你可以替换其中一层，而不需要重写其他部分。

- **使用自己的模型。** Provider adapters 将模型流统一成 provider-neutral
  事件契约。
- **使用自己的工具。** 工具使用明确的 JSON schema、异步 executor、结构化
  结果和可选 renderer。
- **使用自己的工作流。** 直接组合 harness，或通过 Python extensions、
  skills、prompt templates 和项目指令定制内置 coding agent。
- **使用自己的界面。** 在内置 TUI、print 和 JSON renderers、transcript
  或其他 frontend 中消费类型化事件。
- **保持状态可检查。** Session 使用持久化 JSONL 记录，可以恢复、分支、
  压缩和导出。

## 定制 Xoder

Xoder 在多个层面提供定制入口：

| 定制层面 | 定制方式 |
| --- | --- |
| Providers 和 models | 通过 `/login` 与 `/model` 选择内置 provider，使用 `~/.xoder/catalog.toml` 覆盖 catalog，或连接自定义 OpenAI-compatible endpoint。 |
| 工具和工作流 hooks | 加载 Python extensions，注册工具和 slash commands，或拦截 lifecycle、tool-call 和 tool-result 事件。 |
| Agent 行为和上下文 | 使用 `AGENTS.md`、skills、prompt templates、项目资源和自定义 system instructions。 |
| 展示层 | 添加消息和工具 renderers、notifications、dialogs、prompt 周边 widgets、key handlers 或自定义 themes。 |
| 自己的应用 | 导入 `xoder_agent`，提供 provider 和 tools，并在自己的 service 或 frontend 中消费事件流。 |

个人定制内容位于 `~/.xoder/`。项目级资源可以放在 `.xoder/`，也可以使用
可互操作的 `.agents/` 目录结构。

## 快速开始

Xoder 需要 Python 3.12 或更高版本。使用
[uv](https://docs.astral.sh/uv/) 从 PyPI 安装 `xoder` CLI：

```bash
uv tool install xoder-ai==0.0.0
xoder --version
```

如果尚未安装 `uv`：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

在希望 Xoder 操作的项目中启动它：

```bash
xoder --cwd /path/to/project
```

在 TUI 中连接 model provider 并选择模型：

```text
/login
/model
```

然后向 Xoder 提出任务：

```text
解释这个项目的架构
```

脚本和一次性任务可以使用 print mode：

```bash
xoder -p "总结这个仓库"
xoder --cwd /path/to/project -p "找到 CLI 的入口"
```

如需从源码 checkout 运行 Xoder：

```bash
git clone https://github.com/BANGHlxbackout/Xoder.git
cd Xoder
uv sync --dev
uv run xoder --version
```

## 架构

```text
xoder_coding  →  xoder_agent  →  xoder_ai
```

| Package | 职责 |
| --- | --- |
| `xoder_ai` | Provider adapters 和 provider-neutral 模型流。 |
| `xoder_agent` | 可移植的消息、工具、事件、agent loop、harness、队列、取消机制和 session 原语。 |
| `xoder_coding` | 参考 coding 应用：CLI、TUI、资源、provider 配置、工具、skills、extensions、渲染和持久化。 |

核心边界是：

```text
AgentHarness = 可复用的 agent runtime
AgentSession = coding-agent 环境
TUI          = 一种可替换的 frontend
```

`xoder_agent` 不依赖 Textual、Rich rendering、应用配置路径、slash commands
或 coding 专用资源加载。Frontend 和应用通过类型化事件与 provider-neutral
契约和它通信。

## 基于 harness 构建

把同一个 PyPI 发行包安装为项目依赖：

```bash
uv add xoder-ai==0.0.0
# 或者：python -m pip install xoder-ai==0.0.0
```

Harness 接受任何实现 `ModelProvider` protocol 的对象，以及任意
`AgentTool` 集合。下面的确定性示例无需凭证即可在本地运行；在实际应用中，
可以把 `FakeProvider` 替换为自己的 provider。

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

同一个 harness 可以驱动终端 UI、后台 service、测试 fixture，或使用其他渲染
规则的 frontend。

## 扩展内置 coding agent

Extension 是带有 `setup(xoder)` 入口的普通 Python module。它们可以注册
工具和 slash commands、观察 agent 与 session 事件、拦截工具调用和结果、
发送自定义消息，以及扩展 TUI 展示。

可以直接运行内置的自定义工具示例：

```bash
uv run xoder -x examples/extensions/hello_tool.py
```

两个小型示例展示了公开 extension 边界：

- [`hello_tool.py`](examples/extensions/hello_tool.py) 注册一个类型化工具。
- [`permission_gate.py`](examples/extensions/permission_gate.py) 在执行前阻止
  选定的危险 shell commands。

加载位置、hooks 和实现规则见
[extensions 指南](src/xoder_coding/data/docs/extensions.md)。

## 当前已经实现

- 交互式 Textual TUI 和非交互 print mode。
- 内置 `read`、`write`、`edit` 和 `bash` coding tools。
- 多种 model-provider adapters 和自定义 OpenAI-compatible endpoints，包括
  实现相同协议的本地 endpoint。
- 位于 `~/.xoder/sessions/` 的持久化 session，支持恢复、分支、压缩、统计和导出。
- 用于 provider 登录、模型选择、sessions、resources、themes 和其他 runtime
  控制的 slash commands。
- 来自 `AGENTS.md`、`.xoder/` 和 `.agents/` 的项目指令与资源。
- Skills、prompt templates、Python extensions、自定义 renderers 和 TUI themes。
- Rich、plain-text、JSON、transcript 和自定义事件 consumers。

## 工程原则

- **小而明确的分层优于魔法。** 每个 package 只有一个明确职责。
- **事件就是契约。** Providers、tools、sessions、renderers 和 frontends
  在类型化事件边界上协作。
- **核心保持可移植。** Coding policy 和 UI 依赖留在可复用 harness 之外。
- **工具是普通的类型化函数。** Schema 和结构化结果保持可见、可测试。
- **Session 持久且可检查。** Runtime history 保持可读，不隐藏在不透明数据库中。
- **测试不依赖真实模型。** Fake providers 和 tools 可以确定性地验证 agent loop。

## 文档

在 Xoder 专用网站上线前，仓库维护的参考文档和源码一起发布：

- [文档索引](src/xoder_coding/data/docs/README.md)
- [架构](src/xoder_coding/data/docs/architecture.md)
- [CLI](src/xoder_coding/data/docs/cli.md)
- [Extensions](src/xoder_coding/data/docs/extensions.md)
- [Models 和 providers](src/xoder_coding/data/docs/models.md)
- [Skills 和 prompt templates](src/xoder_coding/data/docs/skills.md)
- [TUI](src/xoder_coding/data/docs/tui.md)

## 开发

架构边界、本地环境、测试要求和 pull request 规范见
[CONTRIBUTING.md](CONTRIBUTING.md)。

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

Bug 和改动建议请提交到
[GitHub Issues](https://github.com/BANGHlxbackout/Xoder/issues)。

## 许可证

Xoder 使用 [MIT License](LICENSE)。
