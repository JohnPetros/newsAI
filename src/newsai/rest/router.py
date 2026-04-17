from fastapi import APIRouter

from newsai.rest.controllers import (
    CheckApiHealthController,
    GeneratePostController,
    UpdatePostTitleAndReviewController,
)


class Router:
    @staticmethod
    def register() -> APIRouter:
        router = APIRouter()

        CheckApiHealthController.handle(router)
        GeneratePostController.handle(router)
        UpdatePostTitleAndReviewController.handle(router)

        return router
