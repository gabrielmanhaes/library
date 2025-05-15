from librarian.config import Config


CELERY_CONFIG = {
    "broker_url": Config.CELERY_BROKER_URL,
    "result_backend": Config.CELERY_BROKER_URL,
    "task_default_queue": "hermes",
    "task_routes": {
        "hermes.*": {"queue": "hermes"},
    },
    "task_queues": {
        "hermes": {
            "exchange": "hermes",
            "routing_key": "hermes",
        },
    },
}
