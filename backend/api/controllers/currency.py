from fastapi import APIRouter

from database.crud.currency import CurrencyCRUD
from schemas.rate import USDTRate

__all__ = ["router"]

router = APIRouter()


@router.get("/", response_model=USDTRate)
async def get_rate():
    return await CurrencyCRUD.find_last()
