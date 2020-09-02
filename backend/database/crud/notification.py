import pymongo
from datetime import datetime
from typing import List

from database.crud.base import BaseMongoCRUD
from schemas.user import User


class NotificationCRUD(BaseMongoCRUD):
    collection = "notification"

    @classmethod
    async def create_notification(cls, user: User, payload: dict) -> None:
        payload["user_id"] = user.id
        payload["watched"] = False
        payload["created_at"] = datetime.utcnow()
        await cls.insert_one(payload=payload)

    @classmethod
    async def get_user_notifications(cls, user: User) -> List[dict]:
        query = {
            "user_id": user.id,
            "watched": False
        }
        return await cls.find_many(query=query, limit=7, sort=[("created_at", pymongo.DESCENDING)])

    @classmethod
    async def watch_notifications(cls, user: User) -> bool:
        await cls.update_many(
            query={
                "user_id": user
            },
            payload={
                "watched": True
            }
        )
        return True
