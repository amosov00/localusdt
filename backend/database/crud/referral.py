from typing import Optional
from passlib.pwd import genword
from datetime import datetime
from fastapi import HTTPException
from http import HTTPStatus

from schemas.referral import Referral
from schemas.user import User
from schemas.base import ObjectId
from database.crud.base import BaseMongoCRUD


class ReferralCRUD(BaseMongoCRUD):
    collection = "referral"

    @staticmethod
    async def _get_level(number_of_referrals: int):
        if 0 <= number_of_referrals <= 5:
            return 1
        elif 6 <= number_of_referrals <= 10:
            return 2
        elif 11 <= number_of_referrals <= 15:
            return 3
        elif 16 <= number_of_referrals <= 20:
            return 4
        else:
            return 5

    @classmethod
    async def create_referral(cls, user_id: str, referral_id: Optional[str] = None):
        parent = (
            (await cls.find_one(query={"_id": ObjectId(referral_id)}))
            if referral_id
            else None
        )
        number_of_referrals = (
            len(await cls.find_many({"parent_id": parent.get("_id")}))
            if referral_id
            else 0
        )
        new_referral = Referral(
            user_id=ObjectId(user_id),
            parent_id=parent.get("_id") if referral_id else None,
            level=await cls._get_level(number_of_referrals),
            income=float(0),
            created_at=datetime.utcnow(),
        )
        await cls.insert_one(payload=new_referral.dict())

    @classmethod
    async def _get_referrals_count(cls, referral_in_db: dict) -> int:
        return len(await cls.find_many(query={"parent_id": referral_in_db.get("_id")}))

    @classmethod
    async def get_general_info(cls, user: User):
        referral = await cls.find_one({"user_id": user.id})
        if not referral:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "No referral found")
        count = await cls._get_referrals_count(referral)
        referral["referral_count"] = count
        referral["referral_id"] = str(referral.get("_id"))
        return referral

    @classmethod
    async def accrue_bonuses(cls, user_id: ObjectId, deposit_amount: float):
        referral = await cls.find_one(query={"user_id": user_id})
        percent = 0.005
        while referral is not None and percent > 0:
            if referral.get("user_id") == user_id:
                referral = (
                    await cls.find_one(query={"_id": referral.get("parent_id")})
                    if referral.get("parent_id") is not None
                    else None
                )
                continue
            await cls.update_one(
                query={"_id": referral.get("_id")},
                payload={
                    "income": (
                        referral.get("income") if referral.get("income") else 0.0
                    )
                    + deposit_amount * percent
                },
            )
            referral = (
                await cls.find_one(query={"_id": referral.get("parent_id")})
                if referral.get("parent_id") is not None
                else None
            )
