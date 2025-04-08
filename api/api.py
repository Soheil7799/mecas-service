from api.routers import stream, upload, filters
from fastapi import APIRouter
api_router = APIRouter()
api_router.include_router(upload.router)
api_router.include_router(stream.router)
api_router.include_router(filters.router)

