from fastapi import APIRouter

from diaboli_mundi_back.api.api_v1.endpoints import (
    user, persmission, obituary
)

api_router = APIRouter()
api_router.include_router(user.router, tags=["user"])
api_router.include_router(persmission.router, tags=["permission"])
api_router.include_router(obituary.router, tags=["obituary"])
