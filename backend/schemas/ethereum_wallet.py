from typing import Optional
from pydantic import Field
from decimal import Decimal

from schemas.base import BaseModel

__all__ = [
    "EthereumWallet"
]


class EthereumWallet(BaseModel):
    eth_address: Optional[str] = Field(default=None)
    contract_balance: Optional[Decimal] = Field(default=None)
