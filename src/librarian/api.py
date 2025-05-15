from fastapi import APIRouter, BackgroundTasks
from librarian.worker.tasks import dispatch as _dispatch

api_router = APIRouter()


@api_router.post("/flows/{flow_id}/")
def dispatch(flow_id: int, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(_dispatch.delay, flow_id)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
