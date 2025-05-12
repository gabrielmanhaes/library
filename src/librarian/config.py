import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("librarian")

class Config:
    VERSION = os.getenv("LIBRARIAN_VERSION")
    API_KEY = os.getenv("LIBRARIAN_API_KEY")
    MODEL = os.getenv("LIBRARIAN_MODEL", "o4-mini")
    PORT = int(os.getenv("LIBRARIAN_PORT", "8000"))
    CONTAINER = os.getenv("CONTAINER", "false")
    DEBUG = os.getenv("DEBUG", "false")
