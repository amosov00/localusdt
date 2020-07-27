from fastapi import APIRouter

from config import DEBUG

from api.controllers import account, debug, invoice, contact

api_router = APIRouter()

api_router.include_router(account.router, prefix="/account", tags=["account"])
api_router.include_router(invoice.router, prefix="/invoice", tags=["invoice"])
api_router.include_router(contact.router, prefix="/contact", tags=["contact"])


if DEBUG:
    api_router.include_router(debug.router, prefix="/debug", tags=["debug"])
