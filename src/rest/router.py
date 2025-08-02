from fastapi import APIRouter

from rest.controllers import CheckApiHealthController, CreatePostController


def register_router() -> APIRouter:
    router = APIRouter()

    CheckApiHealthController(router)
    CreatePostController(router)

    return router
