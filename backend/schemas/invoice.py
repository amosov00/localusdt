from typing import Optional, Literal
from datetime import datetime

from pydantic import Field, validator

from enum import IntEnum
from schemas.base import BaseModel, ObjectIdPydantic

__all__ = [
    "Invoice",
    "InvoiceInDB",
    "InvoiceStatus",
    "InvoiceCreate"
]


class InvoiceStatus:
    WAITING_FOR_PAYMENT = "waiting_for_payment"  # Waiting 90 minutes for bank payment
    APPROVED = "approved"
    WAITING_FOR_TOKENS = "waiting_for_tokens"  # Waiting 30 minutes for token
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    ALL = (WAITING_FOR_PAYMENT, WAITING_FOR_TOKENS, COMPLETED, CANCELLED, APPROVED)


class Invoice(BaseModel):
    ads_id: ObjectIdPydantic = Field(...)
    seller_id: ObjectIdPydantic = Field(...)
    buyer_id: ObjectIdPydantic = Field(...)
    amount_rub: float = Field(default=None)
    amount_usdt: float = Field(...)
    status: Literal[InvoiceStatus.ALL] = Field( # noqa
        ...,
        description="Status of Invoice: created, waiting, processing, completed, cancelled",
    )
    chat_id: ObjectIdPydantic = Field(
        default=None, description="Id for chat room between seller and buyer"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, description="UTC")
    status_changed_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC, Timer start after status change"
    )
    finished_at: Optional[datetime] = Field(
        default=None, description="Update when user close Invoice"
    )


class InvoiceInDB(Invoice):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class InvoiceCreate(BaseModel):
    ads_id: ObjectIdPydantic = Field(...)
    amount_usdt: float = Field(...)
