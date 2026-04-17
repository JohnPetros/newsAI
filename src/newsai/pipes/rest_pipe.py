from http import HTTPStatus
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from newsai.core.interfaces.blog_service import BlogService
from newsai.constants import ENV, HTTP_HEADERS
from newsai.rest.httpx.httpx_rest_client import HttpxRestClient
from newsai.rest.services.pulo_do_gato_news_blog_service import (
    PuloDoGatoNewsBlogService,
)


class RestPipe:
    @staticmethod
    def verify_api_key(
        api_key: str = Depends(
            APIKeyHeader(
                name=HTTP_HEADERS.pulo_do_gato_news_api_key,
                auto_error=False,
            )
        ),
    ) -> str:
        if api_key != ENV.pulo_do_gato_news_api_key:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorized"
            )

        return api_key

    @staticmethod
    def get_blog_service() -> BlogService:
        rest_client = HttpxRestClient(base_url=ENV.blog_api_url)
        rest_client.set_header(
            HTTP_HEADERS.pulo_do_gato_news_api_key,
            ENV.pulo_do_gato_news_api_key,
        )
        return PuloDoGatoNewsBlogService(rest_client)
