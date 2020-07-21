from typing import Optional, Union
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException
from http import HTTPStatus
import logging
from sentry_sdk import capture_message

from database.crud.base import BaseMongoCRUD
from core.utils import to_objectid

from core.utils.binance import BinanceRate

from schemas.user import (
    User,
)


__all__ = ["CurrencyCRUD"]


class CurrencyCRUD(BaseMongoCRUD):
    collection: str = "currency"

    @classmethod
    async def find_by_id(cls, _id: str) -> Optional[dict]:
        return await super().find_one(query={"_id": to_objectid(_id)}) if _id else None

    @classmethod
    async def find_last(cls) -> Optional[dict]:
        return await super().find_one(query={})

    @classmethod
    async def update(cls, new_currency: Optional[float]) -> None:
        if not new_currency:
            capture_message("ERROR WHILE UPDATE USDT RATE, USING OLD ONE")
            return None
        current_rate = await cls.find_last()
        logging.info(new_currency)
        if not current_rate:
            await cls.insert_one(payload={
                "current_rate": new_currency,
                "updated_at": datetime.now(),
                "created_at": datetime.now()
            })
        else:
            current_rate["current_rate"] = new_currency
            current_rate["updated_at"] = datetime.now()

            await cls.update_one(query={}, payload={**current_rate})
