from typing import List, Optional, Literal
from os import environ
from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request
from celery_app.tasks.crypto import update_usdt_rate
from database.crud import ContactCRUD, InvoiceCRUD
from schemas.contact import ContactStatus
from datetime import datetime
from http import HTTPStatus


__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def debug_get(
    request: Request,
):
    pass


@router.post("/")
async def debug_post():
    return {}
