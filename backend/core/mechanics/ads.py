from typing import Union

from schemas.ads import AdsInDB
from schemas.user import User


class InvoiceMechanics:
    def __init__(self, ads: Union[dict, AdsInDB], user: Union[dict, User] = None):
        if isinstance(ads, dict):
            ads = AdsInDB(**ads)

        if user and isinstance(user, dict):
            user = User(**user)

        self.ads = ads
        self.user = user
        self.errors = []
