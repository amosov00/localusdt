import asyncio
from typing import Optional, Union, List
from datetime import datetime
from fastapi import HTTPException
from http import HTTPStatus
from sentry_sdk import capture_message

from core.mechanics.notification_manager import NotificationSender
from core.integrations.chat import ChatWrapper
from database.crud.base import BaseMongoCRUD
from database.crud.ads import AdsCRUD
from database.crud.user import UserCRUD
from core.utils import to_objectid, MailGunEmail
from core.mechanics import InvoiceMechanics
from schemas.base import ObjectId
from core.mechanics.logging import LogMechanics
from schemas.logging import LogEvents

from schemas.user import User, UserLanguage

from schemas.invoice import InvoiceCreate, Invoice, InvoiceStatus

from schemas.ads import AdsType, AdsStatuses

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
                adses_kw[ads["_id"]] = ads

        for invoice in result:
            invoice["seller_username"] = users_kw.get(invoice["seller_id"])
            invoice["buyer_username"] = users_kw.get(invoice["buyer_id"])
            invoice["ads_type"] = adses_kw.get(invoice["ads_id"]).get("type")
            invoice["payment_method"] = adses_kw.get(invoice["ads_id"]).get("payment_method")
            invoice["other_payment_method"] = adses_kw.get(invoice["ads_id"]).get("other_payment_method")
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
            currency=ads.get("currency"),
            amount=ads["price"] * payload.amount_usdt,
        )

        if payload.amount_usdt < ads.get("bot_limit"):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "You have exceeded the lower limit")
        if payload.amount_usdt > ads.get("top_limit"):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "You have exceeded the upper limit")

        seller_db = await UserCRUD.find_by_id(seller_id)
        buyer_db = await UserCRUD.find_by_id(buyer_id)
        ads_db = await AdsCRUD.find_by_id(payload.ads_id)
        seller, buyer, ads = await InvoiceMechanics(invoice, seller_db, buyer_db, ads_db).validate_creation()

        await cls.update_all(seller=seller, buyer=buyer, ads=ads)

        inserted_id = (await cls.insert_one(payload={**invoice.dict()})).inserted_id
        owner = await UserCRUD.find_by_id(ads["user_id"])
        asyncio.create_task(
            MailGunEmail(owner.get("language") if owner.get("language") else UserLanguage.RU).send_invoice_notification(to=owner.get("email"), invoice_id=inserted_id)
        )
        invoice_in_db = await cls.find_one(query={"_id": inserted_id})
        await NotificationSender.send_new_invoice(
            str(ads["user_id"]),
            amount=invoice.amount_usdt,
            participant_nickname=user.username,
            invoice_id=inserted_id
        )
        await LogMechanics.new_log(
            event=LogEvents.START_INVOICE,
            user_id=ObjectId(user.id),
            invoice_id=invoice_in_db.get("_id")
        )
        return invoice_in_db

    @classmethod
    async def _send_status_notification(cls, user: User, invoice: dict, status: InvoiceStatus):
        status = str(status)
        seller = await UserCRUD.find_by_id(invoice["seller_id"])
        buyer = await UserCRUD.find_by_id(invoice["buyer_id"])
        if user.is_staff:
            await NotificationSender.send_invoice_status_change(
                seller["_id"],
                participant_nickname=buyer["username"],
                invoice_id=invoice["_id"],
                new_status=status,
            )
            await NotificationSender.send_invoice_status_change(
                buyer["_id"],
                participant_nickname=seller["username"],
                invoice_id=invoice["_id"],
                new_status=status,
            )
            return

        if user.id != seller["_id"]:
            await NotificationSender.send_invoice_status_change(
                seller["_id"],
                participant_nickname=buyer["username"],
                invoice_id=invoice["_id"],
                new_status=status,
            )
        else:
            await NotificationSender.send_invoice_status_change(
                buyer["_id"],
                participant_nickname=seller["username"],
                invoice_id=invoice["_id"],
                new_status=status,
            )

    @classmethod
    async def cancel_invoice(cls, user: User, invoice_id: str):
        invoice = await cls.find_by_id(invoice_id)

        if not invoice:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong invoice id")

        if invoice.get("buyer_id") != user.id:
            if not user.is_staff:
                raise HTTPException(
                    HTTPStatus.BAD_REQUEST, "Wrong user role or invoice status"
                )
        if invoice.get("status") not in (InvoiceStatus.WAITING_FOR_TOKENS, InvoiceStatus.WAITING_FOR_PAYMENT):
            if not user.is_staff:
                raise HTTPException(
                    HTTPStatus.BAD_REQUEST, "Wrong user role or invoice status"
                )

        seller_db = await UserCRUD.find_by_id(invoice["seller_id"])
        buyer_db = await UserCRUD.find_by_id(invoice["buyer_id"])
        ads_db = await AdsCRUD.find_by_id(invoice["ads_id"])
        await LogMechanics.new_log(
            event=LogEvents.CANCEL_INVOICE,
            user_id=ObjectId(user.id),
            invoice_id=invoice.get("_id")
        )
        seller, buyer, invoice, ads = await InvoiceMechanics(invoice, seller_db, buyer_db, ads_db).cancel_invoice()

        await cls.update_all(invoice, seller, buyer, ads)
        invoice = await cls.find_by_id(invoice_id)
        await cls._send_status_notification(user, invoice, InvoiceStatus.CANCELLED)
        return True

    @classmethod
    async def approve_invoice(cls, user: User, invoice_id: str):
        invoice = await cls.find_by_id(invoice_id)

        if not invoice:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong invoice id")

        if user.is_staff:
            if invoice.get("status") not in (InvoiceStatus.FROZEN, InvoiceStatus.WAITING_FOR_PAYMENT):
                raise HTTPException(HTTPStatus.BAD_REQUEST, "Bad invoice status")
        else:
            if invoice.get("buyer_id") != user.id or invoice.get("status") not in InvoiceStatus.WAITING_FOR_TOKENS:
                raise HTTPException(HTTPStatus.BAD_REQUEST, "Bad invoice status or user role")

        await cls.update_one(
            query={"_id": invoice["_id"]},
            payload={
                "status": InvoiceStatus.WAITING_FOR_TOKENS,
                "status_changed_at": datetime.utcnow(),
            },
        )

        await cls._send_status_notification(user, invoice, InvoiceStatus.APPROVED)

        await LogMechanics.new_log(
            event=LogEvents.APPROVE_INVOICE,
            user_id=ObjectId(user.id),
            invoice_id=invoice.get("_id")
        )
        seller = await UserCRUD.find_by_id(invoice.get("seller_id"))
        await MailGunEmail(seller.get("language") if seller.get("language") else UserLanguage.RU).send_invoice_notification_to_seller(seller.get("email"), str(invoice.get("_id")))

        return True

    @classmethod
    async def transfer_tokens(cls, user: User, invoice_id: str):
        invoice = await cls.find_by_id(invoice_id)

        if not invoice:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong invoice id")

        if user.is_staff:
            if invoice.get("status") not in (InvoiceStatus.WAITING_FOR_TOKENS, InvoiceStatus.FROZEN, InvoiceStatus.WAITING_FOR_PAYMENT):
                raise HTTPException(HTTPStatus.BAD_REQUEST, "Bad invoice status")
        else:
            if invoice.get("seller_id") != user.id or invoice.get("status") not in InvoiceStatus.WAITING_FOR_TOKENS:
                raise HTTPException(HTTPStatus.BAD_REQUEST, "Bad invoice status or user role")

        buyer = await UserCRUD.find_by_id(invoice["buyer_id"])
        if not buyer:
            capture_message(f"invoice got corrupted, invoice id: {invoice_id}")
            raise HTTPException(HTTPStatus.BAD_REQUEST, "invoice got corrupted")

        seller_db = await UserCRUD.find_by_id(invoice["seller_id"])
        ads_db = await AdsCRUD.find_by_id(invoice["ads_id"])

        seller, buyer, invoice, ads = await InvoiceMechanics(invoice, seller_db, buyer, ads_db).transfer_tokens()

        await cls.update_all(invoice, seller, buyer, ads)
        invoice_in_db = await cls.find_by_id(invoice_id)
        ads_in_db = await AdsCRUD.find_by_id(invoice_in_db["ads_id"])
        await cls._send_status_notification(user, invoice_in_db, InvoiceStatus.COMPLETED)

        if ads.get("amount_usdt") * ads.get("price") <= ads["bot_limit"]:
            invoices = await cls.find_many(query={
                "ads_id": ads_in_db["_id"]
            })
            can_delete = True
            for current_invoice in invoices:
                if current_invoice["status"] in InvoiceStatus.ACTIVE:
                    can_delete = False
            if can_delete:
                if user.is_staff:
                    await AdsCRUD.set_status_not_safe(str(ads_in_db["_id"]), AdsStatuses.DELETED)
                else:
                    await AdsCRUD.set_status_safe(user, str(ads_in_db["_id"]), AdsStatuses.DELETED)

        await LogMechanics.new_log(
            event=LogEvents.TRANSFER_TOKENS,
            user_id=ObjectId(user.id),
            invoice_id=invoice.get("_id")
        )

        return True

    @classmethod
    async def get_invoice(cls, user: User, invoice_id: str):
        invoice = await InvoiceCRUD.find_by_id(invoice_id)
        if not invoice:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong invoice id")
        if not (invoice.get("seller_id") == user.id or invoice.get("buyer_id") == user.id or user.is_staff):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong invoice id")
        ads = await AdsCRUD.find_by_id(invoice["ads_id"])
        buyer_username = (await UserCRUD.find_by_id(invoice.get("buyer_id"))).get("username")
        seller_username = (await UserCRUD.find_by_id(invoice.get("seller_id"))).get("username")
        invoice["buyer_username"] = buyer_username
        invoice["seller_username"] = seller_username
        invoice["ads_type"] = ads.get("type")
        invoice["bot_limit"] = ads["bot_limit"]
        invoice["top_limit"] = ads["top_limit"]
        invoice["condition"] = ads["condition"]
        invoice["payment_method"] = ads.get("payment_method")
        invoice["other_payment_method"] = ads.get("other_payment_method")

        return invoice

    @classmethod
    async def get_invoice_by_statuses(cls, statuses: List[InvoiceStatus]):
        invoices = await cls.find_many({
            "status": {"$in": statuses}
        })
        return invoices

    @classmethod
    async def rollback(cls, invoice_id: str):
        invoice = await cls.find_by_id(invoice_id)
        if not invoice:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong invoice id")
        if invoice.get("status") != InvoiceStatus.COMPLETED:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong invoice status")
        seller = await UserCRUD.find_by_id(invoice.get("seller_id"))
        buyer = await UserCRUD.find_by_id(invoice.get("buyer_id"))
        await UserCRUD.update_one(
            query={
                "_id": invoice.get("seller_id")
            },
            payload={
                "balance_usdt": seller.get("balance_usdt") + invoice.get("amount_usdt")
            }
        )
        await UserCRUD.update_one(
            query={
                "_id": invoice.get("buyer_id")
            },
            payload={
                "balance_usdt": buyer.get("balance_usdt") - invoice.get("amount_usdt")
            }
        )

        return True

    @classmethod
    async def freeze_invoice(cls, invoice_id: str):
        invoice = await cls.find_by_id(invoice_id)
        if not invoice:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong invoice id")
        if invoice.get("status") not in InvoiceStatus.ACTIVE:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong invoice status")
        await InvoiceCRUD.update_one(
            query={
                "_id": invoice.get("_id")
            },
            payload={
                "status": InvoiceStatus.FROZEN
            }
        )
        staff = await UserCRUD.find_many(query={"is_staff": True})
        staff_ids = [i.get("_id") for i in staff]
        await NotificationSender.send_frozen_invoice_notification(staff_ids, invoice_id=invoice_id)
        return True

# 123