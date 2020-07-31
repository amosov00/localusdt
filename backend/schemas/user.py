import re
from typing import Optional
from datetime import datetime

from pydantic import Field, validator
from passlib.context import CryptContext

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
    "UserUpdate"
]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_email(v: str) -> str:
    return v.lower() if v else v


def validate_password(v: Optional[str], values: dict) -> str:
    if len(v) < 8:
        raise ValueError("password should be longer than 8 characters")
    if "repeat_password" in values and v != values["repeat_password"]:
        raise ValueError("passwords do not match")
    if not bool(re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", v)): # noqa
        raise ValueError(
            "password does not match password policy (at least one uppercase letter, one lowercase, one number)"
        )
    return pwd_context.hash(v)


def validate_username(v: Optional[str], values: dict) -> str:
    if len(v) < 6:
        raise ValueError("username should be longer than 6 characters")
    if not bool(re.match("^(?=[a-zA-Z0-9._]{6,20}$)(?!.*[_.]{2})[^_.].*[^_.]$", v)): # noqa
        raise ValueError(
            "username does not match username policy (contains only alphabetic, underline and dots)"
        )
    return v


class BaseUser(BaseModel):
    pass


class User(BaseModel):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
    email: str = Field(...)
    username: str = Field(...)
    balance_usdt: float = Field(default=0)
    usdt_in_invoices: float = Field(default=0)
    eth_address: Optional[str] = Field(default=None)
    current_state: Optional[int] = Field(
        default=None, description="1 - green, 2 - orange, 3 - red"
    )
    is_active: Optional[bool] = Field(default=True, description="User is active")
    verification_code: Optional[str] = Field(default=None)
    recover_code: Optional[str] = Field(default=None, description="JWT token for password recover")
    created_at: Optional[datetime] = Field(default=None)
    about_me: str = Field(default="", description="About me field")

    @property
    def is_authenticated(self):
        return True

    @property
    def display_name(self):
        return self.username


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

    _validate_email = validator("email", allow_reuse=True)(validate_email)
    _validate_passwords = validator("password", allow_reuse=True)(validate_password)
    _validate_username = validator("username", allow_reuse=True)(validate_username)


class UserCreationNotSafe(BaseModel):
    email: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    ethereum_wallet: Optional[str] = Field(default=None)
    repeat_password: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)

    _validate_email = validator("email", pre=True, allow_reuse=True)(validate_email)
    _validate_passwords = validator("password", allow_reuse=True)(validate_password)


class UserRecover(BaseModel):
    email: str = Field(...)


class UserRecoverLink(BaseModel):
    recover_code: str = Field(...)
    password: str = Field(...)
    repeat_password: str = Field(...)

    _validate_passwords = validator("password", allow_reuse=True)(validate_password)


class UserUpdate(BaseModel):
    about_me: str = Field(..., description="'About me' field")
