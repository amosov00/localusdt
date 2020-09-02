from typing import Optional, List
from pydantic import Field
from datetime import datetime
from enum import IntEnum

from schemas.base import BaseModel, ObjectIdPydantic


__all__ = [
    "NotificationType",
    "Notification",
    "NotificationInDB",
    "Notifications"
]


class NotificationType(IntEnum):
    NEW_INVOICE = 1
    DEPOSIT = 2
    WITHDRAW = 3
    SYSTEM = 4


class Notification(BaseModel):
    user_id: ObjectIdPydantic = Field(...)
    type: NotificationType = Field(...)
    watched: bool = Field(...)
    participant_nickname: str = Field(default=None)
    system_message: str = Field(default=None)
    amount: float = Field(default=None)
    created_at: datetime = Field(default=None)


class NotificationInDB(Notification):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class Notifications(BaseModel):
    notifications: List[Notification] = Field(default=[])
