from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.responses import JSONResponse
from starlette.types import ASGIApp
from starlette.middleware.base import RequestResponseEndpoint

from newsai.constants import ENV, HTTP_HEADERS


class VerifyApiKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        if request.method == "OPTIONS":
            return await call_next(request)

        api_key = request.headers.get(HTTP_HEADERS.pulo_do_gato_news_api_key)
        if api_key != ENV.pulo_do_gato_news_api_key:
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

        return await call_next(request)
