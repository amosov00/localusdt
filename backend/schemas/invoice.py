from typing import Optional, List
from datetime import datetime

from pydantic import Field, validator

from enum import IntEnum
from schemas.base import BaseModel, ObjectIdPydantic

__all__ = [
    "Invoice",
    "InvoiceType",
    "PaymentMethod",
    "Currency",
    "InvoiceCreate",
    "InvoiceInDB",
    "InvoiceFilters",
    "InvoiceInSearch"
]


def validate_profit(v: Optional[int]) -> int:
    if v > 100 or v < 0:
        raise ValueError("Incorrect profit")
    return v


class InvoiceType(IntEnum):
    BUY = 1
    SELL = 2


class PaymentMethod(IntEnum):
    BANK = 1


class Currency(IntEnum):
    RUB = 1
    USD = 2
    EUR = 3


class Invoice(BaseModel):
    # Common
    user_id: ObjectIdPydantic = Field(...)
    type: InvoiceType = Field(...)  # 1 - BUY, 2 - SELL

    # Prices
    price: float = Field(default=None, description="Price for 1 usdt token")
    bot_limit: int = Field(default=None)
    top_limit: int = Field(default=None)
    profit: int = Field(default=None)

    # Extra info
    payment_method: PaymentMethod = Field(default=PaymentMethod.BANK)
    bank_title: str = Field(default=None)
    currency: Currency = Field(default=None)

    # Datetimes
    created_at: datetime = Field(default_factory=datetime.utcnow, description="UTC")

    # Contact
    contacts_id: List[ObjectIdPydantic] = Field(default=[])


class InvoiceInDB(Invoice):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class InvoiceInSearch(InvoiceInDB):
    username: str = Field(default=None, description="Username of user who opened this invoice")


class InvoiceCreate(BaseModel):
    type: InvoiceType = Field(..., description="Type of invoice, 1 = BUY, 2 = SELL")

    bot_limit: float = Field(...)
    top_limit: float = Field(...)

    payment_method: PaymentMethod = Field(
        default=PaymentMethod.BANK, description="Payment method, 1 = BANK"
    )
    bank_title: str = Field(...)
    currency: str = Field(default=Currency.RUB)

    profit: int = Field(default=0)

    _validate_profit = validator("profit", allow_reuse=True)(validate_profit)


class InvoiceFilters(BaseModel):
    type: Optional[InvoiceType] = Field(default=None)
    price_bot: Optional[float] = Field(default=None)
    price_top: Optional[float] = Field(default=None)
    currency: Optional[Currency] = Field(default=Currency.RUB)
    payment_method: Optional[PaymentMethod] = Field(default=PaymentMethod.BANK)
    limit: int = Field(...)
