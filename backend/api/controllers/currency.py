from fastapi import APIRouter
from typing import Optional

from database.crud.currency import CurrencyCRUD
from schemas.currency import Currency, CurrencyType

__all__ = ["router"]

router = APIRouter()


@router.get("/", response_model=Currency)
async def get_rate(currency: Optional[CurrencyType] = CurrencyType.RUB):
    return await CurrencyCRUD.find_last(currency)
