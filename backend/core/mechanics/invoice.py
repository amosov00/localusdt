from fastapi import HTTPException
from http import HTTPStatus
from datetime import datetime
from typing import Union
from bson import ObjectId

from schemas.ads import AdsType, AdsInDB
from schemas.invoice import Invoice, InvoiceStatus, InvoiceInDB
from schemas.user import User
from core.mechanics import AdsMechanics


__all__ = ["InvoiceMechanics"]


class InvoiceMechanics:
    def __init__(
            self,
            invoice: Union[dict, InvoiceInDB],
            seller: Union[dict, User],
            buyer: Union[dict, User],
            ads: Union[dict, AdsInDB],
    ):
        if isinstance(invoice, dict):
            invoice = InvoiceInDB(**invoice)

        if isinstance(seller, dict):
            seller = User(**seller)

        if isinstance(buyer, dict):
            buyer = User(**buyer)

        if isinstance(ads, dict):
            ads = AdsInDB(**ads)

        self.invoice = invoice
        self.seller = seller
        self.buyer = buyer
        self.ads = ads

    async def validate_creation(self):
        if self.ads.amount_usdt < self.invoice.amount_usdt:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "No such USDT on order")
        if self.ads.type == AdsType.BUY:
            if self.seller.balance_usdt < self.invoice.amount_usdt:
                raise HTTPException(HTTPStatus.BAD_REQUEST, "Not enough USDT on wallet")
            # validation section

            self.seller.balance_usdt -= self.invoice.amount_usdt
            self.seller.usdt_in_invoices += self.invoice.amount_usdt

        self.ads.amount_usdt -= self.invoice.amount_usdt

        return (
            self.seller.dict(),
            self.buyer.dict(),
            self.ads.dict()
        )

    async def cancel_invoice(self):
        if self.ads.type == AdsType.BUY:

            self.seller.usdt_in_invoices -= self.invoice.amount_usdt
            self.seller.balance_usdt += self.invoice.amount_usdt

        self.ads.amount_usdt += self.invoice.amount_usdt
        self.invoice.status = InvoiceStatus.CANCELLED
        self.invoice.finished_at = datetime.utcnow()

        return (
            self.seller.dict(),
            self.buyer.dict(),
            self.invoice.dict(),
            self.ads.dict()
        )

    async def transfer_tokens(self):

        self.seller.usdt_in_invoices -= self.invoice.amount_usdt
        self.buyer.balance_usdt += self.invoice.amount_usdt
        self.invoice.status = InvoiceStatus.COMPLETED
        self.invoice.finished_at = datetime.utcnow()
        self.invoice.status_changed_at = datetime.utcnow()

        return (
            self.seller.dict(),
            self.buyer.dict(),
            self.invoice.dict(),
            self.ads.dict()
        )
