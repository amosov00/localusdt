from typing import Optional, Literal
from datetime import datetime
from pydantic import Field, validator
from enum import IntEnum
from decimal import Decimal


from schemas.base import BaseModel, ObjectIdPydantic

__all__ = [
    "USDTTransaction",
    "USDTTransactionInDB"
]


class USDTTransaction(BaseModel):
    to_adr: str = Field(...)
    from_adr: str = Field(...)
    tx_hash: str = Field(...)
    usdt_amount: Decimal = Field(...)


class USDTTransactionInDB(USDTTransaction):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
