import asyncio
from datetime import datetime
from fastapi import WebSocket
from collections import defaultdict


__all__ = ["ChatManager", "chat_manager"]


class ChatManager:
    def __init__(self):
        self.connections: dict = defaultdict(dict)
        self.generator = self.get_notification_generator()

    async def init_manager(self):
        await self.generator.asend(None)

    async def get_notification_generator(self):
        while True:
            message = yield
            msg = message["message"]
            chatroom_id = message["chatroom_id"]
            await self._notify(msg, chatroom_id)

    async def push(self, msg: str, chatroom_id: str, sender: str):
        message_body = {
            "message": msg,
            "chatroom_id": chatroom_id,
            "sender": sender
        }
        await self.generator.asend(message_body)

    async def connect(self, websocket: WebSocket, chatroom: str):
        await websocket.accept()
        if self.connections[chatroom] == {} or len(self.connections[chatroom]) == 0:
            self.connections[chatroom] = []
        self.connections[chatroom].append(websocket)

    def remove(self, websocket: WebSocket, room_name: str):
        self.connections[room_name].remove(websocket)

    async def _notify(self, message: str, chatroom_id: str):
        living_connections = []
        while len(self.connections[chatroom_id]) > 0:
            # Looping like this is necessary in case a disconnection is handled
            # during await websocket.send_text(message)
            websocket = self.connections[chatroom_id].pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        self.connections[chatroom_id] = living_connections


chat_manager = ChatManager()

asyncio.create_task(chat_manager.init_manager())



