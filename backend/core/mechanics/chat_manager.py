import asyncio
import json
from datetime import datetime
from fastapi import WebSocket
from collections import defaultdict


__all__ = ["ChatManager", "chat_manager"]


class ChatManager:
    def __init__(self):
        self.connections: dict = {}
        self.generator = self.get_notification_generator()

    async def init_manager(self):
        await self.generator.asend(None)

    async def get_notification_generator(self):
        while True:
            message = yield
            msg = message["message"]
            chatroom_id = message["chatroom_id"]
            await self._notify(msg, chatroom_id)

    async def push(self, msg: dict, chatroom_id: str):
        msg["created_at"] = str(msg["created_at"])
        msg["_id"] = None
        message_body = {
            "message": json.dumps(msg, ensure_ascii=False),
            "chatroom_id": chatroom_id
        }
        await self.generator.asend(message_body)

    async def connect(self, websocket: WebSocket, chatroom: str):
        await websocket.accept()
        if chatroom not in self.connections:
            self.connections[chatroom] = []
        self.connections[chatroom].append(websocket)

    def remove(self, websocket: WebSocket, room_name: str):
        self.connections[room_name].remove(websocket)

    async def _notify(self, message: str, chatroom_id: str):
        for websocket in self.connections[chatroom_id]:
            await websocket.send_text(message)


chat_manager = ChatManager()



