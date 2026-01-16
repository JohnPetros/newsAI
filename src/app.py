from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from errors import AppError
from rest.router import Router
from messaging.inngest_messaging import InngestMessaging
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

    InngestMessaging.register(app)

    app.add_exception_handler(AppError, ExceptionHandler.handle)

    app.include_router(Router.register())

    return app
