from typing import List, Union
from fastapi import HTTPException
from http import HTTPStatus

from schemas.base import ObjectId
from schemas.chat import ChatRoom, ChatRoomResponse
from database.crud.chat import ChatRoomCRUD, ChatMessageCRUD


class ChatWrapper:
    @staticmethod
    async def create_chat(users_id: List[ObjectId]) -> ObjectId:
        new_room = ChatRoom(participants=users_id)
        return await ChatRoomCRUD.create_chat(new_room)

    @staticmethod
    async def get_chatroom_with_messages(user_id: str, chatroom_id: str) -> ChatRoomResponse:
        messages = await ChatMessageCRUD.get_messages_chatroom(chatroom_id)
        chatroom = await ChatRoomCRUD.find_by_id(chatroom_id)

        if not chatroom:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong chatroom")

        chatroom["messages"] = messages

        if ObjectId(user_id) not in chatroom["participants"]:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Access denied")

        return chatroom

    @staticmethod
    async def get_chatroom_with_messages_unsafe(chatroom_id: str) -> ChatRoomResponse:
        messages = await ChatMessageCRUD.get_messages_chatroom(chatroom_id)
        chatroom = await ChatRoomCRUD.find_by_id(chatroom_id)

        if not chatroom:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong chatroom")

        chatroom["messages"] = messages

        return chatroom
