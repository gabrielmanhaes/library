from celery import Celery
from .config import CELERY_CONFIG

app = Celery("merlin")
app.config_from_object(CELERY_CONFIG)
app.autodiscover_tasks(["src.archiver.worker"])
