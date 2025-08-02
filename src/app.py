from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from errors import AppError
from rest.router import register_router


def http_exception_handler(_: Request, exception: Exception) -> JSONResponse:
    if isinstance(exception, AppError):
        return JSONResponse(
            status_code=500,
            content={"title": exception.title, "message": exception.message},
        )

    return JSONResponse(
        status_code=500,
        content={"title": "Error", "message": str(exception)},
    )


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

    app.add_exception_handler(AppError, http_exception_handler)

    app.include_router(router)

    return app
