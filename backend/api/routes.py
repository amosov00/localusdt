from fastapi import APIRouter

from config import DEBUG

from api.controllers import account, debug, ads, invoice, currency, notification

api_router = APIRouter()

api_router.include_router(account.router, prefix="/account", tags=["account"])
api_router.include_router(ads.router, prefix="/order", tags=["order"])
api_router.include_router(invoice.router, prefix="/invoice", tags=["invoice"])
api_router.include_router(currency.router, prefix="/currency", tags=["currency"])
api_router.include_router(notification.router, prefix="/notification", tags=["notification"])


if DEBUG:
    api_router.include_router(debug.router, prefix="/debug", tags=["debug"])
