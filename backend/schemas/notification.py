from typing import Optional, List
from pydantic import Field
from datetime import datetime
from enum import IntEnum

from schemas.base import BaseModel, ObjectIdPydantic
from schemas.invoice import InvoiceStatus


__all__ = ["NotificationType", "Notification", "NotificationInDB", "Notifications"]


class NotificationType(IntEnum):
    NEW_INVOICE = 1
    DEPOSIT = 2
    WITHDRAW = 3
    SYSTEM = 4
    CHAT_MESSAGE = 5
    INVOICE_STATUS_CHANGE = 6
    NEW_FROZEN_INVOICE = 7


class Notification(BaseModel):
    user_id: ObjectIdPydantic = Field(...)
    type: NotificationType = Field(
        ...,
        description="NEW_INVOICE = 1, DEPOSIT = 2, WITHDRAW = 3, SYSTEM = 4, CHAT_MESSAGE = 5, INVOICE_STATUS_CHANGE = 6",
    )
    watched: bool = Field(...)
    new_status: str = Field(default=None)
    participant_nickname: str = Field(default=None)
    invoice_id: ObjectIdPydantic = Field(default=None)
    system_message: str = Field(default=None)
    amount: float = Field(default=None)
    created_at: datetime = Field(default=None)
    message_text: str = Field(default=None)


class NotificationInDB(Notification):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class Notifications(BaseModel):
    notifications: List[Notification] = Field(default=[])
