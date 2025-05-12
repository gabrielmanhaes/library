from fastapi import APIRouter
from archiver.api import api_router

def get_routers():
    router = APIRouter()
    router.include_router(api_router, prefix="/api")
    return router
