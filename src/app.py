from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rest.router import register_router


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    router = register_router()

    app.include_router(router)

    return app
