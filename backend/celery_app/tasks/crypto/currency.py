import logging
from core.utils.binance import Currency
from database.crud import CurrencyCRUD, AdsCRUD
from schemas.currency import CurrencyType

from celery_app.celeryconfig import app

__all__ = ["update_currency_rate"]


@app.task(name="update_currency_rate", bind=True, soft_time_limit=42, time_limit=300)
async def update_currency_rate(self, *args, **kwargs):
    obj = Currency()
    current_rate_rub = await obj.get_tether_rate_rub()
    current_rate_byn = await obj.get_tether_rate_byn()
    current_rate_usd = await obj.get_tether_rate_usd()
    current_rate_eur = await obj.get_tether_rate_eur()
    logging.info(f"Starting updating usdt rate from binance/nbrb")
    await CurrencyCRUD.update(CurrencyType.BYN, current_rate_byn)
    await CurrencyCRUD.update(CurrencyType.RUB, current_rate_rub)
    await CurrencyCRUD.update(CurrencyType.USD, current_rate_usd)
    await CurrencyCRUD.update(CurrencyType.EUR, current_rate_eur)
    if current_rate_rub:
        await AdsCRUD.update_currency(currency_type=CurrencyType.RUB, currency_value=current_rate_rub)
    if current_rate_byn:
        await AdsCRUD.update_currency(currency_type=CurrencyType.BYN, currency_value=current_rate_byn)
    if current_rate_eur:
        await AdsCRUD.update_currency(currency_type=CurrencyType.EUR, currency_value=current_rate_eur)
    if current_rate_usd:
        await AdsCRUD.update_currency(currency_type=CurrencyType.USD, currency_value=current_rate_usd)
    return True
