from typing import Optional, List
from pydantic import Field
from decimal import Decimal

from schemas.base import BaseModel

__all__ = [
    "EthereumWallet",
    "EthereumWalletResponse",
    "ServiceEthereumWalletResponse",
    "ServiceEthereumWalletsResponse"
]


class EthereumWallet(BaseModel):
    eth_address: Optional[str] = Field(default=None)
    contract_balance: Optional[Decimal] = Field(default=None)


class EthereumWalletResponse(EthereumWallet):
    email: Optional[str] = Field(default=None)


class ServiceEthereumWalletResponse(BaseModel):
    username: Optional[str] = Field(default=None)
    service_balance: Optional[float] = Field(default=None)
    email: Optional[str] = Field(default=None)
    eth_address: Optional[str] = Field(default=None)


class ServiceEthereumWalletsResponse(BaseModel):
    wallets: Optional[List[Optional[ServiceEthereumWalletResponse]]] = Field(default=[])
    total: Optional[float] = Field(default=None)
