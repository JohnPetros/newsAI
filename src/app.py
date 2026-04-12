from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.errors import AppError
from rest.router import Router
from pubsub.inngest_pubsub import InngestPubSub
from exception_handler import ExceptionHandler


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    InngestPubSub.register(app)

    app.add_exception_handler(AppError, ExceptionHandler.handle)

    app.include_router(Router.register())

    return app
