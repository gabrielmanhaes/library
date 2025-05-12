import os
import logging
from dotenv import load_dotenv

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
    MAX_METHOD_LENGTH = 8
    MAX_URL_LENGTH = 2048
    MAX_PATH_LENGTH = 2048
    MAX_BODY_LENGTH = 1024 * 1024 * 10  # 10 MB
    MAX_RAW_LENGTH = 1024 * 1024 * 10  # 10 MB
    MAX_HEADERS_LENGTH = 1024 * 1024 * 10  # 10 MB

