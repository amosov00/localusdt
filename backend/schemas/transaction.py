from typing import Optional, Literal
from datetime import datetime
from pydantic import Field, validator
from enum import IntEnum
from decimal import Decimal


from schemas.base import BaseModel, ObjectIdPydantic

__all__ = [
    "USDTTransaction",
    "USDTTransactionInDB",
    "USDTTransactionStatus",
    "USDTTransactionEvents"
]


class USDTTransactionStatus(IntEnum):
    DONE = 1
    PENDING = 2


class USDTTransactionEvents(IntEnum):
    DEPOSIT = 1
    WITHDRAW = 2
    DEPOSIT_LOOT_TOKENS = 3
    DEPOSIT_LOOT_ETHER = 4


class USDTTransaction(BaseModel):
    date: Optional[datetime] = Field(default=None)
    to_adr: Optional[str] = Field(default=None)
    from_adr: Optional[str] = Field(default=None)
    tx_hash: Optional[str] = Field(default=None)
    event: Optional[int] = Field(default=None)
    status: Optional[USDTTransactionStatus] = Field(default=None, description="DEPOSIT = 1 WITHDRAW = 2 DEPOSIT_LOOT_TOKENS = 3 DEPOSIT_LOOT_ETHER = 3")
    usdt_amount: Optional[Decimal] = Field(default=None)
    user_id: Optional[ObjectIdPydantic] = Field(default=None)
    ether_amount: Optional[Decimal] = Field(default=None)


class USDTTransactionInDB(USDTTransaction):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
