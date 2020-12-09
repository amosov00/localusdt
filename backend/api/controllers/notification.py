from fastapi import APIRouter, Depends, Body, Path, WebSocket, status
from starlette.websockets import WebSocketDisconnect
from typing import List

from schemas.user import User
from schemas.notification import NotificationInDB
from database.crud.notification import NotificationCRUD
from api.dependencies import get_user_websocket, get_user
from core.mechanics.notification_manager import notification_manager


__all__ = ["router"]

router = APIRouter()


@router.get("/watch/")
async def watch_all(user: User = Depends(get_user)):
    return await NotificationCRUD.watch_notifications(user)


@router.get("/watch/{notification_id}/")
async def watch_notification(user: User = Depends(get_user), notification_id: str = Path(...)):
    return await NotificationCRUD.watch_notification(user, notification_id)


@router.get("/", response_model=List[NotificationInDB])
async def get_notifications(user: User = Depends(get_user)):
    return await NotificationCRUD.get_user_notifications(user)


@router.websocket("/ws/")
async def websocket_endpoint(
    websocket: WebSocket,
    user: User = Depends(get_user_websocket)
):
    if user is None:
        return
    await notification_manager.connect(websocket, str(user.id))
    try:
        while True:
            _ = await websocket.receive_text()

    except WebSocketDisconnect:
        notification_manager.remove(websocket, str(user.id))
