from fastapi import APIRouter, Request

api_router = APIRouter()

@api_router.post("/collect")
async def collect(request: Request):
    try:
        body = await request.json()
        archiver = request.app.state.archiver
        archiver.store(body)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
