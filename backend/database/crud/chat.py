import pymongo

from database.crud.base import BaseMongoCRUD
from schemas.chat import ChatRoom, ChatRoomInDB
from schemas.base import ObjectId

from datetime import datetime

__all__ = ["ChatRoomCRUD", "ChatMessageCRUD"]


class ChatRoomCRUD(BaseMongoCRUD):
    collection = "chatroom"

    @classmethod
    async def create_chat(cls, payload: ChatRoom) -> ObjectId:
        return (await cls.insert_one({
            **payload.dict(),
            "created_at": datetime.now()
        })).inserted_id


class ChatMessageCRUD(BaseMongoCRUD):
    collection = "chat_msg"

    @classmethod
    async def get_messages_chatroom(cls, chatroom_id: str) -> list:
        query = {"chatroom_id": ObjectId(chatroom_id)}
        return await cls.find_many(query=query, sort=[("created_at", pymongo.ASCENDING)])
