from typing import List
from fastapi import APIRouter, Depends, Body, Path

from database.crud.contact import ContactCRUD
from api.dependencies import get_user
from schemas.contact import (
    ContactCreate,
    ContactInDB,
    ContactStatus
)
from schemas.user import User

__all__ = ["router"]

router = APIRouter()


@router.post("/create/", response_model=ContactInDB)
async def contact_create(user: User = Depends(get_user), payload: ContactCreate = Body(...)):
    return await ContactCRUD.create_contact(user, payload)


@router.put("/{contact_id}/cancel/", response_model=ContactInDB)
async def contact_cancel(user: User = Depends(get_user), contact_id: str = Path(...)):
    return await ContactCRUD.cancel_contact(user, contact_id)


@router.get("/", response_model=List[ContactInDB])
async def contact_search(user: User = Depends(get_user)):
    return await ContactCRUD.find_by_user_id(user.id)
