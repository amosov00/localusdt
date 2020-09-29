from datetime import datetime
from bson import Decimal128

from celery_app.celeryconfig import app
from core.integrations.crypto import USDTWrapper
from database.crud import UserCRUD, USDTTransactionCRUD, EthereumWalletCRUD
from config import LOCALUSDT_FEE


__all__ = ["loot_tokens"]


@app.task(name="loot_tokens", bind=True, soft_time_limit=60, time_limit=400)
async def loot_tokens(self, *args, **kwargs):
    print(f"Looting deposits starts at {datetime.now()}")
    wallets = await EthereumWalletCRUD.find_many({})
    target_wallets = []
    for wallet in wallets:
        if int(wallet.get("contract_balance").to_decimal()) > LOCALUSDT_FEE * 10**6:
            target_wallets.append(wallet)
    print(target_wallets)
    wallets_to_send = await USDTWrapper().transfer_from_deposits(target_wallets)
    print(wallets_to_send)
    await USDTWrapper().send_gas_to_addresses(wallets_to_send)

    print(f"Looting deposits ends at {datetime.now()}")