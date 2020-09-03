from typing import Optional
from fastapi import WebSocket, Query, status
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.authentication import UnauthenticatedUser
from datetime import datetime

from schemas.user import User
from database.crud import UserCRUD
from core.utils.jwt import decode_jwt_token

__all__ = [
    "get_db",
    "get_user",
    "user_is_superuser",
    "get_user_websocket"
]


def get_db(request: Request):
    return request.app.mongo_db


async def get_user_websocket(
    websocket: WebSocket
) -> Optional[User]:
    token = websocket.cookies.get("token")
    user_id = (
        decode_jwt_token(token).get("id")
        if decode_jwt_token(token) is not None and decode_jwt_token(token).get("exp") > int(datetime.utcnow().timestamp())
        else None
    )
    if token is None or not user_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    user = await UserCRUD.find_by_id(user_id)
    return User(**user)


def get_user(request: Request):
    if isinstance(request.user, UnauthenticatedUser):
        raise HTTPException(401, "Auth is required")

    elif request.user and not request.user.is_active:
        raise HTTPException(401, "User is not active")

    else:
        return request.user


def user_is_staff_or_superuser(request: Request):
    user = get_user(request)

    if not user.is_staff and not user.is_superuser:
        raise HTTPException(403, "User has not enough permissions")
    else:
        return user


def user_is_superuser(request: Request):
    user = get_user(request)

    if not user.is_superuser:
        raise HTTPException(403, "User has not enough permissions")
    else:
        return user
