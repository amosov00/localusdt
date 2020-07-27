from typing import Optional, Union, List
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException
from http import HTTPStatus


from database.crud.base import BaseMongoCRUD
from database.crud import UserCRUD, CurrencyCRUD
from core.utils import to_objectid
from schemas.invoice import (
    Invoice,
    InvoiceCreate,
    InvoiceType,
    InvoiceFilters
)
from core.utils.binance import BinanceRate
from schemas.user import (
    User,
)


__all__ = ["InvoiceCRUD"]


class InvoiceCRUD(BaseMongoCRUD):
    collection: str = "invoice"

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
        for invoice in result:
            invoice["username"] = user.username
        return result

    @classmethod
    async def create(cls, user: User, payload: InvoiceCreate):
        if payload.amount_usdt > user.balance_usdt:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Not enough usdt on your account.")
        else:
            user.balance_usdt -= payload.amount_usdt
            await UserCRUD.update_one(query={"_id": user.id}, payload={"balance_usdt": user.balance_usdt})
        # Money check and transfer to invoice

        invoice = Invoice(
            **payload.dict(),
            user_id=user.id,
            created_at=datetime.now()
        )
        current_rate = (await CurrencyCRUD.find_last())["current_rate"]
        if not current_rate:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Can't get currency rate.")
        invoice.price = current_rate * (float(invoice.profit) / 100. + 1.)
        inserted_id = (
            await cls.insert_one(payload={
                **invoice.dict(),
            })
        ).inserted_id

        invoice_in_db = await cls.find_one(query={"_id": inserted_id})
        return invoice_in_db

    @classmethod
    async def find_with_filters(cls, filters: InvoiceFilters):
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
        for invoice in result:
            invoice["username"] = users_kw[invoice["user_id"]]
        return result
