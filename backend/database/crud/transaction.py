from typing import List

from database.crud.base import BaseMongoCRUD
from schemas.user import User
from schemas.transaction import USDTTransactionInDB, USDTTransactionStatus


class USDTTransactionCRUD(BaseMongoCRUD):
    collection = "transaction"

    @classmethod
    async def get_transactions_by_address(cls, user: User) -> List[dict]:
        return await cls.find_many(query={
            "$or": [
                {"to_adr": user.eth_address},
                {"from_adr": user.eth_address},
                {"user_id": user.id}
            ]
        })

    @classmethod
    async def approve_withdraw(cls, tx_hash: str) -> None:
        await cls.update_one(
            query={
                "tx_hash": tx_hash
            },
            payload={
                "status": USDTTransactionStatus.DONE
            }
        )
