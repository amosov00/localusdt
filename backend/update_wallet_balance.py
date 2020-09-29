import asyncio

from database.crud.ethereum_wallet import EthereumWalletCRUD
from core.integrations.crypto import USDTWrapper
from bson import Decimal128


async def update_wallet_balance():
    addresses = await EthereumWalletCRUD.find_many({})
    for address in addresses:
        adr = USDTWrapper().w3.toChecksumAddress(address.get("eth_address").lower())
        balance = Decimal128(str(await USDTWrapper()._get_balance_contract(adr)))
        await EthereumWalletCRUD.update_one(query={
            "_id": address.get("_id")
        },
            payload={"contract_balance": balance}
        )


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(update_wallet_balance())
