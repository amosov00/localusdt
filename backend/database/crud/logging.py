from schemas.logging import Log, LogEvents
from database.crud.base import BaseMongoCRUD


__all__ = [
    "LogCRUD"
]


class LogCRUD(BaseMongoCRUD):
    collection = "logs"
