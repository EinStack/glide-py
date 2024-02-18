# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0
from typing import List, Optional

from pydantic import BaseModel


class LangRouter(BaseModel):
    ...


class ChatMessage(BaseModel):
    name: str
    content: str
    role: str


class ModelMessageOverride(BaseModel):
    """
    Allows to override a message that is asked if the specific model ends up serving the chat request
    """
    model_id: str
    message: ChatMessage


class ChatRequest(BaseModel):
    message: ChatMessage
    message_history: List[ChatMessage]
    override: Optional[List[ModelMessageOverride]]


class ChatResponse(BaseModel):
    ...
