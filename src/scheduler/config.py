import os
import logging
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("chronos")


class Config:
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")
    REDIS_DB = os.getenv("REDIS_DB", "0")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "<yourpassword>")
    CELERY_BROKER_URL = (
        f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    )


CELERY_CONFIG = {
    "broker_url": Config.CELERY_BROKER_URL,
    "result_backend": Config.CELERY_BROKER_URL,
    "task_routes": {
        "hermes.*": {"queue": "hermes"},
        "merlin.*": {"queue": "merlin"},
    },
    "task_queues": {
        "hermes": {
            "exchange": "hermes",
            "routing_key": "hermes",
        },
        "merlin": {
            "exchange": "merlin",
            "routing_key": "merlin",
        },
    },
}
