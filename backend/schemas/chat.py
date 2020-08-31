from typing import List
from pydantic import Field
from datetime import datetime

from schemas.base import BaseModel, ObjectIdPydantic


__all__ = [
    "ChatRoom",
    "ChatMessage",
    "ChatRoomInDB",
    "ChatMessageInDB",
    "ChatRoomResponse"
]


class ChatRoom(BaseModel):
    participants: List[ObjectIdPydantic] = Field(default=[])


class ChatRoomInDB(ChatRoom):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
    created_at: datetime = Field(default=datetime.now)


class ChatMessage(BaseModel):
    chatroom_id: ObjectIdPydantic = Field(...)
    sender: str = Field(...)
    message_body: str = Field(default="")
    is_service: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.now)


class ChatMessageInDB(ChatMessage):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class ChatRoomResponse(ChatRoom):
    messages: List[ChatMessage] = Field(default=[])
