from datetime import datetime

from schemas.ads import AdsStatuses
from schemas.invoice import InvoiceStatus
from database.crud import AdsCRUD, InvoiceCRUD
from celery_app.celeryconfig import app

__all__ = ["check_expired_orders"]


@app.task(name="check_expired_orders", bind=True, soft_time_limit=42, time_limit=300)
async def check_expired_orders(self, *args, **kwargs):
    orders = await AdsCRUD.find_many(
        query={
            "status": AdsStatuses.ACTIVE
        }
    )
    for order in orders:
        created_at: datetime = order.get("created_at")
        expiration_timestamp: int = order.get("expiration_timestamp")
        if expiration_timestamp + int(created_at.timestamp()) <= datetime.utcnow().timestamp():
            invoices = await InvoiceCRUD.find_many(query={
                "ads_id": order.get("_id")
            })
            can_delete = True
            for current_invoice in invoices:
                if current_invoice["status"] in InvoiceStatus.ACTIVE:
                    can_delete = False
            if can_delete:
                await AdsCRUD.set_status_not_safe(order.get("_id"), AdsStatuses.DELETED)

    return True
