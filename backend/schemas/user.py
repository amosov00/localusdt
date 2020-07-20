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
]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_email(v: str) -> str:
    return v.lower() if v else v


def validate_password(v: Optional[str], values: dict) -> str:
    if len(v) < 8:
        raise ValueError("password should be longer than 8 characters")
    if "repeat_password" in values and v != values["repeat_password"]:
        raise ValueError("passwords do not match")
    return pwd_context.hash(v)


class BaseUser(BaseModel):
    pass


class User(BaseModel):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
    email: str = Field(...)
    username: str = Field(...)
    balance: float = Field(default=0)
    eth_address: Optional[str] = Field(default=None)
    current_state: Optional[int] = Field(
        default=None, description="1 - green, 2 - orange, 3 - red"
    )
    is_active: Optional[bool] = Field(default=True, description="User is active")
    verification_code: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)

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


class UserCreationNotSafe(BaseModel):
    email: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    ethereum_wallet: Optional[str] = Field(default=None)
    repeat_password: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)

    _validate_email = validator("email", pre=True, allow_reuse=True)(validate_email)
    _validate_passwords = validator("password", allow_reuse=True)(validate_password)
