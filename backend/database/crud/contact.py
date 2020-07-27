from typing import Optional, Union
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException
from http import HTTPStatus
import logging
from sentry_sdk import capture_message

from database.crud.base import BaseMongoCRUD
from database.crud.invoice import InvoiceCRUD
from core.utils import to_objectid

from schemas.user import User

from schemas.contact import ContactCreate, Contact, ContactStatus

from schemas.invoice import InvoiceType

__all__ = ["ContactCRUD"]


class ContactCRUD(BaseMongoCRUD):
    collection: str = "contact"

    @classmethod
    async def find_by_id(cls, _id: str) -> Optional[dict]:
        return await super().find_one(query={"_id": to_objectid(_id)}) if _id else None

    @classmethod
    async def find_by_invoice_id(cls, _id: str) -> Optional[list]:
        return await super().find_many(query={"_id": to_objectid(_id)}) if _id else None

    @classmethod
    async def find_by_user_id(cls, _id: str) -> Optional[list]:
        seller: list = await super().find_many(
            query={"seller_id": to_objectid(_id)}
        ) if _id else None
        buyer: list = await super().find_many(
            query={"buyer_id": to_objectid(_id)}
        ) if _id else None
        if seller:
            return seller + buyer

    @classmethod
    async def find_by_status(cls, status: ContactStatus) -> Optional[list]:
        return await super().find_many(query={"status": status})

    @classmethod
    async def create_contact(cls, user: User, payload: ContactCreate):
        invoice = await InvoiceCRUD.find_by_id(payload.invoice_id)

        if not invoice:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong invoice id")

        invoice_type = invoice.get("type")

        if invoice_type:
            buyer_id = (
                invoice["user_id"] if invoice_type == InvoiceType.BUY else user.id
            )
            seller_id = (
                invoice["user_id"] if invoice_type == InvoiceType.SELL else user.id
            )
        else:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Invoice got corrupted")

        contact = Contact(
            **payload.dict(),
            buyer_id=buyer_id,
            seller_id=seller_id,
            status=ContactStatus.WAITING_FOR_PAYMENT,
            created_at=datetime.utcnow(),
            status_changed_at=datetime.utcnow()
        )

        if payload.amount_usdt > invoice["amount_usdt"]:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Not enough money on invoice")
        else:
            invoice["amount_usdt"] -= payload.amount_usdt
            await InvoiceCRUD.update_one(
                query={"_id": payload.invoice_id},
                payload={"amount_usdt": invoice["amount_usdt"]},
            )
        # Check money is enough and transfer
        inserted_id = (await cls.insert_one(payload={**contact.dict()})).inserted_id

        invoice_in_db = await cls.find_one(query={"_id": inserted_id})
        return invoice_in_db

    @classmethod
    async def _cancel_contact_db(cls, contact: dict):
        invoice = await InvoiceCRUD.find_by_id(contact.get("invoice_id"))
        if invoice:
            invoice["amount_usdt"] += contact.get("amount_usdt")
            await InvoiceCRUD.update_one(
                query={"_id": invoice["_id"]},
                payload={"amount_usdt": invoice["amount_usdt"]}
            )
            await cls.update_one(
                query={"_id": contact["_id"]},
                payload={
                    "status": ContactStatus.CANCELLED,
                    "finished_at": datetime.utcnow()
                },
            )
        else:
            capture_message(f"Error while cancelling contact, contact_id: {contact['_id']}")
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Error while cancelling contact")

    @classmethod
    async def cancel_contact(cls, user: User, contact_id: str):
        contact = await cls.find_by_id(contact_id)

        if not contact:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong contact id")

        if (
                contact.get("buyer_id") != user.id
                or contact.get("status") != ContactStatus.WAITING_FOR_PAYMENT
        ):
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, "Wrong user role or contact status"
            )

        await cls._cancel_contact_db(contact)

        return await cls.find_by_id(contact_id)
