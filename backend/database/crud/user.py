import asyncio
from datetime import datetime
from http import HTTPStatus
from passlib import pwd
from typing import Optional, List
from datetime import timedelta
from bson import Decimal128

from fastapi.exceptions import HTTPException

from .base import ObjectId
from database.crud.base import BaseMongoCRUD
from database.crud.ethereum_wallet import EthereumWalletCRUD
from database.crud.transaction import USDTTransactionCRUD
from core.integrations.crypto import USDTWrapper
from core.utils.jwt import decode_jwt_token, encode_jwt_token
from core.utils.email import MailGunEmail
from schemas.user import (
    User,
    UserCreationSafe,
    pwd_context,
    UserChangePassword,
    UserRecover,
    UserRecoverLink,
    UserUpdate,
    UserTransaction,
    UserTransactionEvents,
    UserTransactionStatus
)

__all__ = ["UserCRUD"]

FIELDS_TO_EXCLUDE = ("repeat_password",)


class UserCRUD(BaseMongoCRUD):
    collection: str = "users"

    @classmethod
    async def find_by_email(cls, email: str) -> Optional[dict]:
        return await super().find_one(query={"email": email}) if email else None

    @classmethod
    async def find_by_username(cls, username: str) -> Optional[dict]:
        return (
            await super().find_one(query={"username": username}) if username else None
        )

    @classmethod
    async def authenticate(cls, email: str, password: str) -> dict:
        email = email.lower()

        user = await super().find_one(query={"email": email})

        if user and pwd_context.verify(password, user["password"]):
            token = encode_jwt_token({"id": str(user["_id"])})
            if not user.get("is_active"):
                raise HTTPException(HTTPStatus.BAD_REQUEST, "Активируйте аккаунт через email для входа в аккаунт")
            return {"token": token, "user": User(**user).dict()}
        else:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Неправильно введены данные")

    @classmethod
    async def autenticate_by_token(cls, token: str) -> Optional[dict]:
        token_data = decode_jwt_token(token)
        user_id = token_data.get("id") if token_data else None
        return await cls.find_by_id(user_id) if user_id else None

    @classmethod
    async def verify(cls, email: str, verification_code: str) -> dict:
        email = email.lower()

        user = await cls.find_by_email(email)

        if not user:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Пользователи с таки email нет")
        if user.get("is_active"):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Пользователь уже верифицирован")

        if user["verification_code"] == verification_code:
            user["is_active"] = True
        else:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Неправильный код")

        user["verification_code"] = None

        await cls.update_one(
            query={"_id": user["_id"]},
            payload={
                "verification_code": user["verification_code"],
                "is_active": user["is_active"],
            },
        )
        keys = {"password", "repeat_password", "verification_code", "_id"}
        return {
            "token": encode_jwt_token({"id": user["_id"]}),
            "user": {x: user[x] for x in user if x not in keys},
        }

    @classmethod
    async def create_safe(cls, user: UserCreationSafe, **kwargs) -> bool:
        if await cls.find_by_email(user.email):
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, "Пользователь с таким email уже существует",
            )

        if await cls.find_by_username(user.username):
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, "Пользователь с таким именем уже существует",
            )

        eth_wallet, private_key, entropy = await USDTWrapper().create_wallet()
        await EthereumWalletCRUD.create_wallet(eth_wallet, private_key, entropy)
        # create ethereum wallet for user

        verification_code = pwd.genword()

        inserted_id = (
            await cls.insert_one(
                payload={
                    **user.dict(exclude=set(FIELDS_TO_EXCLUDE)),
                    "created_at": datetime.now(),
                    "verification_code": verification_code,
                    "is_active": False,
                    "eth_address": eth_wallet,
                    "balance_usdt": 0.0,
                    "usdt_in_invoices": 0.0
                }
            )
        ).inserted_id

        asyncio.create_task(
            MailGunEmail().send_verification_code(user.email, verification_code)
        )

        return True

    @classmethod
    async def change_password(cls, user: User, payload: UserChangePassword) -> bool:
        old_password_obj = await cls.find_one({"_id": user.id})

        if not pwd_context.verify(payload.old_password, old_password_obj["password"]):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Неверный пароль")

        await cls.update_one(
            query={"_id": user.id}, payload={"password": payload.password}
        )

        return True

    @classmethod
    async def recover_send(cls, payload: UserRecover):
        user = await cls.find_by_email(payload.email)

        if not user:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Такого пользователя нет")

        recover_code = encode_jwt_token({"_id": user["_id"]}, timedelta(hours=3))

        await cls.update_one({"_id": user["_id"]}, {"recover_code": recover_code})
        asyncio.create_task(MailGunEmail().send_recover_code(user["email"], recover_code))
        return True

    @classmethod
    async def recover(cls, payload: UserRecoverLink):
        data = decode_jwt_token(payload.recover_code)

        if data is None:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Incorrect code")

        user_id = data["_id"]

        user = await cls.find_one({"_id": ObjectId(user_id)})

        if "recover_code" not in user or user["recover_code"] != payload.recover_code:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Неправильный код")

        await cls.update_one(
            query={"_id": user["_id"]}, payload={"password": payload.password, "recover_code": None}
        )

        return True

    @classmethod
    async def update(cls, user: User, payload: UserUpdate):
        await cls.update_one(
            query={
                "_id": user.id
            },
            payload={
                **payload.dict()
            }
        )
        updated_user = await cls.find_by_id(user.id)
        return updated_user

    @classmethod
    async def get_transactions(cls, user: User) -> List[dict]:
        if not user.eth_address:
            return []
        result = []
        transactions = await USDTTransactionCRUD.get_transactions_by_address(user.eth_address)
        for transaction in transactions:
            parsed_trans = {
                "date": transaction.get("date"),
                "event": transaction.get("event"),
                "address": transaction.get("to_adr") if user.eth_address != transaction.get(
                    "to_adr") else transaction.get("from_adr"),
                "amount_usdt": float(transaction.get("usdt_amount").to_decimal()) * 0.000001,
                "status": UserTransactionStatus.DONE  # TODO change when doing withdraw
            }
            result.append(parsed_trans)
        return sorted(result, key=lambda i: i["date"], reverse=True)
