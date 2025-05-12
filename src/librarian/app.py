import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from librarian.config import Config, logger
from librarian.agent import Librarian
from librarian.routes import get_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Initializing Librarian {Config.VERSION}")
    app.state.librarian = Librarian(
        api_key=Config.API_KEY,
        model=Config.MODEL,
    )
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(get_routers())


def main():
    if Config.CONTAINER == "true" and Config.DEBUG == "false":
        logger.info("Running in container mode")
    else:
        uvicorn.run(
            "librarian.app:app",
            host="0.0.0.0",
            port=Config.PORT,
            reload=Config.DEBUG == "true",
        )
