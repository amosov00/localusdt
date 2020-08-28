import asyncio
from typing import Optional, Union
from datetime import datetime
from fastapi import HTTPException
from http import HTTPStatus
from sentry_sdk import capture_message

from core.integrations.chat import ChatWrapper
from database.crud.base import BaseMongoCRUD
from database.crud.ads import AdsCRUD
from database.crud.user import UserCRUD
from core.utils import to_objectid, MailGunEmail
from core.mechanics import InvoiceMechanics
from schemas.base import ObjectId

from schemas.user import User

from schemas.invoice import InvoiceCreate, Invoice, InvoiceStatus

from schemas.ads import AdsType

__all__ = ["InvoiceCRUD"]


class InvoiceCRUD(BaseMongoCRUD):
    collection: str = "invoice"

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
        result = result if not buyer else seller + buyer
        users = await UserCRUD.find_many(query={})
        users_kw = {}
        for user in users:
            if user.get("username"):
                users_kw[user["_id"]] = user["username"]

        adses = await AdsCRUD.find_many(query={})
        adses_kw = {}
        for ads in adses:
            if ads.get("type"):
                adses_kw[ads["_id"]] = ads["type"]

        for invoice in result:
            invoice["seller_username"] = users_kw.get(invoice["seller_id"])
            invoice["buyer_username"] = users_kw.get(invoice["buyer_id"])
            invoice["ads_type"] = adses_kw.get(invoice["ads_id"])
        return sorted(result, key=lambda i: i["created_at"], reverse=True)

    @classmethod
    async def find_by_status(cls, status: InvoiceStatus) -> Optional[list]:
        return await super().find_many(query={"status": status})

    @classmethod
    async def update_all(cls, invoice: dict = None, seller: dict = None, buyer: dict = None, ads: dict = None) -> None:
        if invoice:
            await cls.update_one(
                query={"_id": invoice["id"]},
                payload=invoice
            )

        if seller:
            await UserCRUD.update_one(
                query={"_id": seller["id"]},
                payload=seller
            )

        if buyer:
            await UserCRUD.update_one(
                query={"_id": buyer["id"]},
                payload=buyer
            )

        if ads:
            await AdsCRUD.update_one(
                query={"_id": ads["id"]},
                payload=ads
            )

    @classmethod
    async def create_invoice(cls, user: User, payload: InvoiceCreate):
        ads = await AdsCRUD.find_by_id(payload.ads_id)

        if not ads:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong ads id")

        ads_type = ads.get("type")

        if ads["user_id"] == user.id:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Can't connect to your order")

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
            chat_id=await ChatWrapper.create_chat([ObjectId(seller_id), ObjectId(buyer_id)]),
            buyer_id=buyer_id,
            seller_id=seller_id,
            status=InvoiceStatus.WAITING_FOR_PAYMENT,
            created_at=datetime.utcnow(),
            status_changed_at=datetime.utcnow(),
            amount_rub=ads["price"] * payload.amount_usdt,
        )

        if invoice.amount_rub < ads.get("bot_limit"):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "You have exceeded the lower limit")
        if invoice.amount_rub > ads.get("top_limit"):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "You have exceeded the upper limit")

        seller_db = await UserCRUD.find_by_id(seller_id)
        buyer_db = await UserCRUD.find_by_id(buyer_id)
        ads_db = await AdsCRUD.find_by_id(payload.ads_id)
        seller, buyer, ads = await InvoiceMechanics(invoice, seller_db, buyer_db, ads_db).validate_creation()

        await cls.update_all(seller=seller, buyer=buyer, ads=ads)

        inserted_id = (await cls.insert_one(payload={**invoice.dict()})).inserted_id
        owner_email = (await UserCRUD.find_by_id(ads["user_id"])).get("email")
        asyncio.create_task(
            MailGunEmail().send_invoice_notification(to=owner_email, invoice_id=inserted_id)
        )
        invoice_in_db = await cls.find_one(query={"_id": inserted_id})
        return invoice_in_db

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

        seller_db = await UserCRUD.find_by_id(invoice["seller_id"])
        buyer_db = await UserCRUD.find_by_id(invoice["buyer_id"])
        ads_db = await AdsCRUD.find_by_id(invoice["ads_id"])
        seller, buyer, invoice, ads = await InvoiceMechanics(invoice, seller_db, buyer_db, ads_db).cancel_invoice()

        await cls.update_all(invoice, seller, buyer, ads)

        return True

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

        seller_db = await UserCRUD.find_by_id(invoice["seller_id"])
        ads_db = await AdsCRUD.find_by_id(invoice["ads_id"])

        seller, buyer, invoice, ads = await InvoiceMechanics(invoice, seller_db, buyer, ads_db).transfer_tokens()

        await cls.update_all(invoice, seller, buyer, ads)

        return True

    @classmethod
    async def get_invoice(cls, user: User, invoice_id: str):
        invoice = await InvoiceCRUD.find_by_id(invoice_id)
        if not (invoice.get("seller_id") == user.id or invoice.get("buyer_id") == user.id):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong invoice id")
        ads = await AdsCRUD.find_by_id(invoice["ads_id"])
        buyer_username = (await UserCRUD.find_by_id(invoice.get("buyer_id"))).get("username")
        seller_username = (await UserCRUD.find_by_id(invoice.get("seller_id"))).get("username")
        ads_type = (await AdsCRUD.find_by_id(invoice.get("ads_id"))).get("type")
        invoice["buyer_username"] = buyer_username
        invoice["seller_username"] = seller_username
        invoice["ads_type"] = ads_type
        invoice["bot_limit"] = ads["bot_limit"]
        invoice["top_limit"] = ads["top_limit"]
        invoice["condition"] = ads["condition"]

        return invoice
