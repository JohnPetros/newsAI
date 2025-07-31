from fastapi import APIRouter

from rest.controllers.create_post_controller import CreatePostController


def register_router() -> APIRouter:
    router = APIRouter()

    CreatePostController(router)

    return router
