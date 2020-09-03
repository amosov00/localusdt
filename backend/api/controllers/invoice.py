from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, Body, Path, WebSocket, status
from collections import defaultdict
from starlette.websockets import WebSocketDisconnect

from schemas.base import ObjectId
from core.mechanics.chat_manager import chat_manager
from core.integrations.chat import ChatWrapper
from core.mechanics.chat_manager import ChatManager
from database.crud.invoice import InvoiceCRUD
from database.crud.chat import ChatRoomCRUD, ChatMessageCRUD
from api.dependencies import get_user, get_user_chat
from schemas.invoice import (
    InvoiceCreate,
    InvoiceInDB,
    InvoiceStatus,
    InvoiceInSearch,
    InvoiceWithAds
)
from schemas.chat import ChatRoomResponse
from schemas.user import User

__all__ = ["router"]

router = APIRouter()


@router.post("/create/", response_model=InvoiceInDB)
async def invoice_create(user: User = Depends(get_user), payload: InvoiceCreate = Body(...)):
    return await InvoiceCRUD.create_invoice(user, payload)


@router.put("/{invoice_id}/cancel/")
async def invoice_cancel(user: User = Depends(get_user), invoice_id: str = Path(...)):
    return await InvoiceCRUD.cancel_invoice(user, invoice_id)


@router.put("/{invoice_id}/confirm/")
async def invoice_approve(user: User = Depends(get_user), invoice_id: str = Path(...)):
    return await InvoiceCRUD.approve_invoice(user, invoice_id)


@router.put("/{invoice_id}/transfer/")
async def invoice_transfer(user: User = Depends(get_user), invoice_id: str = Path(...)):
    return await InvoiceCRUD.transfer_tokens(user, invoice_id)


@router.get("/", response_model=List[InvoiceInSearch])
async def invoice_search(user: User = Depends(get_user)):
    return await InvoiceCRUD.find_by_user_id(user.id)


@router.get("/{invoice_id}/", response_model=InvoiceWithAds)
async def invoice_get(user: User = Depends(get_user), invoice_id: str = Path(...)):
    return await InvoiceCRUD.get_invoice(user, invoice_id)


@router.websocket("/ws/{chatroom_id}/")
async def websocket_endpoint(
    websocket: WebSocket,
    chatroom_id: str = Path(...),
    user: User = Depends(get_user_chat)
):
    if user is None:
        return
    chatroom = await ChatRoomCRUD.find_by_id(chatroom_id)
    if not chatroom or user.id not in chatroom.get("participants"):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    await chat_manager.connect(websocket, chatroom_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = {
                "sender": user.username,
                "message_body": f"{data}",
                "is_service": False,
                "created_at": datetime.utcnow()
            }
            await ChatMessageCRUD.insert_one({
                **message,
                "chatroom_id": ObjectId(chatroom_id)
            })
            await chat_manager.push(message, chatroom_id)

    except WebSocketDisconnect:
        chat_manager.remove(websocket, chatroom_id)


@router.get("/chatroom/{chatroom_id}/", response_model=ChatRoomResponse)
async def get_chatroom(chatroom_id: str = Path(...), user: User = Depends(get_user)):
    return await ChatWrapper.get_chatroom_with_messages(str(user.id), chatroom_id)
