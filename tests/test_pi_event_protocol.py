"""Focused contract tests for the canonical Pi-shaped event stream."""

from pathlib import Path

import pytest

import xoder_agent
import xoder_agent.events
import xoder_agent.provider
import xoder_agent.session
import xoder_agent.types
import xoder_ai
import xoder_ai.http
import xoder_ai.provider
import xoder_ai.stream
from xoder_agent import (
    AgentEndEvent,
    AgentHarness,
    AgentHarnessConfig,
    AssistantMessage,
    MessageEndEvent,
    MessageUpdateEvent,
    TextContent,
    ToolCall,
    ToolExecutionEndEvent,
    ToolExecutionStartEvent,
    ToolResultMessage,
)
from xoder_agent.provider_events import (
    AssistantDoneEvent,
    AssistantStartEvent,
    TextDeltaEvent,
    TextEndEvent,
    TextStartEvent,
    ToolCallEndEvent,
    ToolCallStartEvent,
)
from xoder_ai import FakeProvider


def test_xoder_agent_does_not_import_xoder_ai() -> None:
    for path in Path("src/xoder_agent").rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "from xoder_ai" not in source, path
        assert "import xoder_ai" not in source, path


def test_xoder_ai_reexports_canonical_event_classes() -> None:
    from xoder_ai.events import TextDeltaEvent as public

    assert public is TextDeltaEvent


def test_core_module_docstrings_use_xoder_branding() -> None:
    modules = (
        xoder_ai,
        xoder_ai.http,
        xoder_ai.provider,
        xoder_ai.stream,
        xoder_agent,
        xoder_agent.events,
        xoder_agent.provider,
        xoder_agent.session,
        xoder_agent.types,
    )

    for module in modules:
        assert module.__doc__ is not None
        assert "Xoder" in module.__doc__
        assert "Tau" not in module.__doc__


@pytest.mark.anyio
async def test_text_stream_has_nested_updates_and_terminal_messages() -> None:
    empty = AssistantMessage(model="fake")
    hello = AssistantMessage(model="fake", content=[TextContent(text="hello")])
    provider = FakeProvider(
        [
            [
                AssistantStartEvent(partial=empty),
                TextStartEvent(content_index=0, partial=empty),
                TextDeltaEvent(content_index=0, delta="hello", partial=hello),
                TextEndEvent(content_index=0, content="hello", partial=hello),
                AssistantDoneEvent(reason="stop", message=hello),
            ]
        ]
    )
    harness = AgentHarness(AgentHarnessConfig(provider=provider, model="fake", system="test"))

    events = [event async for event in harness.prompt("hi")]

    assert [event.type for event in events] == [
        "agent_start",
        "turn_start",
        "message_start",
        "message_end",
        "message_start",
        "message_update",
        "message_update",
        "message_update",
        "message_end",
        "turn_end",
        "agent_end",
    ]
    updates = [event for event in events if isinstance(event, MessageUpdateEvent)]
    assert [event.assistant_message_event.type for event in updates] == [
        "text_start",
        "text_delta",
        "text_end",
    ]
    assert isinstance(events[-1], AgentEndEvent)
    assert events[-1].messages[-1] == hello


@pytest.mark.anyio
async def test_tool_result_gets_execution_and_message_lifecycle_events() -> None:
    call = ToolCall(id="call-1", name="missing", arguments={})
    partial = AssistantMessage(model="fake", content=[call])
    provider = FakeProvider(
        [
            [
                AssistantStartEvent(partial=AssistantMessage(model="fake")),
                ToolCallStartEvent(content_index=0, partial=partial),
                ToolCallEndEvent(content_index=0, tool_call=call, partial=partial),
                AssistantDoneEvent(reason="toolUse", message=partial),
            ],
            [
                AssistantStartEvent(partial=AssistantMessage(model="fake")),
                AssistantDoneEvent(
                    reason="stop",
                    message=AssistantMessage(model="fake", content=[TextContent(text="done")]),
                ),
            ],
        ]
    )
    harness = AgentHarness(AgentHarnessConfig(provider=provider, model="fake", system="test"))

    events = [event async for event in harness.prompt("use it")]

    start = next(event for event in events if isinstance(event, ToolExecutionStartEvent))
    end = next(event for event in events if isinstance(event, ToolExecutionEndEvent))
    result_end = next(
        event
        for event in events
        if isinstance(event, MessageEndEvent) and isinstance(event.message, ToolResultMessage)
    )
    assert start.tool_call_id == end.tool_call_id == result_end.message.tool_call_id
    assert end.is_error is True
