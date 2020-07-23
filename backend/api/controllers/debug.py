from typing import List, Optional, Literal
from os import environ
from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request
from celery_app.tasks.crypto import update_usdt_rate


__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def debug_get(
    request: Request,
):
    await update_usdt_rate()
    return {
        "headers": request.headers,
        "envvars": dict(environ),
    }


@router.post("/")
async def debug_post():
    return {}
