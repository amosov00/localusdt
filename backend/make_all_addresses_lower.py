import asyncio

from database.crud.ethereum_wallet import EthereumWalletCRUD
from database.crud.user import UserCRUD


async def make_all_addresses_lower():
    addresses = await EthereumWalletCRUD.find_many({})
    for address in addresses:
        await EthereumWalletCRUD.update_one(query={
            "_id": address.get("_id")
        },
            payload={"eth_address": address.get("eth_address").lower()}
        )
    users = await UserCRUD.find_many({})
    for user in users:
        if user.get("eth_address"):
            await UserCRUD.update_one(query={
                "_id": user.get("_id")
            },
                payload={"eth_address": user.get("eth_address").lower()}
            )


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(make_all_addresses_lower())
