from typing import Optional, List
from pydantic import Field
from decimal import Decimal

from schemas.base import BaseModel


__all__ = [
    "DepositStatistic",
    "AccountWalletInfo",
    "AccountWalletInfos"
]


class DepositStatistic(BaseModel):
    total_withdraw_pending: Decimal = Field(default=None)
    total_withdraw_done: Decimal = Field(default=None)
    total_withdraw: Decimal = Field(default=None)
    total_on_wallets: Decimal = Field(default=None)
    total_on_hot_wallet: Decimal = Field(default=None)
    total_active: Decimal = Field(default=None)
    total: Decimal = Field(default=None)


class AccountWalletInfo(BaseModel):
    email: Optional[str] = Field(default=None)
    eth_address: Optional[str] = Field(default=None)
    private_key: Optional[str] = Field(default=None)
    amount_usdt: Optional[Decimal] = Field(default=None)
    amount_eth: Optional[Decimal] = Field(default=None)


class AccountWalletInfos(BaseModel):
    accounts: List[AccountWalletInfo] = Field(default=[])
