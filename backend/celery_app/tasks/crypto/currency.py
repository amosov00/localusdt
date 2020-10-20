import logging
from core.utils.binance import Currency
from database.crud import CurrencyCRUD, AdsCRUD
from schemas.currency import CurrencyType

from celery_app.celeryconfig import app

__all__ = ["update_usdt_rate"]


@app.task(name="update_usdt_rate", bind=True, soft_time_limit=42, time_limit=300)
async def update_usdt_rate(self, *args, **kwargs):
    obj = Currency()
    current_rate_rub = await obj.get_tether_rate_rub()
    current_rate_byn = await obj.get_tether_rate_byn()
    logging.info(f"Starting updating usdt rate from binance/nbrb {current_rate_rub} and {current_rate_byn}")
    await CurrencyCRUD.update(CurrencyType.BYN, current_rate_byn)
    await CurrencyCRUD.update(CurrencyType.RUB, current_rate_rub)
    if current_rate_rub:
        await AdsCRUD.db[AdsCRUD.collection].update_many(
            {
                "fixed_price": False,
                "currency": CurrencyType.RUB
            },
            [  # noqa
                {
                    "$set": {
                        "price": {
                            "$trunc": [{
                                "$multiply": [
                                    {"$add": [{"$multiply": ["$profit", 0.01]}, 1]},
                                    current_rate_rub,
                                ]},
                                2]
                            }
                        }
                    }
            ],
        )
    if current_rate_byn:
        await AdsCRUD.db[AdsCRUD.collection].update_many(
            {
                "fixed_price": False,
                "currency": CurrencyType.BYN
            },
            [  # noqa
                {
                    "$set": {
                        "price": {
                            "$trunc": [{
                                "$multiply": [
                                    {"$add": [{"$multiply": ["$profit", 0.01]}, 1]},
                                    current_rate_byn,
                                ]},
                                2]
                        }
                    }
                }
            ],
        )
    return True
