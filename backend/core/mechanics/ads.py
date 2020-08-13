from fastapi import HTTPException
from http import HTTPStatus
from datetime import datetime
from typing import Union

from database.crud.user import UserCRUD

from schemas.ads import AdsCreate, AdsInDB, AdsType, Ads
from schemas.user import User


__all__ = ["AdsMechanics"]


class AdsMechanics:
    def __init__(self, ads: Union[dict, AdsInDB] = None, user: Union[dict, User] = None):
        if isinstance(ads, dict):
            ads = AdsInDB(**ads)

        if user and isinstance(user, dict):
            user = User(**user)

        self.ads = ads
        self.user = user

    @staticmethod
    async def get_created_ads(payload: AdsCreate, user: User) -> Ads:
        if payload.type == AdsType.SELL:
            if user.balance_usdt < payload.amount_usdt:
                raise HTTPException(HTTPStatus.BAD_REQUEST, "Not enough USDT")
            await UserCRUD.update_one(
                query={
                    "_id": user.id
                },
                payload={
                    "balance_usdt": user.balance_usdt - payload.amount_usdt,
                    "usdt_in_invoices": user.usdt_in_invoices + payload.amount_usdt
                }
            )

        ads = Ads(
            **payload.dict(),
            user_id=user.id,
            created_at=datetime.now()
        )

        return ads
