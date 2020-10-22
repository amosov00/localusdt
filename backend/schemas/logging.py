from enum import IntEnum
from pydantic import Field
from datetime import datetime
from typing import Optional, List

from schemas.base import BaseModel, ObjectIdPydantic

__all__ = [
    "LogEvents",
    "Log",
    "LogInDB",
]


class LogEvents:
    CREATE_ADS = "create_ads"
    CHANGE_ADS = "change_ads"
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    START_INVOICE = "start_invoice"
    APPROVE_INVOICE = "approve_invoice"
    TRANSFER_TOKENS = "transfer_tokens"
    CANCEL_INVOICE = "cancel_invoice"

    INVOICE = (START_INVOICE, APPROVE_INVOICE, TRANSFER_TOKENS, CANCEL_INVOICE)
    ADS = (CREATE_ADS, CHANGE_ADS)
    CRYPTO = (DEPOSIT, WITHDRAW)


class Log(BaseModel):
    event: str = Field(default=None, description="Log events in trello =)")
    user_id: ObjectIdPydantic = Field(default=None, description="User who done this")
    invoice_id: ObjectIdPydantic = Field(default=None, description="Invoice id")
    ads_id: ObjectIdPydantic = Field(default=None)
    tx_hash: str = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LogInDB(Log):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
