from typing import Optional, Union
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException
from http import HTTPStatus
import logging
from sentry_sdk import capture_message

from database.crud.base import BaseMongoCRUD
from database.crud.ads import AdsCRUD
from database.crud.user import UserCRUD
from core.utils import to_objectid

from schemas.user import User

from schemas.invoice import InvoiceCreate, Invoice, InvoiceStatus

from schemas.ads import AdsType

__all__ = ["InvoiceCRUD"]


class InvoiceCRUD(BaseMongoCRUD):
    collection: str = "invoice"

    @classmethod
    async def find_by_id(cls, _id: str) -> Optional[dict]:
        return await super().find_one(query={"_id": to_objectid(_id)}) if _id else None

    @classmethod
    async def find_by_ads_id(cls, _id: str) -> Optional[list]:
        return await super().find_many(query={"ads_id": to_objectid(_id)}) if _id else None

    @classmethod
    async def find_by_user_id(cls, _id: str) -> Optional[list]:
        seller: list = await super().find_many(
            query={"seller_id": to_objectid(_id)}
        ) if _id else []
        buyer: list = await super().find_many(
            query={"buyer_id": to_objectid(_id)}
        ) if _id else []
        result = seller if seller else []
        return result if not buyer else seller + buyer

    @classmethod
    async def find_by_status(cls, status: InvoiceStatus) -> Optional[list]:
        return await super().find_many(query={"status": status})

    @classmethod
    async def create_invoice(cls, user: User, payload: InvoiceCreate):
        ads = await AdsCRUD.find_by_id(payload.ads_id)

        if not ads:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong ads id")

        ads_type = ads.get("type")

        if ads_type:
            buyer_id = (
                ads["user_id"] if ads_type == AdsType.BUY else user.id
            )
            seller_id = (
                ads["user_id"] if ads_type == AdsType.SELL else user.id
            )
        else:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Ads got corrupted")

        # Give roles to users

        invoice = Invoice(
            **payload.dict(),
            buyer_id=buyer_id,
            seller_id=seller_id,
            status=InvoiceStatus.WAITING_FOR_PAYMENT,
            created_at=datetime.utcnow(),
            status_changed_at=datetime.utcnow(),
            amount_rub=ads["price"] * payload.amount_usdt,
        )

        if payload.amount_usdt > ads["amount_usdt"]:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Not enough money on ads")
        else:
            ads["amount_usdt"] -= payload.amount_usdt
            await AdsCRUD.update_one(
                query={"_id": payload.ads_id},
                payload={"amount_usdt": ads["amount_usdt"]},
            )
        # Check money is enough and transfer

        inserted_id = (await cls.insert_one(payload={**invoice.dict()})).inserted_id

        ads_in_db = await cls.find_one(query={"_id": inserted_id})
        return ads_in_db

    @classmethod
    async def _cancel_invoice_db(cls, invoice: dict):
        ads = await AdsCRUD.find_by_id(invoice.get("ads_id"))
        if ads:
            ads["amount_usdt"] += invoice.get("amount_usdt")
            await AdsCRUD.update_one(
                query={"_id": ads["_id"]},
                payload={"amount_usdt": ads["amount_usdt"]},
            )
            await cls.update_one(
                query={"_id": invoice["_id"]},
                payload={
                    "status": InvoiceStatus.CANCELLED,
                    "finished_at": datetime.utcnow(),
                },
            )
        else:
            capture_message(
                f"Error while cancelling invoice, invoice_id: {invoice['_id']}"
            )
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, "Error while cancelling invoice"
            )

    @classmethod
    async def cancel_invoice(cls, user: User, invoice_id: str):
        invoice = await cls.find_by_id(invoice_id)

        if not invoice:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong invoice id")

        if (
            invoice.get("buyer_id") != user.id
            or invoice.get("status") != InvoiceStatus.WAITING_FOR_PAYMENT
        ):
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, "Wrong user role or invoice status"
            )

        await cls._cancel_invoice_db(invoice)

        return await cls.find_by_id(invoice_id)

    @classmethod
    async def approve_invoice(cls, user: User, invoice_id: str):
        invoice = await cls.find_by_id(invoice_id)

        if not invoice:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong invoice id")

        if (
            invoice.get("buyer_id") != user.id
            or invoice.get("status") != InvoiceStatus.WAITING_FOR_PAYMENT
        ):
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, "Wrong user role or invoice status"
            )

        await cls.update_one(
            query={"_id": invoice["_id"]},
            payload={
                "status": InvoiceStatus.WAITING_FOR_TOKENS,
                "status_changed_at": datetime.utcnow(),
            },
        )

        return True

    @classmethod
    async def transfer_tokens(cls, user: User, invoice_id: str):
        invoice = await cls.find_by_id(invoice_id)

        if not invoice:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong invoice id")

        if (
            invoice.get("seller_id") != user.id
            or invoice.get("status") != InvoiceStatus.WAITING_FOR_TOKENS
        ):
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, "Wrong user role or invoice status"
            )

        buyer = await UserCRUD.find_by_id(invoice["buyer_id"])
        if not buyer:
            capture_message(f"invoice got corrupted, invoice id: {invoice_id}")
            raise HTTPException(HTTPStatus.BAD_REQUEST, "invoice got corrupted")

        await cls.update_one(
            query={"_id": invoice["_id"]},
            payload={
                "status": InvoiceStatus.COMPLETED,
                "finished_at": datetime.utcnow(),
                "status_changed_at": datetime.utcnow(),
            },
        )

        await UserCRUD.update_one(
            query={"_id": invoice["buyer_id"]},
            payload={
                "balance_usdt": buyer.get("balance_usdt") + invoice["amount_usdt"]
                if buyer.get("balance_usdt")
                else invoice["amount_usdt"]
            },
        )

        return True
