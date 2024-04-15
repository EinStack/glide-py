# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0
import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any

from pydantic import Field

from glide.schames import Schema
from glide.typing import RouterId, ProviderName, ModelName

ChatRequestId = str
Metadata = Dict[str, Any]


class FinishReason(str, Enum):
    # generation is finished successfully without interruptions
    COMPLETE = "complete"
    # generation is interrupted because of the length of the response text
    MAX_TOKENS = "max_tokens"
    CONTENT_FILTERED = "content_filtered"
    OTHER = "other"


class LangRouter(Schema): ...


class ChatMessage(Schema):
    content: str
    role: str  # TODO: make it optional and default
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
    prompt_tokens: int
    response_tokens: int
    total_tokens: int


class ModelResponse(Schema):
    response_id: dict[str, str]
    message: ChatMessage
    token_count: TokenUsage


class ChatResponse(Schema):
    id: ChatRequestId
    created: datetime
    provider: ProviderName
    router: RouterId
    model_id: str
    model: ModelName
    model_response: ModelResponse


class ChatStreamRequest(Schema):
    id: ChatRequestId = Field(default_factory=lambda: str(uuid.uuid4()))
    message: ChatMessage
    message_history: List[ChatMessage] = Field(default_factory=list)
    override: Optional[ModelMessageOverride] = None
    metadata: Optional[Metadata] = None


class ModelChunkResponse(Schema):
    metadata: Optional[Metadata] = None
    message: ChatMessage


class ChatStreamChunk(Schema):
    """
    A response chunk of a streaming chat
    """

    model_id: str

    provider_name: ProviderName
    model_name: ModelName

    model_response: ModelChunkResponse
    finish_reason: Optional[FinishReason] = None


class ChatStreamError(Schema):
    id: ChatRequestId
    err_code: str
    message: str


class ChatStreamMessage(Schema):
    id: ChatRequestId
    created_at: datetime
    metadata: Optional[Metadata] = None

    router_id: RouterId

    chunk: Optional[ChatStreamChunk] = None
    error: Optional[ChatStreamError] = None

    @property
    def content_chunk(self) -> Optional[str]:
        if not self.chunk:
            return None

        return self.chunk.model_response.message.content
