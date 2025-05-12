from fastapi import APIRouter, Request

api_router = APIRouter()


@api_router.post("/feed")
def feed(request: Request):
    try:
        body = request.json()
        librarian = request.app.state.librarian
        librarian.feed(body)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
