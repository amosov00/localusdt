from fastapi import APIRouter

from database import mongo_client

__all__ = ["router"]

router = APIRouter()


@router.get(
    "/",
    include_in_schema=False,
)
async def ping():
    return await mongo_client.admin.command("ping")
