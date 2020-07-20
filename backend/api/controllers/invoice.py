from http import HTTPStatus
from typing import List

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, Body, Response

from database.crud.invoice import InvoiceCRUD
from api.dependencies import get_user
from schemas.invoice import (
    Invoice,
    InvoiceCreate,
    InvoiceInDB
)
from schemas.user import User

__all__ = ["router"]

router = APIRouter()


@router.post("/", response_model=InvoiceInDB)
async def create_invoice(
    user: User = Depends(get_user), data: InvoiceCreate = Body(...),
):
    created_invoice = await InvoiceCRUD.create(user, data)
    return created_invoice


@router.get("/", response_model=List[InvoiceInDB])
async def invoice_fetch_all(user: User = Depends(get_user)):
    return await InvoiceCRUD.find_by_user_id(user.id)
