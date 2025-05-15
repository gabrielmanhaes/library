from celery import Celery
from celery.schedules import crontab
from .config import CELERY_CONFIG

app = Celery("scheduler")
app.config_from_object(CELERY_CONFIG)

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    # "hermes-gather-every-minute": {
    #     "task": "hermes.gather",
    #     "schedule": crontab(),
    #     "args": (),
    # },
    # "hermes-poll-every-minute": {
    #     "task": "hermes.poll",
    #     "schedule": crontab(),
    #     "args": (),
    # },
}
