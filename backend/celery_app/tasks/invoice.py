from datetime import datetime

from schemas.invoice import InvoiceStatus
from database.crud import InvoiceCRUD, UserCRUD, AdsCRUD
from celery_app.celeryconfig import app
from core.mechanics import InvoiceMechanics
from config import IS_PRODUCTION

__all__ = ["update_invoice_status"]


@app.task(name="update_invoice_status", bind=True, soft_time_limit=42, time_limit=300)
async def update_invoice_status(self, *args, **kwargs):
    invoices = await InvoiceCRUD.find_many(query={
        "$or": [
            {"status": InvoiceStatus.WAITING_FOR_TOKENS},
            {"status": InvoiceStatus.WAITING_FOR_PAYMENT},
        ]
    })
    for invoice in invoices:
        date = invoice.get("status_changed_at")
        if invoice.get("status") == InvoiceStatus.WAITING_FOR_PAYMENT:
            if date:
                if (datetime.utcnow() - date).seconds / 60.0 >= (90.0 if IS_PRODUCTION else 10.0):
                    seller_db = await UserCRUD.find_by_id(invoice["seller_id"])
                    buyer_db = await UserCRUD.find_by_id(invoice["buyer_id"])
                    ads_db = await AdsCRUD.find_by_id(invoice["ads_id"])
                    seller, buyer, invoice, ads = await InvoiceMechanics(invoice, seller_db, buyer_db,
                                                                         ads_db).cancel_invoice()

                    await InvoiceCRUD.update_all(invoice, seller, buyer, ads)
        elif invoice.get("status") == InvoiceStatus.WAITING_FOR_TOKENS:
            if date:
                if (datetime.utcnow() - date).seconds / 60.0 >= (30.0 if IS_PRODUCTION else 10.0):
                    await InvoiceCRUD.freeze_invoice(str(invoice.get("_id")))

    return True
