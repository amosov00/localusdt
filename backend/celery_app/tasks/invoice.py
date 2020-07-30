from datetime import datetime

from schemas.invoice import InvoiceStatus
from database.crud import InvoiceCRUD
from celery_app.celeryconfig import app

__all__ = ["update_invoice_status"]


@app.task(name="update_invoice_status", bind=True, soft_time_limit=42, time_limit=300)
async def update_invoice_status(self, *args, **kwargs):
    invoices = await InvoiceCRUD.find_by_status(InvoiceStatus.WAITING_FOR_PAYMENT)
    for invoice in invoices:
        date = invoice.get("status_changed_at")
        if date:
            if (datetime.utcnow() - date).seconds / 60.0 >= 90.0:
                await InvoiceCRUD._cancel_invoice_db(invoice)
    return True
