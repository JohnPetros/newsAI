from typing import Any, Protocol

from newsai.core.responses.rest_response import RestResponse


type Json = dict[str, Any]
type Data = dict[str, Any]
type Files = dict[str, tuple[str, Any, str]]


class RestClient(Protocol):
    def get[Body](
        self,
        path: str,
        response_model: type[Body],
        query_params: Json | None = None,
        timeout: float | None = None,
    ) -> RestResponse[Body]: ...

    def post[Body](
        self,
        path: str,
        response_model: type[Body],
        body: Any | None = None,
        query_params: Json | None = None,
        data: Data | None = None,
        files: Files | None = None,
        timeout: float | None = None,
    ) -> RestResponse[Body]: ...

    def put[Body](
        self,
        path: str,
        response_model: type[Body],
        body: Any | None = None,
        query_params: Json | None = None,
        data: Data | None = None,
        files: Files | None = None,
        timeout: float | None = None,
    ) -> RestResponse[Body]: ...

    def patch[Body](
        self,
        path: str,
        response_model: type[Body],
        body: Any | None = None,
        query_params: Json | None = None,
        data: Data | None = None,
        files: Files | None = None,
        timeout: float | None = None,
    ) -> RestResponse[Body]: ...

    def delete[Body](
        self,
        path: str,
        response_model: type[Body],
        body: Any | None = None,
        query_params: Json | None = None,
        data: Data | None = None,
        files: Files | None = None,
        timeout: float | None = None,
    ) -> RestResponse[Body]: ...

    def get_base_url(self) -> str: ...

    def set_base_url(self, base_url: str) -> None: ...

    def set_header(self, key: str, value: str) -> None: ...
