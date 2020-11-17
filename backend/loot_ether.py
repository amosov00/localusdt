import asyncio

from core.integrations.crypto import USDTWrapper

asyncio.get_event_loop().run_until_complete(USDTWrapper().loot_eth_from_wallets())
