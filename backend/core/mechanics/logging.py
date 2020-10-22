from database.crud.logging import LogCRUD
from schemas.logging import *

from datetime import datetime


__all__ = [
    "LogMechanics"
]


class LogMechanics:

    @staticmethod
    async def new_log(event: LogEvents, **kwargs) -> None:
        """
        Build new log depends on kwargs
        :param event:
        :param kwargs:
        :return:
        """
        new_log = Log(
            **kwargs,
            event=event,
            created_at=datetime.utcnow(),
        )
        await LogCRUD.insert_one(new_log.dict())
