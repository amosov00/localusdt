from typing import Optional, List
from datetime import datetime

from pydantic import Field, validator

from enum import IntEnum
from schemas.base import BaseModel, ObjectIdPydantic

__all__ = [
    "Ads",
    "AdsType",
    "PaymentMethod",
    "Currency",
    "AdsCreate",
    "AdsInDB",
    "AdsFilters",
    "AdsInSearch",
    "AdsSort"
]


def validate_profit(v: Optional[int]) -> int:
    if v > 100 or v < 0:
        raise ValueError("Incorrect profit")
    return v


class AdsType(IntEnum):
    BUY = 1
    SELL = 2


class PaymentMethod(IntEnum):
    SBERBANK = 1
    TINKOFF = 2
    ALFA_BANK = 3
    OTHER = 4


class Currency(IntEnum):
    RUB = 1
    USD = 2
    EUR = 3


class Ads(BaseModel):
    # Common
    user_id: ObjectIdPydantic = Field(...)
    type: AdsType = Field(...)  # 1 - BUY, 2 - SELL
    amount_usdt: float = Field(defaul=None)

    # Prices
    price: float = Field(default=None, description="Price for 1 usdt token")
    bot_limit: int = Field(default=None)
    top_limit: int = Field(default=None)
    profit: int = Field(default=None)

    # Extra info
    payment_method: PaymentMethod = Field(default=None)
    other_payment_method: str = Field(default=None)
    currency: Currency = Field(default=None)
    condition: str = Field(default=None, description="Condition of the Ads")

    # Datetimes
    created_at: datetime = Field(default_factory=datetime.utcnow, description="UTC")

    # Contact
    contacts_id: List[ObjectIdPydantic] = Field(default=[])


class AdsInDB(Ads):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class AdsInSearch(AdsInDB):
    username: str = Field(default=None, description="Username of user who opened this Ads")


class AdsCreate(BaseModel):
    type: AdsType = Field(..., description="Type of Ads, 1 = BUY, 2 = SELL")

    bot_limit: float = Field(...)
    top_limit: float = Field(...)

    amount_usdt: float = Field(...)

    payment_method: PaymentMethod = Field(
        default=PaymentMethod.SBERBANK,
        description="Payment method, 1 = Sberbank, 2 = Tinkoff, 3 = Alfa-bank, 4 = Other"
    )
    other_payment_method: str = Field(default=None)
    currency: str = Field(default=Currency.RUB)
    condition: str = Field(default="", description="Condition of the Ads")

    profit: int = Field(default=0)

    _validate_profit = validator("profit", allow_reuse=True)(validate_profit)


class AdsSort(IntEnum):
    ASC = 1
    DESC = -1


class AdsFilters(BaseModel):
    type: Optional[AdsType] = Field(default=None)
    price_bot: Optional[float] = Field(default=None)
    price_top: Optional[float] = Field(default=None)
    currency: Optional[Currency] = Field(default=Currency.RUB)
    payment_method: Optional[PaymentMethod] = Field(default=PaymentMethod.SBERBANK)
    sort: Optional[AdsSort] = Field(default=AdsSort.ASC)
    limit: int = Field(...)
