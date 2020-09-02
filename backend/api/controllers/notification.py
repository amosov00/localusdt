from fastapi import APIRouter, Depends, Body, Path, WebSocket, status

from api.dependencies import get_user_chat, get_user
from database.crud.notification import NotificationCRUD


__all__ = ["router"]

router = APIRouter()


@router.get("/watch/")
async def watch_all(user: Depends(get_user)):
    return await NotificationCRUD.watch_notifications(user)


@router.get("/")
async def get_notifications(user: Depends(get_user)):
    return await NotificationCRUD.get_user_notifications(user)


# @router.websocket("/ws")
# async def websocket_endpoint(
#     websocket: WebSocket,
#     user: User = Depends(get_user_chat)
# ):
#     if user is None:
#         return
#     chatroom = await ChatRoomCRUD.find_by_id(chatroom_id)
#     if not chatroom or user.id not in chatroom.get("participants"):
#         await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
#         return
#     await chat_manager.connect(websocket, chatroom_id)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             message = {
#                 "sender": user.username,
#                 "message_body": f"{data}",
#                 "is_service": False,
#                 "created_at": datetime.utcnow()
#             }
#             await ChatMessageCRUD.insert_one({
#                 **message,
#                 "chatroom_id": ObjectId(chatroom_id)
#             })
#             await chat_manager.push(message, chatroom_id)
#
#     except WebSocketDisconnect:
#         chat_manager.remove(websocket, chatroom_id)