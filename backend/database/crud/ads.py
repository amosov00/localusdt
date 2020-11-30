from typing import Optional, Union, List
from bson import ObjectId
from fastapi import HTTPException
from http import HTTPStatus

from core.mechanics import AdsMechanics
from database.crud.base import BaseMongoCRUD
from database.crud import UserCRUD, CurrencyCRUD
from schemas.ads import (
    AdsCreate,
    AdsFilters,
    AdsStatuses,
    AdsType,
    AdsUpdate
)
from schemas.currency import CurrencyType
from schemas.user import (
    User,
)


__all__ = ["AdsCRUD"]


class AdsCRUD(BaseMongoCRUD):
    collection: str = "ads"

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
        result = await cls.find_many(query={
            "$or": [
                {
                    "status": AdsStatuses.ACTIVE,
                    "user_id": user.id,
                },
                {
                    "status": AdsStatuses.NOT_ACTIVE,
                    "user_id": user.id
                },
            ]
        })
        for ads in result:
            ads["username"] = user.username
        return result

    @classmethod
    async def create(cls, user: User, payload: AdsCreate):
        ads = await AdsMechanics().get_created_ads(
            payload,
            user
        )
        current_rate = (await CurrencyCRUD.find_last(payload.currency))["current_rate"]
        if not current_rate:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Can't get currency rate.")

        if ads.fixed_price is True and ads.price is None:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Enter price")
        elif ads.fixed_price is False:
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
            "status": AdsStatuses.ACTIVE,
            "amount_usdt": {"$gt": 0.0}
        }
        if filters.currency:
            query["currency"] = filters.currency

        if filters.payment_method:
            query["payment_method"] = filters.payment_method
        if filters.type:
            query["type"] = filters.type
        if filters.price_bot:
            query["price"] = {"$gte": filters.price_bot}
        if filters.price_top:
            if not query.get("price"):
                query["price"] = {"$lte": filters.price_top}
            else:
                query["price"]["$lte"] = filters.price_top
        result = await cls.find_many(query=query, limit=filters.limit, sort=[("price", filters.sort)])
        users = await UserCRUD.find_many(query={})
        users_kw = {}
        for user in users:
            if user.get("username"):
                users_kw[user["_id"]] = user["username"]
        for ads in result:
            ads["username"] = users_kw[ads["user_id"]]
        return result

    @classmethod
    async def get_ads(cls, user: User, ads_id: str):
        ads = await cls.find_by_id(ads_id)
        if ads["user_id"] != user.id:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Cannot get order")

        return ads

    @classmethod
    async def set_status_safe(cls, user: User, ads_id: str, status: AdsStatuses):
        ads = await cls.find_by_id(ads_id)
        if ads["user_id"] != user.id:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Cannot get order")
        if ads["status"] == status:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Order already has that status")

        if status == AdsStatuses.DELETED and ads["type"] == AdsType.SELL:
            await UserCRUD.update_one(
                query={"_id": user.id},
                payload={
                    "balance_usdt": user.balance_usdt + ads["amount_usdt"],
                    "usdt_in_invoices": user.usdt_in_invoices - ads["amount_usdt"]
                }
            )

        await cls.update_one(
            query={"_id": ads["_id"]},
            payload={"status": status}
        )
        return True

    @classmethod
    async def set_status_not_safe(cls, ads_id: str, status: AdsStatuses):
        ads = await cls.find_by_id(ads_id)
        if status == AdsStatuses.DELETED and ads["type"] == AdsType.SELL:
            user = await UserCRUD.find_by_id(ads["user_id"])
            await UserCRUD.update_one(
                query={"_id": ads["user_id"]},
                payload={
                    "balance_usdt": user["balance_usdt"] + ads["amount_usdt"],
                    "usdt_in_invoices": user["usdt_in_invoices"] - ads["amount_usdt"]
                }
            )
        await cls.update_one(
            query={"_id": ads["_id"]},
            payload={"status": status}
        )
        return True

    @classmethod
    async def update_ads(cls, user: User, ads_id: str, payload: AdsUpdate):
        ads = await cls.find_by_id(ads_id)

        ads_bot_limit = payload.bot_limit if payload.bot_limit else ads.get("bot_limit")
        ads_top_limit = payload.top_limit if payload.top_limit else ads.get("top_limit")

        if payload.amount_usdt:
            delta = payload.amount_usdt - ads["amount_usdt"]
            if user.balance_usdt < delta:
                raise HTTPException(HTTPStatus.BAD_REQUEST, "Not enough money")
            await UserCRUD.update_one(query={"_id": user.id}, payload={
                "balance_usdt": user.balance_usdt - delta,
                "usdt_in_invoices": user.usdt_in_invoices + delta
            })

        if ads_bot_limit > ads_top_limit:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Incorrect limits")

        if user.id != ads["user_id"] or \
                (ads["status"] != AdsStatuses.ACTIVE and ads["status"] != AdsStatuses.NOT_ACTIVE):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Cannot get order")

        current_rate = (await CurrencyCRUD.find_last(ads.get("currency")))["current_rate"]
        if not current_rate:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Can't get currency rate.")

        if payload.fixed_price is True and payload.price is None:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Enter price")
        elif payload.fixed_price is False:
            ads_price = current_rate * (float(payload.profit if payload.profit else 0) / 100. + 1.)
        elif payload.fixed_price is True and payload.price is not None:
            ads_price = payload.price
        elif payload.fixed_price is None:
            ads_price = ads["price"]

        await cls.update_one(
            query={"_id": ads["_id"]},
            payload={
                **payload.dict(exclude_unset=True),
                "price": ads_price
            }
        )
        ads = await cls.find_by_id(ads_id)
        ads["username"] = user.username
        return ads

    @classmethod
    async def update_currency(cls, currency_type: CurrencyType, currency_value: float):
        await cls.db[cls.collection].update_many(
            {
                "fixed_price": False,
                "currency": currency_type
            },
            [  # noqa
                {
                    "$set": {
                        "price": {
                            "$trunc": [{
                                "$multiply": [
                                    {"$add": [{"$multiply": ["$profit", 0.01]}, 1]},
                                    currency_value,
                                ]},
                                2]
                            }
                        }
                    }
            ],
        )

