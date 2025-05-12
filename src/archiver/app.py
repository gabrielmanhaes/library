import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from archiver.config import Config, logger
from archiver.routes import get_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Initializing Archiver {Config.VERSION}")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(get_routers())


def main():
    if Config.CONTAINER == "true" and Config.DEBUG == "false":
        logger.info("Running in container mode")
    else:
        uvicorn.run(
            "archiver.app:app",
            host="0.0.0.0",
            port=Config.PORT,
            reload=Config.DEBUG == "true",
        )
