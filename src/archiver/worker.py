from celery import Celery
from archiver.config import Config
from archiver.factories import get_archiver_instance
from archiver.schemas import RequestModel, ResponseModel

celery_app = Celery("archiver", broker=Config.CELERY_BROKER_URL)


@celery_app.task(name="archiver.tasks.collect")
def collect(event: dict) -> None:

    archiver = get_archiver_instance()

    if event["type"] == "response":
        archiver.store(ResponseModel(**event))
    if event["type"] == "request":
        archiver.store(RequestModel(**event))
