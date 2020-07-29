from typing import Optional, Union, List
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException
from http import HTTPStatus


from database.crud.base import BaseMongoCRUD
from database.crud import UserCRUD, CurrencyCRUD
from core.utils import to_objectid
from schemas.ads import (
    Ads,
    AdsCreate,
    AdsType,
    AdsFilters
)
from schemas.user import (
    User,
)


__all__ = ["AdsCRUD"]


class AdsCRUD(BaseMongoCRUD):
    collection: str = "ads"

    @classmethod
    async def find_by_id(cls, _id: str) -> Optional[dict]:
        return await super().find_one(query={"_id": to_objectid(_id)}) if _id else None

    @classmethod
    async def find_by_email(cls, email: str) -> Optional[dict]:
        return await super().find_one(query={"email": email}) if email else None

    @classmethod
    async def find_by_user_id(cls, user_id: str) -> Optional[dict]:
        return (
            await super().find_many(query={"user_id": ObjectId(user_id)}) if user_id else None
        )

    @classmethod
    async def find_by_user_obj(cls, user: User) -> Optional[List[dict]]:
        result = await cls.find_many(query={"user_id": user.id})
        for ads in result:
            ads["username"] = user.username
        return result

    @classmethod
    async def create(cls, user: User, payload: AdsCreate):
        if payload.amount_usdt > user.balance_usdt:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Not enough usdt on your account.")
        else:
            user.balance_usdt -= payload.amount_usdt
            await UserCRUD.update_one(query={"_id": user.id}, payload={"balance_usdt": user.balance_usdt})
        # Money check and transfer to ads

        ads = Ads(
            **payload.dict(),
            user_id=user.id,
            created_at=datetime.now()
        )
        current_rate = (await CurrencyCRUD.find_last())["current_rate"]
        if not current_rate:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Can't get currency rate.")
        ads.price = current_rate * (float(ads.profit) / 100. + 1.)
        inserted_id = (
            await cls.insert_one(payload={
                **ads.dict(),
            })
        ).inserted_id

        ads_in_db = await cls.find_one(query={"_id": inserted_id})
        return ads_in_db

    @classmethod
    async def find_with_filters(cls, filters: AdsFilters):
        query = {
            "currency": filters.currency,
            "payment_method": filters.payment_method
        }
        if filters.type:
            query["type"] = filters.type
        if filters.price_bot:
            query["price"] = {"$gte": filters.price_bot}
        if filters.price_top:
            if not query.get("price"):
                query["price"] = {"$lte": filters.price_top}
            else:
                query["price"]["$lte"] = filters.price_top
        result = await cls.find_many(query=query, limit=filters.limit)
        users = await UserCRUD.find_many(query={})
        users_kw = {}
        for user in users:
            if user.get("username"):
                users_kw[user["_id"]] = user["username"]
        for ads in result:
            ads["username"] = users_kw[ads["user_id"]]
        return result
