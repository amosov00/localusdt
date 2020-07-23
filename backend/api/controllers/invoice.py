from http import HTTPStatus
from typing import List

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, Body, Response

from database.crud.invoice import InvoiceCRUD
from api.dependencies import get_user
from schemas.invoice import (
    InvoiceFilters,
    InvoiceCreate,
    InvoiceInDB,
    InvoiceInSearch
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


@router.get("/user/", response_model=List[InvoiceInSearch])
async def invoice_fetch_users(user: User = Depends(get_user)):
    return await InvoiceCRUD.find_by_user_obj(user)


@router.get("/", response_model=List[InvoiceInSearch])
async def invoice_fetch_all(filters: InvoiceFilters = Body(...)):
    return await InvoiceCRUD.find_with_filters(filters)

