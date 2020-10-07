from pydantic import Field
from decimal import Decimal

from schemas.base import BaseModel


__all__ = [
    "DepositStatistic"
]


class DepositStatistic(BaseModel):
    total_withdraw_pending: Decimal = Field(default=None)
    total_withdraw_done: Decimal = Field(default=None)
    total_withdraw: Decimal = Field(default=None)
    total_on_wallets: Decimal = Field(default=None)
    total_on_hot_wallet: Decimal = Field(default=None)
    total_active: Decimal = Field(default=None)
    total: Decimal = Field(default=None)
