import re
from typing import Optional
from datetime import datetime
from enum import IntEnum
from decimal import Decimal

from pydantic import Field, validator
from passlib.context import CryptContext
from fastapi import HTTPException
from http import HTTPStatus

from schemas.base import BaseModel, ObjectIdPydantic

__all__ = [
    "pwd_context",
    "User",
    "UserLogin",
    "UserCreationSafe",
    "UserCreationNotSafe",
    "UserLoginResponse",
    "UserChangePassword",
    "UserVerify",
    "UserRecover",
    "UserRecoverLink",
    "UserUpdate",
    "UserTransactionStatus",
    "UserTransactionEvents",
    "UserTransaction",
    "UserMakeWithdraw",
    "UserUpdateNotSafe",
    "UserLanguage",
    "UserAdminView",
    "UserLocation"
]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_email(v: str) -> str:
    return v.lower() if v else v


def validate_password(v: Optional[str], values: dict) -> str:
    if len(v) < 8:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST, "password should be longer than 8 characters"
        )
    if "repeat_password" in values and v != values["repeat_password"]:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "passwords do not match")
    if not bool(re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", v)):  # noqa
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            "password does not match password policy (at least one uppercase letter, one lowercase, one number)",
        )
    return pwd_context.hash(v)


def validate_username(v: Optional[str], values: dict) -> str:
    if len(v) < 6:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "username should be longer than 6 characters")
    if not bool(re.match("^(?=[a-zA-Z0-9._]{6,20}$)(?!.*[_.]{2})[^_.].*[^_.]$", v)): # noqa
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            "username does not match username policy (contains only alphabetic, underline and dots)"
        )
    return v


def validate_withdraw_amount(v: Optional[float]) -> float:
    if v >= 10000:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Too much usdt to withdraw")
    if v <= 0:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Wrong usdt format")

    return v


class BaseUser(BaseModel):
    pass


class UserLanguage(IntEnum):
    RU = 1
    ENG = 2


class UserLocation(BaseModel):
    country_name: Optional[str] = Field(default=None)
    country_code: Optional[str] = Field(default=None)
    region: Optional[str] = Field(default=None)


class User(BaseModel):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
    email: str = Field(default=None)
    username: str = Field(default=None)
    balance_usdt: float = Field(default=0)
    usdt_in_invoices: float = Field(default=0)
    eth_address: Optional[str] = Field(default=None)
    current_state: Optional[int] = Field(
        default=None, description="1 - green, 2 - orange, 3 - red"
    )
    is_active: Optional[bool] = Field(default=True, description="User is active")
    is_staff: Optional[bool] = Field(default=False, description="Moderator")
    is_superuser: Optional[bool] = Field(default=False, description="Admin")
    banned: Optional[bool] = Field(default=False, description="User banned or not")
    verification_code: Optional[str] = Field(default=None)
    recover_code: Optional[str] = Field(
        default=None, description="JWT token for password recover"
    )
    last_active: Optional[datetime] = Field(default=None)
    language: Optional[UserLanguage] = Field(default=None, description="1 -- RU, 2 -- ENG")
    created_at: Optional[datetime] = Field(default=None)
    about_me: str = Field(default="", description="About me field")
    location: UserLocation = Field(default=None, description="User last location")


class UserVerify(BaseModel):
    email: str = Field(...)
    verification_code: str = Field(...)


class UserLogin(BaseModel):
    email: str = Field(..., example="email")
    password: str = Field(..., example="password")


class UserLoginResponse(BaseModel):
    token: str = Field(..., description="JWT token")
    user: User


class UserChangePassword(BaseModel):
    old_password: str = Field(...)
    repeat_password: str = Field(...)
    password: str = Field(...)

    _validate_passwords = validator("password", allow_reuse=True)(validate_password)


class UserCreationSafe(BaseModel):
    email: str = Field(...)
    username: str = Field(...)
    repeat_password: str = Field(...)
    password: str = Field(...)
    language: UserLanguage = Field(default=UserLanguage.RU, example="1", description="It's enum, 1 -- RU, 2 -- ENG")
    referral_id: Optional[str] = Field(default=None)

    _validate_email = validator("email", allow_reuse=True)(validate_email)
    _validate_passwords = validator("password", allow_reuse=True)(validate_password)
    _validate_username = validator("username", allow_reuse=True)(validate_username)


class UserCreationNotSafe(BaseModel):
    email: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    ethereum_wallet: Optional[str] = Field(default=None)
    repeat_password: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)

    _validate_passwords = validator("password", allow_reuse=True)(validate_password)
    _validate_email = validator("email", pre=True, allow_reuse=True)(validate_email)


class UserRecover(BaseModel):
    email: str = Field(...)


class UserRecoverLink(BaseModel):
    recover_code: str = Field(...)
    password: str = Field(...)
    repeat_password: str = Field(...)

    _validate_passwords = validator("password", allow_reuse=True)(validate_password)


class UserUpdate(BaseModel):
    about_me: str = Field(default=None, description="'About me' field")
    language: UserLanguage = Field(default=None, example="1", description="It's enum, 1 -- RU, 2 -- ENG")


class UserUpdateNotSafe(BaseModel):
    email: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    is_staff: Optional[bool] = Field(default=False, description="Moderator")
    repeat_password: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)

    _validate_passwords = validator("password", allow_reuse=True)(validate_password)
    _validate_email = validator("email", pre=True, allow_reuse=True)(validate_email)


class UserTransactionEvents(IntEnum):
    DEPOSIT = 1
    WITHDRAW = 2


class UserTransactionStatus(IntEnum):
    IN_PROGRESS = 1
    CANCELLED = 2
    DONE = 3


class UserTransaction(BaseModel):
    date: datetime = Field(default=None)
    event: UserTransactionEvents = Field(default=None, description="1 -- DEPOSIT, 2 -- WITHDRAW")
    address: str = Field(default=None)
    amount_usdt: float = Field(default=None)
    status: UserTransactionStatus = Field(default=None, description="1 -- IN_PROGRESS, 2 -- CANCELLED, 3 -- DONE")


class UserMakeWithdraw(BaseModel):
    amount: float = Field(...)
    to: str = Field(...)

    _validate_withdraw_amount = validator("amount", allow_reuse=True)(validate_withdraw_amount)


class UserAdminView(User):
    contract_balance: Optional[Decimal] = Field(default=None)
    ethereum_balance: Optional[Decimal] = Field(default=None)
