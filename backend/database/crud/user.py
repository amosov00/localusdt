import asyncio
from datetime import datetime
from http import HTTPStatus
from passlib import pwd
from typing import Optional, List
from datetime import timedelta
from decimal import Decimal

from fastapi.exceptions import HTTPException
from fastapi import Request

from .base import ObjectId
from database.crud.base import BaseMongoCRUD
from database.crud.ethereum_wallet import EthereumWalletCRUD
from database.crud.transaction import USDTTransactionCRUD
from core.integrations.crypto import USDTWrapper
from core.utils.jwt import decode_jwt_token, encode_jwt_token
from core.utils.email import MailGunEmail
from core.utils import IPApiWrapper
from schemas.user import (
    User,
    UserCreationSafe,
    pwd_context,
    UserChangePassword,
    UserRecover,
    UserRecoverLink,
    UserUpdate,
    UserLanguage
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
    async def update_user_location(cls, ip: str, user_id: ObjectId):
        location = await IPApiWrapper().get_location(ip)

        if not location:
            return

        await cls.update_one(
            {"_id": user_id},
            {
                "location": {
                    "country_name": location.get("country_name"),
                    "country_code": location.get("country_code"),
                    "region": location.get("region"),
                }
            }
        )

    @classmethod
    async def authenticate(cls, email: str, password: str, ip: str) -> dict:
        email = email.lower()

        user = await super().find_one(query={"email": email})

        if user and pwd_context.verify(password, user["password"]):
            token = encode_jwt_token({"id": str(user["_id"])})
            if not user.get("is_active"):
                raise HTTPException(HTTPStatus.BAD_REQUEST, "activate email or you are blocked")
            asyncio.create_task(cls.update_user_location(ip, user.get("_id")))
            return {"token": token, "user": user}
        else:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "wrong input")

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
            raise HTTPException(HTTPStatus.BAD_REQUEST, "???????????????????????? ?? ???????? email ??????")
        if user.get("is_active"):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "???????????????????????? ?????? ??????????????????????????")

        if user["verification_code"] == verification_code:
            user["is_active"] = True
        else:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "???????????????????????? ??????")

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
                HTTPStatus.BAD_REQUEST, "???????????????????????? ?? ?????????? email ?????? ????????????????????",
            )

        if await cls.find_by_username(user.username):
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, "???????????????????????? ?? ?????????? ???????????? ?????? ????????????????????",
            )

        eth_wallet, private_key, entropy = await USDTWrapper().create_wallet()
        await EthereumWalletCRUD.create_wallet(eth_wallet.lower(), private_key, entropy)
        # create ethereum wallet for user

        verification_code = pwd.genword()

        inserted_id = (
            await cls.insert_one(
                payload={
                    **user.dict(exclude=set(FIELDS_TO_EXCLUDE)),
                    "created_at": datetime.now(),
                    "verification_code": verification_code,
                    "is_active": False,
                    "eth_address": eth_wallet.lower(),
                    "balance_usdt": 0.0,
                    "usdt_in_invoices": 0.0,
                    "is_staff": False,
                    "is_superuser": False
                }
            )
        ).inserted_id

        asyncio.create_task(
            MailGunEmail(user.language).send_verification_code(user.email, verification_code)
        )

        return inserted_id

    @classmethod
    async def change_password(cls, user: User, payload: UserChangePassword) -> bool:
        old_password_obj = await cls.find_one({"_id": user.id})

        if not pwd_context.verify(payload.old_password, old_password_obj["password"]):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "???????????????? ????????????")

        await cls.update_one(
            query={"_id": user.id}, payload={"password": payload.password}
        )

        return True

    @classmethod
    async def recover_send(cls, payload: UserRecover):
        user = await cls.find_by_email(payload.email)

        if not user:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "???????????? ???????????????????????? ??????")

        recover_code = encode_jwt_token({"_id": user["_id"]}, timedelta(hours=3))

        await cls.update_one({"_id": user["_id"]}, {"recover_code": recover_code})
        asyncio.create_task(MailGunEmail(user.get("language")).send_recover_code(user["email"], recover_code))
        return True

    @classmethod
    async def recover(cls, payload: UserRecoverLink):
        data = decode_jwt_token(payload.recover_code)

        if data is None:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Incorrect code")

        user_id = data["_id"]

        user = await cls.find_one({"_id": ObjectId(user_id)})

        if "recover_code" not in user or user["recover_code"] != payload.recover_code:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "???????????????????????? ??????")

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
                **payload.dict(exclude_unset=True, exclude_none=True)
            }
        )
        updated_user = await cls.find_by_id(user.id)
        return updated_user

    @classmethod
    async def get_transactions(cls, user: User) -> List[dict]:
        if not user.eth_address:
            return []
        result = []
        transactions = await USDTTransactionCRUD.get_transactions_by_address(user)
        for transaction in transactions:
            parsed_trans = {
                "date": transaction.get("date"),
                "event": transaction.get("event"),
                "address": transaction.get("to_adr") if user.eth_address != transaction.get(
                    "to_adr") else transaction.get("from_adr"),
                "amount_usdt": float(transaction.get("usdt_amount").to_decimal()) * 0.000001,
                "status": transaction.get("status")
            }
            result.append(parsed_trans)
        return sorted(result, key=lambda i: i["date"], reverse=True)

    @classmethod
    async def set_online(cls, user: User) -> None:
        await cls.update_one(
            query={
                "_id": user.id
            },
            payload={
                "last_active": datetime.utcnow()
            }
        )

    @classmethod
    async def make_withdraw(cls, user: User, payload):
        if user.balance_usdt < payload.amount:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Not enough for transaction")

        await cls.update_one(
            query={"_id": user.id},
            payload={"balance_usdt": user.balance_usdt - payload.amount}
        )
        return await USDTWrapper().withdraw(user, payload.to, Decimal(payload.amount * 1000000))

