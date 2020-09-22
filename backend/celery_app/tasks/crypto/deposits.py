from datetime import datetime
from bson import Decimal128

from core.mechanics.notification_manager import NotificationSender
from core.mechanics.notification_manager import notification_manager
from celery_app.celeryconfig import app
from core.integrations.crypto import USDTWrapper
from database.crud import UserCRUD, USDTTransactionCRUD
from config import LAST_BLOCKS_TO_PARSE


__all__ = ["check_deposits"]


@app.task(name="check_deposits", bind=True, soft_time_limit=46, time_limit=300)
async def check_deposits(self, *args, **kwargs):
    await notification_manager.init_manager()
    print(f"Parsing blocks and updating users balance starts at {datetime.now()}")
    users = await UserCRUD.find_many({})
    user_kw = {}
    for user in users:
        if user.get("eth_address"):
            user_kw[user.get("eth_address").lower()] = user
    transactions = await USDTWrapper().parse_last_blocks(LAST_BLOCKS_TO_PARSE)
    transactions_to_insert = []
    for transaction in transactions:
        if transaction.get("to_adr").lower() in user_kw:
            user: dict = user_kw.get(transaction.get("to_adr").lower())
            if transaction.get("to_adr").lower() == user.get("eth_address").lower():
                new_balance = float(
                    (user.get("balance_usdt") if user.get("balance_usdt") else 0.0)
                    + float(transaction.get("usdt_amount")) * 0.000001
                )
                await UserCRUD.update_one(
                    query={"_id": user.get("_id")},
                    payload={"balance_usdt": new_balance},
                )
                await NotificationSender.send_deposit_notification(
                    user.get("_id"),
                    amount=float(transaction.get("usdt_amount")) * 0.000001
                )
                transaction["usdt_amount"] = Decimal128(transaction.get("usdt_amount"))
                transaction["date"] = datetime.utcnow()
                transaction["event"] = 1
                transactions_to_insert.append(transaction)
    if transactions_to_insert:
        await USDTTransactionCRUD.insert_many(payload=transactions_to_insert)
    print(f"Parsing blocks and updating users balance finished at {datetime.now()}")
    return True
