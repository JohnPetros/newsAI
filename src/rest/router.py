from fastapi import APIRouter

from rest.controllers import CheckApiHealthController, GeneratePostController


class Router:
    @staticmethod
    def register() -> APIRouter:
        router = APIRouter()

        CheckApiHealthController.handle(router)
        GeneratePostController.handle(router)

        return router
