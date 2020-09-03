import asyncio
import json
from typing import List, Optional
from datetime import datetime
from fastapi import WebSocket
from collections import defaultdict

from schemas.notification import NotificationType, Notification
from database.crud.notification import NotificationCRUD


__all__ = ["NotificationManager", "notification_manager", "NotificationSender"]


class NotificationManager:
    def __init__(self):
        self.connections: dict = {}
        self.generator = self.get_notification_generator()

    async def init_manager(self):
        await self.generator.asend(None)

    async def get_notification_generator(self):
        while True:
            message = yield
            msg = message["message"]
            user_id = message["user_id"]
            await self._notify(msg, user_id)

    async def push(self, msg: dict, user_id: str):
        message_body = {
            "message": msg,
            "user_id": user_id
        }
        await self.generator.asend(message_body)

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.connections[user_id] = websocket

    def remove(self, websocket: WebSocket, user_id: str):
        self.connections[user_id] = None if websocket == self.connections[user_id] else self.connections[user_id]

    async def _notify(self, message: dict, user_id: str):
        message["user_id"] = str(message["user_id"])
        if "invoice_id" in message:
            message["invoice_id"] = str(message["invoice_id"])
        message["created_at"] = str(message["created_at"])
        if self.connections.get(user_id) is not None:
            await self.connections[user_id].send_json(message)


notification_manager = NotificationManager()


class NotificationSender:
    @staticmethod
    async def send_new_invoice(user_id: str, **kwargs) -> None:
        """
        :param user_id:
        :param kwargs: participant_nickname, amount, invoice_id
        :return:
        """
        new_notification = Notification(
            type=NotificationType.NEW_INVOICE,
            watched=False,
            user_id=user_id,
            amount=kwargs.get("amount"),
            created_at=datetime.utcnow(),
            participant_nickname=kwargs.get("participant_nickname"),
            invoice_id=kwargs.get("invoice_id")
        )
        await notification_manager.push(new_notification.dict(), user_id)
        await NotificationCRUD.create_notification(new_notification)









