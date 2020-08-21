from typing import List

from database.crud.base import BaseMongoCRUD
from schemas.transaction import USDTTransactionInDB


class USDTTransactionCRUD(BaseMongoCRUD):
    collection = "transaction"

    @classmethod
    async def get_transactions_by_address(cls, eth_address: str) -> List[dict]:
        return await cls.find_many(query={
            "$or": [
                {"to_adr": eth_address},
                {"from_adr": eth_address},
            ]
        })
