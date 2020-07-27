from celery import Celery
from celery.schedules import crontab

import celery_decorator_taskcls # noqa
import celery_pool_asyncio  # noqa

celery_pool_asyncio.__package__  # noqa

from config import *

__all__ = ["app"]

celery_decorator_taskcls.patch_celery()

CELERY_MONGO_DATABASE_URL = f"{MONGO_DATABASE_URL}{CELERY_DATABASE_NAME}"

app = Celery(main="celery_main", broker=CELERY_BROKER_URL, backend=CELERY_MONGO_DATABASE_URL,)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=True,
    imports=["celery_app.tasks"],
)

app.conf.beat_schedule = {
    "update_usdt_rate": {
        "task": "update_usdt_rate",
        "schedule": crontab(minute="*/5"),
        "args": (),
    },
    "update_contacts_status":{
        "task": "update_contacts_status",
        "schedule": crontab(minute="*/1"),
        "args": (),
    }
}
