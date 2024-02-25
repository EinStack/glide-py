# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class LangRouter(BaseModel): ...


class ChatMessage(BaseModel):
    content: str
    role: str
    name: Optional[str] = None


class ModelMessageOverride(BaseModel):
    """
    Allows to override a message that is asked if the specific model ends up serving the chat request
    """

    model_id: str
    message: ChatMessage


class ChatRequest(BaseModel):
    message: ChatMessage
    message_history: List[ChatMessage]
    override: Optional[ModelMessageOverride]


class TokenUsage(BaseModel):
    prompt_tokens: float
    response_tokens: float
    total_tokens: float


class ModelResponse(BaseModel):
    system_id: dict[str, str]
    message: ChatMessage
    token_usage: TokenUsage


class ChatResponse(BaseModel):
    id: str
    created: datetime
    provider: str
    router_id: str
    model: str
    cached: bool
    model_response: ModelResponse
