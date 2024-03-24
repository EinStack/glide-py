# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0
import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Union

from pydantic import Field

from glide.schames import Schema

Metadata = Dict[str, Any]


class FinishReason(str, Enum):
    COMPLETE = "complete"


class LangRouter(Schema): ...


class ChatMessage(Schema):
    content: str
    role: str
    name: Optional[str] = None


class ModelMessageOverride(Schema):
    """
    Allows to override a message that is asked if the specific model ends up serving the chat request
    """

    model: str
    message: ChatMessage


class ChatRequest(Schema):
    message: ChatMessage
    message_history: List[ChatMessage] = Field(default_factory=list)
    override: Optional[ModelMessageOverride] = None


class TokenUsage(Schema):
    prompt_tokens: float
    response_tokens: float
    total_tokens: float


class ModelResponse(Schema):
    response_id: dict[str, str]
    message: ChatMessage
    token_count: TokenUsage


class ChatResponse(Schema):
    id: str
    created: datetime
    provider: str
    router: str
    model_id: str
    model: str
    model_response: ModelResponse


class StreamChatRequest(Schema):
    id: str = Field(default_factory=uuid.uuid4)
    message: ChatMessage
    message_history: List[ChatMessage] = Field(default_factory=list)
    override: Optional[ModelMessageOverride] = None
    metadata: Optional[Metadata] = None


class ModelChunkResponse(Schema):
    metadata: Optional[Metadata] = None
    message: ChatMessage
    finish_reason: Optional[FinishReason] = None


class ChatStreamChunk(Schema):
    """
    A response chunk of a streaming chat
    """

    id: str
    created: datetime
    provider: str
    router: str
    model_id: str
    model: str
    metadata: Optional[Metadata] = None
    model_response: ModelChunkResponse


class ChatStreamError(Schema):
    id: str
    err_code: str
    message: str
    metadata: Optional[Metadata] = None


StreamResponse = Union[ChatStreamChunk, ChatStreamError]
