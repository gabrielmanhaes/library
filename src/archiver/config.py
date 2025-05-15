import os
import logging
from dotenv import load_dotenv
from archiver.utils import load_blocklist

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("archiver")


class Config:
    VERSION = os.getenv("ARCHIVER_VERSION")
    PORT = int(os.getenv("ARCHIVER_PORT", "8001"))
    CONTAINER = os.getenv("CONTAINER", "false")
    DEBUG = os.getenv("DEBUG", "false")
    BLOCKER_URL = os.getenv(
        "BLOCKER_URL",
        "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/pro-onlydomains.txt",
    )
    POSTGRES_DB = os.getenv("POSTGRES_DB", "library")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "library")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "librarian")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "<yourpassword>")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    BLOCKLIST = load_blocklist(BLOCKER_URL)
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")
    REDIS_DB = os.getenv("REDIS_DB", "0")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "<yourpassword>")
    CELERY_BROKER_URL = (
        f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    )
    MAX_METHOD_LENGTH = 64
    MAX_URL_LENGTH = 2048
    MAX_PATH_LENGTH = 2048
    MAX_BODY_LENGTH = 1024 * 1024 * 10  # 10 MB
    MAX_RAW_CONTENT_LENGTH = 1024 * 1024 * 10  # 10 MB
    MAX_HEADERS_LENGTH = 1024 * 1024 * 10  # 10 MB
    MAX_TRAILERS_LENGTH = 1024 * 1024 * 10  # 10 MB
