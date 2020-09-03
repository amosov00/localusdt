import pymongo
from datetime import datetime
from typing import List

from database.crud.base import BaseMongoCRUD
from schemas.notification import Notification
from schemas.user import User


class NotificationCRUD(BaseMongoCRUD):
    collection = "notification"

    @classmethod
    async def create_notification(cls, payload: Notification) -> None:
        payload.watched = False
        payload.created_at = datetime.utcnow()
        await cls.insert_one(payload=payload.dict())

    @classmethod
    async def get_user_notifications(cls, user: User):
        query = {
            "user_id": user.id,
            "watched": False
        }
        result = await cls.find_many(query=query, limit=7, sort=[("created_at", pymongo.DESCENDING)])
        return result

    @classmethod
    async def watch_notifications(cls, user: User) -> bool:
        await cls.update_many(
            query={
                "user_id": user.id
            },
            payload={
                "watched": True
            }
        )
        return True

