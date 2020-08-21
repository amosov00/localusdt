from typing import List
from fastapi import APIRouter, Depends, Body, Path

from database.crud.invoice import InvoiceCRUD
from api.dependencies import get_user
from schemas.invoice import (
    InvoiceCreate,
    InvoiceInDB,
    InvoiceStatus,
    InvoiceInSearch,
    InvoiceWithAds
)
from schemas.user import User

__all__ = ["router"]

router = APIRouter()


@router.post("/create/", response_model=InvoiceInDB)
async def invoice_create(user: User = Depends(get_user), payload: InvoiceCreate = Body(...)):
    return await InvoiceCRUD.create_invoice(user, payload)


@router.put("/{invoice_id}/cancel/")
async def invoice_cancel(user: User = Depends(get_user), invoice_id: str = Path(...)):
    return await InvoiceCRUD.cancel_invoice(user, invoice_id)


@router.put("/{invoice_id}/confirm/")
async def invoice_approve(user: User = Depends(get_user), invoice_id: str = Path(...)):
    return await InvoiceCRUD.approve_invoice(user, invoice_id)


@router.put("/{invoice_id}/transfer/")
async def invoice_transfer(user: User = Depends(get_user), invoice_id: str = Path(...)):
    return await InvoiceCRUD.transfer_tokens(user, invoice_id)


@router.get("/", response_model=List[InvoiceInSearch])
async def invoice_search(user: User = Depends(get_user)):
    return await InvoiceCRUD.find_by_user_id(user.id)


@router.get("/{invoice_id}/", response_model=InvoiceWithAds)
async def invoice_get(user: User = Depends(get_user), invoice_id: str = Path(...)):
    return await InvoiceCRUD.get_invoice(user, invoice_id)
