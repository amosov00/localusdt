from typing import Optional, Union
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException
from http import HTTPStatus


from database.crud.base import BaseMongoCRUD
from core.utils import to_objectid
from schemas.invoice import (
    Invoice,
    InvoiceCreate,
    InvoiceType
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
    async def create(cls, user: User, payload: InvoiceCreate):
        invoice = Invoice(
            **payload.dict(),
            user_id=user.id,
            created_at=datetime.now()
        )
        current_rate = await BinanceRate().get_tether_rate()
        if not current_rate:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Can't get currency rate")
        invoice.price = current_rate * (float(invoice.profit) / 100. + 1.)
        inserted_id = (
            await cls.insert_one(payload={
                **invoice.dict(),
            })
        ).inserted_id

        invoice_in_db = await cls.find_one(query={"_id": inserted_id})
        return invoice_in_db
