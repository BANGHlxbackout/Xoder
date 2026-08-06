"""Provider and Pi-compatible model streaming layer for Xoder."""

# ruff: noqa: F401 - this module intentionally defines the public facade

from xoder_ai.anthropic import AnthropicProvider
from xoder_ai.env import (
    DEFAULT_ANTHROPIC_BASE_URL,
    DEFAULT_OPENAI_COMPATIBLE_MAX_RETRIES,
    DEFAULT_OPENAI_COMPATIBLE_MAX_RETRY_DELAY_SECONDS,
    DEFAULT_OPENAI_COMPATIBLE_TIMEOUT_SECONDS,
    AnthropicConfig,
    OpenAICompatibleConfig,
    RuntimeProviderAuth,
    openai_compatible_config_from_env,
)
from xoder_ai.events import (
    AssistantDoneEvent,
    AssistantErrorEvent,
    AssistantMessageEvent,
    AssistantStartEvent,
    TextDeltaEvent,
    TextEndEvent,
    TextStartEvent,
    ThinkingDeltaEvent,
    ThinkingEndEvent,
    ThinkingStartEvent,
    ToolCallDeltaEvent,
    ToolCallEndEvent,
    ToolCallStartEvent,
)
from xoder_ai.fake import FakeProvider
from xoder_ai.google import GoogleGenerativeAIProvider
from xoder_ai.mistral import MistralConversationsProvider
from xoder_ai.model_limits import ModelLimitsProvider, RuntimeModelLimits
from xoder_ai.openai_codex import (
    DEFAULT_OPENAI_CODEX_BASE_URL,
    OpenAICodexConfig,
    OpenAICodexCredentials,
    OpenAICodexProvider,
)
from xoder_ai.openai_compatible import OpenAICompatibleProvider
from xoder_ai.provider import CancellationToken, ModelProvider

__all__ = [name for name in globals() if not name.startswith("_")]
