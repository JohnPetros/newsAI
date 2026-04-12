from fastapi.responses import JSONResponse
from fastapi import Request

from newsai.core.errors import AppError


class ExceptionHandler:
    @staticmethod
    def handle(_: Request, exception: Exception) -> JSONResponse:
        if isinstance(exception, AppError):
            return JSONResponse(
                status_code=500,
                content={"title": exception.title, "message": exception.message},
            )

        return JSONResponse(
            status_code=500,
            content={"title": "Error", "message": str(exception)},
        )
