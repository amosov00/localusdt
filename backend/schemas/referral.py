from pydantic import Field
from typing import Optional
from datetime import datetime

from schemas.base import BaseModel, ObjectIdPydantic


__all__ = [
    "Referral",
    "ReferralInDB",
    "ReferralGeneralInfo"
]


class Referral(BaseModel):
    user_id: ObjectIdPydantic = Field(..., description="User whose referral object is")
    parent_id: Optional[ObjectIdPydantic] = Field(default=None, description="Id for parent in referral-tree")
    level: int = Field(..., description="Referral level")
    income: float = Field(default=0, description="Referral income")
    created_at = Field(default_factory=datetime.utcnow)


class ReferralInDB(Referral):
    id: ObjectIdPydantic = Field(default=None, alias="_id", title="_id")


class ReferralGeneralInfo(Referral):
    referral_count: int = Field(..., description="Count of referrals")
    referral_id: str = Field(..., description="Referral code")
