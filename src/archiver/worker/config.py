from archiver.config import Config


CELERY_CONFIG = {
    "broker_url": Config.CELERY_BROKER_URL,
    "result_backend": Config.CELERY_BROKER_URL,
    "task_default_queue": "merlin",
    "task_routes": {
        "merlin.*": {"queue": "merlin"},
    },
    "task_queues": {
        "merlin": {
            "exchange": "merlin",
            "routing_key": "merlin",
        },
    },
}
