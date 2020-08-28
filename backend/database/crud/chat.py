from database.crud.base import BaseMongoCRUD
from schemas.chat import ChatRoom, ChatRoomInDB
from schemas.base import ObjectId

from datetime import datetime

__all__ = ["ChatRoomCRUD"]


class ChatRoomCRUD(BaseMongoCRUD):
    collection = "chatroom"

    @classmethod
    async def create_chat(cls, payload: ChatRoom) -> ObjectId:
        return (await cls.insert_one({
            **payload.dict(),
            "created_at": datetime.now()
        })).inserted_id
