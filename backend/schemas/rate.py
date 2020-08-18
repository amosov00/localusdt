from typing import Optional, List
from datetime import datetime
from pydantic import Field

from schemas.base import BaseModel, ObjectIdPydantic

__all__ = [

]


class USDTRate(BaseModel):
    current_rate: float = Field(default=None, description="Current USDT rate")
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class USDTRateInDB(USDTRate):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")
