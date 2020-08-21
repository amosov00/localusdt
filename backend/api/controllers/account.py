from typing import List
from http import HTTPStatus
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, Depends, Body, Request

from api.dependencies import get_user
from database.crud import UserCRUD
from schemas.user import (
    UserLogin,
    User,
    UserLoginResponse,
    UserCreationSafe,
    UserChangePassword,
    UserVerify,
    UserRecover,
    UserRecoverLink,
    UserUpdate,
    UserTransaction
)

__all__ = ["router"]

router = APIRouter()


@router.post("/login/", response_model=UserLoginResponse, response_model_exclude={"_id"})
async def account_login(data: UserLogin = Body(...)):
    return await UserCRUD.authenticate(data.email, data.password)


@router.post("/signup/")
async def account_signup(data: UserCreationSafe = Body(...)):
    return await UserCRUD.create_safe(data)


@router.post("/verify/", response_model=UserLoginResponse, response_model_exclude={"_id"})
async def account_verify(data: UserVerify = Body(...)):
    return await UserCRUD.verify(data.email, data.verification_code)


@router.get("/user/", response_model=User, response_model_exclude={"_id"})
async def account_get_user(user: User = Depends(get_user)):
    return user


@router.post("/change_password/")
async def account_change_password(user: User = Depends(get_user), payload: UserChangePassword = Body(...)):
    resp = await UserCRUD.change_password(user, payload)
    return resp


@router.post("/recover/")
async def account_recover_send(data: UserRecover = Body(...)):
    return await UserCRUD.recover_send(data)


@router.put("/recover/")
async def account_recover(data: UserRecoverLink = Body(...)):
    return await UserCRUD.recover(data)


@router.put("/user/", response_model=User, response_model_exclude={"_id"})
async def account_update_user(user: User = Depends(get_user), payload: UserUpdate = Body(...)):
    return await UserCRUD.update(user, payload)


@router.get("/transactions/", response_model=List[UserTransaction])
async def get_transactions(user: User = Depends(get_user)):
    return await UserCRUD.get_transactions(user)
