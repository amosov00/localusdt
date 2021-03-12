from typing import Optional, List
from datetime import datetime

from pydantic import Field, validator

from enum import IntEnum
from schemas.base import BaseModel, ObjectIdPydantic
from schemas.currency import CurrencyType

__all__ = [
    "Ads",
    "AdsType",
    "PaymentMethod",
    "AdsCreate",
    "AdsInDB",
    "AdsFilters",
    "AdsInSearch",
    "AdsSort",
    "AdsStatuses",
    "AdsUpdate"
]


def validate_profit(v: Optional[float]) -> float:
    if v > 100.0 or v < -100.0:
        raise ValueError("Incorrect profit")
    return v


def validate_amount(v: Optional[float]) -> float:
    if v <= 0:
        raise ValueError("Incorrect amount")
    return v


class AdsType(IntEnum):
    BUY = 1
    SELL = 2


class PaymentMethod(IntEnum):
    SBERBANK = 1
    TINKOFF = 2
    ALFA_BANK = 3
    OTHER = 4
    ALL = 5
    CARD_TO_CARD = 6
    QIWI = 7
    YANDEX_MONEY = 8
    PAYEER = 9
    PAYPAL = 10
    WEBMONEY = 11
    CASH = 12


class AdsStatuses(IntEnum):
    ACTIVE = 1
    NOT_ACTIVE = 2
    DELETED = 3


class Ads(BaseModel):
    # Common
    user_id: ObjectIdPydantic = Field(...)
    type: AdsType = Field(...)  # 1 - BUY, 2 - SELL
    amount_usdt: float = Field(defaul=None)
    status: AdsStatuses = Field(default=None, description="1 - ACTIVE, 2 - NOT_ACTIVE, 3 - DELETED")

    # Prices
    fixed_price: bool = Field(default=None, description="If true - show price_field, else - show profit field")
    price: float = Field(default=None, description="Price for 1 usdt token")
    bot_limit: int = Field(default=None)
    top_limit: int = Field(default=None)
    profit: float = Field(default=None)

    # Extra info
    payment_method: PaymentMethod = Field(default=None)
    other_payment_method: str = Field(default=None)
    currency: CurrencyType = Field(default=None, description="1 -- RUB, 2 -- BYN, 3 -- USD, 4 -- EUR")
    condition: str = Field(default=None, description="Condition of the Ads")

    # Datetimes
    created_at: datetime = Field(default_factory=datetime.utcnow, description="UTC")
    expiration_timestamp: int = Field(default=None, description="Timestamp delta of expiration")

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

    #TODO: remove expiration at all
    expiration_timestamp: int = Field(default=24*365*3600, description="Timestamp delta of expiration")

    fixed_price: bool = Field(default=False, description="If true - show price_field, else - show profit field")
    price: float = Field(default=None)

    payment_method: PaymentMethod = Field(
        default=PaymentMethod.SBERBANK,
        description="Payment method, 1 = Sberbank, 2 = Tinkoff, 3 = Alfa-bank, 4 = Other"
    )
    other_payment_method: str = Field(default=None)
    currency: CurrencyType = Field(default=CurrencyType.RUB, description='1 -- RUB, 2 -- BYN, 3 -- USD, 4 -- EUR')
    condition: str = Field(default="", description="Condition of the Ads")

    profit: float = Field(default=0)

    _validate_profit = validator("profit", allow_reuse=True)(validate_profit)
    _validate_amount = validator("amount_usdt", allow_reuse=True)(validate_amount)


class AdsUpdate(BaseModel):
    amount_usdt: float = Field(default=None)

    bot_limit: float = Field(default=None)
    top_limit: float = Field(default=None)

    payment_method: PaymentMethod = Field(
        default=None,
        description="Payment method, 1 = Sberbank, 2 = Tinkoff, 3 = Alfa-bank, 4 = Other"
    )
    other_payment_method: str = Field(default=None)

    condition: str = Field(default=None, description="Condition of the Ads")

    expiration_timestamp: int = Field(default=None, description="Timestamp delta of expiration")

    profit: float = Field(default=None)

    fixed_price: bool = Field(default=None, description="If true - show price_field, else - show profit field")
    price: float = Field(default=None)

    _validate_profit = validator("profit", allow_reuse=True)(validate_profit)
    _validate_amount = validator("amount_usdt", allow_reuse=True)(validate_amount)


class AdsSort(IntEnum):
    ASC = 1
    DESC = -1


class AdsFilters(BaseModel):
    type: Optional[AdsType] = Field(default=None)
    price_bot: Optional[float] = Field(default=None)
    price_top: Optional[float] = Field(default=None)
    currency: Optional[CurrencyType] = Field(default=CurrencyType.RUB)
    payment_method: Optional[PaymentMethod] = Field(default=PaymentMethod.SBERBANK)
    sort: Optional[AdsSort] = Field(default=AdsSort.ASC)
    limit: int = Field(...)
