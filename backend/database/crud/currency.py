from typing import Optional, Union
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException
from http import HTTPStatus
import logging
from sentry_sdk import capture_message

from database.crud.base import BaseMongoCRUD
from core.utils import to_objectid

from schemas.currency import Currency, CurrencyType

from schemas.user import (
    User,
)


__all__ = ["CurrencyCRUD"]


class CurrencyCRUD(BaseMongoCRUD):
    collection: str = "currency"

    @classmethod
    async def find_last(cls, cur_type: CurrencyType) -> Optional[dict]:
        return await super().find_one(query={"type": cur_type})

    @classmethod
    async def update(cls, cur_type: CurrencyType, new_currency: Optional[float]) -> None:
        if not new_currency:
            capture_message(f"ERROR WHILE UPDATE {cur_type.name} RATE, USING OLD ONE")
            return None
        current_rate = await cls.find_last(cur_type)
        if not current_rate:
            await cls.insert_one(payload={
                "type": cur_type,
                "current_rate": new_currency,
                "updated_at": datetime.now(),
                "created_at": datetime.now()
            })
        else:
            current_rate["current_rate"] = new_currency
            current_rate["updated_at"] = datetime.now()

            await cls.update_one(query={"type": cur_type}, payload={**current_rate})
