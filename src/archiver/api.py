from archiver.worker import collect as _collect
from fastapi import APIRouter, BackgroundTasks
from archiver.dependencies import APIArchiver
from archiver.schemas import RequestModel, ResponseModel

api_router = APIRouter()


@api_router.post("/collect")
def collect(
    request: RequestModel | ResponseModel,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(_collect.delay, request.model_dump())
    return {"status": "queued"}
