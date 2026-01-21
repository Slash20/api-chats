from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List


class MessageOut(BaseModel):
    id: int
    chat_id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class ChatOut(BaseModel):
    id: int
    title: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)


class ChatWithMessages(BaseModel):
    chat: ChatOut
    messages: List[MessageOut] = []