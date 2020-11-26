from typing import List
from fastapi import APIRouter, Depends, Body

from api.dependencies import get_user
from database.crud import UserCRUD, ReferralCRUD
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
    UserTransaction,
    UserMakeWithdraw
)
from schemas.referral import (
    ReferralGeneralInfo,
)


__all__ = ["router"]

router = APIRouter()


@router.post("/login/", response_model=UserLoginResponse, response_model_exclude={"_id"})
async def account_login(data: UserLogin = Body(...)):
    return await UserCRUD.authenticate(data.email, data.password, data.language)


@router.post("/signup/")
async def account_signup(data: UserCreationSafe = Body(...)):
    user_id = await UserCRUD.create_safe(data)
    await ReferralCRUD.create_referral(str(user_id), data.referral_id)
    return True


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


@router.post("/withdraw/")
async def make_withdraw(user: User = Depends(get_user), payload: UserMakeWithdraw = Body(...)):
    return await UserCRUD.make_withdraw(user, payload)


@router.get("/referral_info/", response_model=ReferralGeneralInfo)
async def get_referral_info(user: User = Depends(get_user)):
    return await ReferralCRUD.get_general_info(user)
