from typing import List

from schemas.base import ObjectId
from schemas.chat import ChatRoom
from database.crud.chat import ChatRoomCRUD


class ChatWrapper:
    @staticmethod
    async def create_chat(users_id: List[ObjectId]) -> ObjectId:
        new_room = ChatRoom(participants=users_id)
        return await ChatRoomCRUD.create_chat(new_room)
