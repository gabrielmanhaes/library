from archiver.worker.tasks import collect as _collect
from fastapi import APIRouter, BackgroundTasks
from archiver.schemas import TransactionData
from archiver.dependencies import APIArchiver

api_router = APIRouter()


@api_router.post("/collect/")
def collect(
    request: TransactionData,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(_collect.delay, request.model_dump())
    return {"status": "queued"}


@api_router.get("/flows/{flow_id}/")
def get_flow(flow_id: int, archiver: APIArchiver):
    """
    Get flow by ID.
    """
    return archiver.get_flow(flow_id)
