from http import HTTPStatus
from typing import List

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, Body, Response

from database.crud.ads import AdsCRUD
from api.dependencies import get_user
from schemas.ads import (
    AdsFilters,
    AdsCreate,
    AdsInDB,
    AdsInSearch
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
async def ads_fetch_all(filters: AdsFilters = Body(...)):
    return await AdsCRUD.find_with_filters(filters)

