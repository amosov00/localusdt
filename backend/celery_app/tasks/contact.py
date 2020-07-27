from datetime import datetime

from schemas.contact import ContactStatus
from database.crud import ContactCRUD
from celery_app.celeryconfig import app

__all__ = ["update_contacts_status"]


@app.task(name="update_contacts_status", bind=True, soft_time_limit=42, time_limit=300)
async def update_contacts_status(self, *args, **kwargs):
    contacts = await ContactCRUD.find_by_status(ContactStatus.WAITING_FOR_PAYMENT)
    for contact in contacts:
        date = contact.get("status_changed_at")
        if date:
            print((datetime.utcnow() - date).seconds / 60.0)
            if (datetime.utcnow() - date).seconds / 60.0 >= 90.0:
                await ContactCRUD._cancel_contact_db(contact)
    return True
