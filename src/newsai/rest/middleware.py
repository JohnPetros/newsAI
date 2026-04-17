from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from newsai.constants import ENV, HTTP_HEADERS


class Middleware:
    @staticmethod
    def verify_api_key(
        api_key: str = Depends(
            APIKeyHeader(name=HTTP_HEADERS.pulo_do_gato_news_api_key, auto_error=False)
        ),
    ) -> str:
        if api_key != ENV.pulo_do_gato_news_api_key:
            raise HTTPException(status_code=401, detail="Unauthorized")

        return api_key
