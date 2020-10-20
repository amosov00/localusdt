from typing import Optional
from pydantic import Field
from enum import IntEnum
from datetime import datetime

from .base import BaseModel


__all__ = [
    "CurrencyType",
    "Currency"
]


class CurrencyType(IntEnum):
    RUB = 1
    BYN = 2


class Currency(BaseModel):
    type: CurrencyType = Field(..., description="1 -- RUB, 2 -- BYN")
    current_rate: float = Field(...)
    updated_at: Optional[datetime] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
