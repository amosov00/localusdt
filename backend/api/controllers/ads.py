from http import HTTPStatus
from typing import List, Optional

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, Body, Response, Path

from database.crud.ads import AdsCRUD
from database.crud.user import UserCRUD
from api.dependencies import get_user, user_not_banned
from schemas.ads import (
    AdsFilters,
    AdsCreate,
    AdsInDB,
    AdsInSearch,
    AdsType,
    Currency,
    PaymentMethod,
    AdsSort,
    AdsStatuses,
    AdsUpdate
)
from schemas.user import User

__all__ = ["router"]

router = APIRouter()


@router.post("/", response_model=AdsInDB)
async def create_ads(
    user: User = Depends(user_not_banned), data: AdsCreate = Body(...),
):
    created_ads = await AdsCRUD.create(user, data)
    return created_ads


@router.get("/user/", response_model=List[AdsInSearch])
async def ads_fetch_users(user: User = Depends(get_user)):
    return await AdsCRUD.find_by_user_obj(user)


@router.get("/", response_model=List[AdsInSearch])
async def ads_fetch_all(
        order_type: Optional[AdsType] = None,
        price_bot: Optional[float] = None,
        price_top: Optional[float] = None,
        currency: Optional[Currency] = Currency.RUB,
        payment_method: Optional[PaymentMethod] = None,
        sort: Optional[AdsSort] = AdsSort.ASC,
        limit: int = 10000
):

    filters = AdsFilters(
        type=order_type,
        price_bot=price_bot,
        price_top=price_top,
        currency=currency,
        payment_method=payment_method,
        sort=sort,
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


@router.put("/{ads_id}/off/")
async def off_order(user: User = Depends(user_not_banned), ads_id: str = Path(...)):
    return await AdsCRUD.set_status_safe(user, ads_id, AdsStatuses.NOT_ACTIVE)


@router.put("/{ads_id}/on/")
async def on_order(user: User = Depends(user_not_banned), ads_id: str = Path(...)):
    return await AdsCRUD.set_status_safe(user, ads_id, AdsStatuses.ACTIVE)


@router.put("/{ads_id}/delete/")
async def delete_order(user: User = Depends(user_not_banned), ads_id: str = Path(...)):
    return await AdsCRUD.set_status_safe(user, ads_id, AdsStatuses.DELETED)


@router.put("/{ads_id}/update/", response_model=AdsInSearch)
async def update_order(
        user: User = Depends(user_not_banned),
        ads_id: str = Path(...),
        payload: AdsUpdate = Body(...)):
    return await AdsCRUD.update_ads(user, ads_id, payload)
