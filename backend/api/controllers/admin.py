from fastapi import APIRouter, Depends, Path
from typing import List, Optional

from database.crud.invoice import InvoiceCRUD
from schemas.invoice import InvoiceStatus, InvoiceWithAds, InvoiceInDB
from api.dependencies import user_is_staff_or_superuser
from schemas import User

__all__ = [
    'router'
]

router = APIRouter()


@router.get("/invoices/{status}/", response_model=Optional[List[InvoiceInDB]])
async def get_all_invoices(user: User = Depends(user_is_staff_or_superuser), status: str = Path(...)):
    if status == "active":
        return await InvoiceCRUD.get_invoice_by_status(status=InvoiceStatus.ACTIVE)
    elif status == "not_active":
        return await InvoiceCRUD.get_invoice_by_status(status=InvoiceStatus.NOT_ACTIVE)


@router.get("/invoice/{invoice_id}/", response_model=InvoiceWithAds)
async def get_all_invoices(user: User = Depends(user_is_staff_or_superuser), invoice_id: str = Path(...)):
    return await InvoiceCRUD.get_invoice(user, invoice_id)


@router.put("/invoice/{invoice_id}/cancel/")
async def cancel_not_safe(user: User = Depends(user_is_staff_or_superuser), invoice_id: str = Path(...)):
    return await InvoiceCRUD.cancel_invoice(user, invoice_id)


@router.put("/invoice/{invoice_id}/confirm/")
async def confirm_not_safe(user: User = Depends(user_is_staff_or_superuser), invoice_id: str = Path(...)):
    return await InvoiceCRUD.approve_invoice(user, invoice_id)


@router.put("/invoice/{invoice_id}/transfer/")
async def transfer_not_safe(user: User = Depends(user_is_staff_or_superuser), invoice_id: str = Path(...)):
    return await InvoiceCRUD.transfer_tokens(user, invoice_id)


@router.put("/invoice/{invoice_id}/rollback/")
async def rollback_invoice(user: User = Depends(user_is_staff_or_superuser), invoice_id: str = Path(...)):
    return await InvoiceCRUD.rollback(invoice_id)

