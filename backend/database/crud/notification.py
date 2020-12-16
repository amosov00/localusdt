import pymongo
from bson import ObjectId
from http import HTTPStatus
from datetime import datetime
from fastapi import HTTPException

from schemas.user import User
from database.crud.base import BaseMongoCRUD
from schemas.notification import Notification, NotificationWatch


class NotificationCRUD(BaseMongoCRUD):
    collection = "notification"

    @classmethod
    async def create_notification(cls, payload: Notification) -> ObjectId:
        payload.watched = False
        payload.created_at = datetime.utcnow()
        return (await cls.insert_one(payload=payload.dict())).inserted_id

    @classmethod
    async def get_user_notifications(cls, user: User):
        query = {
            "user_id": user.id
        }
        result = await cls.find_many(query=query, limit=10, sort=[("created_at", pymongo.DESCENDING)])
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

    @classmethod
    async def watch_notification(cls, user: User, notification_id: str) -> bool:
        notification = await cls.find_one(query={
            "_id": ObjectId(notification_id),
            "user_id": user.id
        })
        if not notification:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Notification not found")
        await cls.update_one(
            query={"_id": notification.get("_id")},
            payload={"watched": True}
        )
        return True

    @classmethod
    async def watch_notifications_selectively(cls, user: User, payload: NotificationWatch):
        for notification_id in payload.notification_ids:
            notification = await cls.find_one(query={
                "_id": ObjectId(notification_id),
                "user_id": user.id
            })
            if notification:
                await cls.update_one(
                    query={"_id": ObjectId(notification.get("_id"))},
                    payload={"watched": True}
                )
        return True
