from database.crud.base import BaseMongoCRUD
from bson import Decimal128


__all__ = [
    "EthereumWalletCRUD"
]


class EthereumWalletCRUD(BaseMongoCRUD):
    collection = "ethwallet"

    @classmethod
    async def create_wallet(cls, eth_wallet: str, private_key: str, entropy: str) -> None:
        await cls.insert_one(payload={
            "eth_address": eth_wallet,
            "private_key": private_key,
            "entropy": entropy,
            "contract_balance": Decimal128(str(0))
        })