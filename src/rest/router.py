from fastapi import APIRouter

from rest.controllers import CheckApiHealthController, GeneratePostController


def register_router() -> APIRouter:
    router = APIRouter()

    CheckApiHealthController(router)
    GeneratePostController(router)

    return router
