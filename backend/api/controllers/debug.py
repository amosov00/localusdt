from fastapi import APIRouter, Request

from celery_app.tasks.crypto.deposits import check_deposits

__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def debug_get(
    request: Request,
):
    await check_deposits()


@router.post("/")
async def debug_post():
    return {}
