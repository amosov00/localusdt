from database.crud.base import BaseMongoCRUD


class USDTTransactionCRUD(BaseMongoCRUD):
    collection = "transaction"

    @classmethod
    async def insert_transaction(cls, tx_input: dict, tx_raw: dict):
        pass
