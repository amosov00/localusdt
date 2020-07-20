from typing import Optional, List
from datetime import datetime

from pydantic import Field, validator

from enum import IntEnum
from schemas.base import BaseModel, ObjectIdPydantic

__all__ = []


class ContactStatus:
    CREATED = "created"
    WAITING = "waiting"  # Waiting 90 minutes for confirming deal
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    ALL = (CREATED, WAITING, PROCESSING, COMPLETED, CANCELLED)


class Contact(BaseModel):
    invoice_id: ObjectIdPydantic = Field(default=None)
    seller_id: ObjectIdPydantic = Field(default=None)
    buyer_id: ObjectIdPydantic = Field(default=None)
    amount_rub: float = Field(default=None)
    amount_usdt: float = Field(default=None)
    status: ContactStatus.ALL = Field(
        default=None,
        description="Status of contact: created, waiting, processing, completed, cancelled",
    )
    chat_id: ObjectIdPydantic = Field(
        default=None, description="Id for chat room between seller and buyer"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, description="UTC")
    finished_at: Optional[datetime] = Field(
        default=None, description="Update when user close invoice"
    )


class ContactInDB(Contact):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")