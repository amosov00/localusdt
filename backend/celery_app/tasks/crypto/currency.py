import logging
from core.utils.binance import BinanceRate
from database.crud import CurrencyCRUD
import os

from celery_app.celeryconfig import app

__all__ = ["update_usdt_rate"]


@app.task(
    name="update_usdt_rate", bind=True, soft_time_limit=42, time_limit=300
)
async def update_usdt_rate(self, *args, **kwargs):
    obj = BinanceRate()
    current_rate = await obj.get_tether_rate()
    logging.info(f"Starting updating usdt rate from binance {current_rate}")
    await CurrencyCRUD.update(current_rate)
    return True
