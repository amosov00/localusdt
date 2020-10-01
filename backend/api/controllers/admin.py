from fastapi import APIRouter, Depends, Path, Query
from typing import List, Optional

from schemas.base import ObjectId
from database.crud.user import UserCRUD
from database.crud.invoice import InvoiceCRUD
from database.crud.logging import LogCRUD
from database.crud import USDTTransactionCRUD
from schemas.logging import Log
from schemas.invoice import InvoiceStatus, InvoiceWithAds, InvoiceInDB
from schemas.transaction import USDTTransaction, USDTTransactionStatus, USDTTransactionEvents
from api.dependencies import user_is_staff_or_superuser
from schemas import User

__all__ = ["router"]

router = APIRouter()


@router.get("/invoices/{status}/", response_model=Optional[List[InvoiceInDB]])
async def get_all_invoices(
    user: User = Depends(user_is_staff_or_superuser),
    status: str = Path(
        ..., description="possible: 'active', 'not_active', 'under_consideration'"
    ),
):
    if status == "active":
        return await InvoiceCRUD.get_invoice_by_status(status=InvoiceStatus.ACTIVE)
    elif status == "not_active":
        return await InvoiceCRUD.get_invoice_by_status(status=InvoiceStatus.NOT_ACTIVE)
    elif status == "under_consideration":
        return await InvoiceCRUD.get_invoice_by_status(
            status=InvoiceStatus.FROZEN
        )


@router.get("/invoice/{invoice_id}/", response_model=InvoiceWithAds)
async def get_all_invoices(
    user: User = Depends(user_is_staff_or_superuser), invoice_id: str = Path(...)
):
    return await InvoiceCRUD.get_invoice(user, invoice_id)


@router.put("/invoice/{invoice_id}/cancel/")
async def cancel_not_safe(
    user: User = Depends(user_is_staff_or_superuser), invoice_id: str = Path(...)
):
    return await InvoiceCRUD.cancel_invoice(user, invoice_id)


@router.put("/invoice/{invoice_id}/confirm/")
async def confirm_not_safe(
    user: User = Depends(user_is_staff_or_superuser), invoice_id: str = Path(...)
):
    return await InvoiceCRUD.approve_invoice(user, invoice_id)


@router.put("/invoice/{invoice_id}/transfer/")
async def transfer_not_safe(
    user: User = Depends(user_is_staff_or_superuser), invoice_id: str = Path(...)
):
    return await InvoiceCRUD.transfer_tokens(user, invoice_id)


@router.put("/invoice/{invoice_id}/rollback/")
async def rollback_invoice(
    user: User = Depends(user_is_staff_or_superuser), invoice_id: str = Path(...)
):
    return await InvoiceCRUD.rollback(invoice_id)


@router.put("/invoice/{invoice_id}/freeze/")
async def freeze_invoice(
    user: User = Depends(user_is_staff_or_superuser), invoice_id: str = Path(...)
):
    return await InvoiceCRUD.freeze_invoice(invoice_id)


@router.put("/users/ban/{user_id}/")
async def ban_user(
    user: User = Depends(user_is_staff_or_superuser), user_id: str = Path(...)
):
    # TODO: delete all ads and invoice for current user
    await UserCRUD.update_one(
        query={"_id": ObjectId(user_id)}, payload={"banned": True}
    )
    return True


@router.put("/users/unban/{user_id}/")
async def unban_user(
    user: User = Depends(user_is_staff_or_superuser), user_id: str = Path(...)
):
    await UserCRUD.update_one(
        query={"_id": ObjectId(user_id)}, payload={"banned": False}
    )
    return True


@router.put("/users/deactivate/{user_id}/")
async def deactivate_user(
    user: User = Depends(user_is_staff_or_superuser), user_id: str = Path(...)
):
    await UserCRUD.update_one(
        query={"_id": ObjectId(user_id)}, payload={"is_active": False}
    )
    return True


@router.put("/users/activate/{user_id}/")
async def activate_user(
    user: User = Depends(user_is_staff_or_superuser), user_id: str = Path(...)
):
    await UserCRUD.update_one(
        query={"_id": ObjectId(user_id)}, payload={"is_active": True}
    )
    return True


@router.get("/logs/", response_model=List[Log])
async def get_logs(
    user: User = Depends(user_is_staff_or_superuser)
):
    return await LogCRUD.find_many({})

# TODO: Make nice logs filters


@router.get("/transactions/", response_model=List[USDTTransaction])
async def get_transactions(
    user: User = Depends(user_is_staff_or_superuser),
    user_id: Optional[str] = None,
    to_adr: Optional[str] = None,
    from_adr: Optional[str] = None,
    status: Optional[USDTTransactionStatus] = None,
    event: Optional[USDTTransactionEvents] = None,
):
    tx_filter = USDTTransaction(
        user_id=ObjectId(user_id) if user_id is not None else None,
        to_adr=to_adr,
        from_adr=from_adr,
        status=status,
        event=event
    )
    return await USDTTransactionCRUD.find_many(query=tx_filter.dict(exclude_unset=True, exclude_none=True))
