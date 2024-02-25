# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0
from datetime import datetime
from typing import List, Optional

from pydantic import Field

from glide.schames import Schema


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
    cached: bool = False
    model_response: ModelResponse
