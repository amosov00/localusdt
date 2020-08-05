from http import HTTPStatus
from typing import List, Optional

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, Body, Response, Path

from database.crud.ads import AdsCRUD
from database.crud.user import UserCRUD
from api.dependencies import get_user
from schemas.ads import (
    AdsFilters,
    AdsCreate,
    AdsInDB,
    AdsInSearch,
    AdsType,
    Currency,
    PaymentMethod
)
from schemas.user import User

__all__ = ["router"]

router = APIRouter()


@router.post("/", response_model=AdsInDB)
async def create_ads(
    user: User = Depends(get_user), data: AdsCreate = Body(...),
):
    created_ads = await AdsCRUD.create(user, data)
    return created_ads


@router.get("/user/", response_model=List[AdsInSearch])
async def ads_fetch_users(user: User = Depends(get_user)):
    return await AdsCRUD.find_by_user_obj(user)


@router.get("/", response_model=List[AdsInSearch])
async def ads_fetch_all(
        ad_type: Optional[AdsType] = None,
        price_bot: Optional[float] = None,
        price_top: Optional[float] = None,
        currency: Optional[Currency] = Currency.RUB,
        payment_method: Optional[PaymentMethod] = None,
        limit: int = 10000
):

    filters = AdsFilters(
        type=ad_type,
        price_bot=price_bot,
        price_top=price_top,
        currency=currency,
        payment_method=payment_method,
        limit=limit
    )
    return await AdsCRUD.find_with_filters(filters)


@router.get("/{ads_id}", response_model=AdsInSearch)
async def ads_by_id(ads_id: str = Path(...)):
    ads = await AdsCRUD.find_by_id(ads_id)
    user = await UserCRUD.find_by_id(ads["user_id"])
    if not user:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "No user")
    ads["username"] = user.get("username")
    return ads
