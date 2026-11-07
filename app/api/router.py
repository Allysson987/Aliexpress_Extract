from fastapi import APIRouter

from app.api.v1.endpoints import aliexpress

api_router = APIRouter()

api_router.include_router(aliexpress.router)