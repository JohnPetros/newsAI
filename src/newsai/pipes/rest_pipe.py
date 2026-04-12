from newsai.core.interfaces.blog_service import BlogService
from newsai.constants import ENV
from newsai.rest.httpx.httpx_rest_client import HttpxRestClient
from newsai.rest.services.pulo_do_gato_news_blog_service import (
    PuloDoGatoNewsBlogService,
)


class RestPipe:
    @staticmethod
    def get_blog_service() -> BlogService:
        return PuloDoGatoNewsBlogService(HttpxRestClient(base_url=ENV.blog_api_url))
