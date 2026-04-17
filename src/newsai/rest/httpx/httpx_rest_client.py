from typing import Any, TypeVar, cast

import httpx
from pydantic import BaseModel

from newsai.core.interfaces.rest_client import Data, Files, Json, RestClient
from newsai.core.responses.rest_response import RestResponse

Body = TypeVar("Body")


class HttpxRestClient(RestClient):
    def __init__(
        self,
        base_url: str = "",
        timeout: float = 30.0,
        headers: Json | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._headers = dict(headers or {})

    def get[Body](
        self,
        path: str,
        response_model: type[Body],
        query_params: Json | None = None,
        timeout: float | None = None,
    ) -> RestResponse[Body]:
        return self._request(
            method="GET",
            path=path,
            response_model=response_model,
            query_params=query_params,
            timeout=timeout,
        )

    def post[Body](
        self,
        path: str,
        response_model: type[Body],
        body: Any | None = None,
        query_params: Json | None = None,
        data: Data | None = None,
        files: Files | None = None,
        timeout: float | None = None,
    ) -> RestResponse[Body]:
        return self._request(
            method="POST",
            path=path,
            response_model=response_model,
            body=body,
            query_params=query_params,
            data=data,
            files=files,
            timeout=timeout,
        )

    def put[Body](
        self,
        path: str,
        response_model: type[Body],
        body: Any | None = None,
        query_params: Json | None = None,
        data: Data | None = None,
        files: Files | None = None,
        timeout: float | None = None,
    ) -> RestResponse[Body]:
        return self._request(
            method="PUT",
            path=path,
            response_model=response_model,
            body=body,
            query_params=query_params,
            data=data,
            files=files,
            timeout=timeout,
        )

    def patch[Body](
        self,
        path: str,
        response_model: type[Body],
        body: Any | None = None,
        query_params: Json | None = None,
        data: Data | None = None,
        files: Files | None = None,
        timeout: float | None = None,
    ) -> RestResponse[Body]:
        return self._request(
            method="PATCH",
            path=path,
            response_model=response_model,
            body=body,
            query_params=query_params,
            data=data,
            files=files,
            timeout=timeout,
        )

    def delete[Body](
        self,
        path: str,
        response_model: type[Body],
        body: Any | None = None,
        query_params: Json | None = None,
        data: Data | None = None,
        files: Files | None = None,
        timeout: float | None = None,
    ) -> RestResponse[Body]:
        return self._request(
            method="DELETE",
            path=path,
            response_model=response_model,
            body=body,
            query_params=query_params,
            data=data,
            files=files,
            timeout=timeout,
        )

    def get_base_url(self) -> str:
        return self._base_url

    def set_base_url(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")

    def set_header(self, key: str, value: str) -> None:
        self._headers[key] = value

    def _request[Body](
        self,
        method: str,
        path: str,
        response_model: type[Body],
        body: Any | None = None,
        query_params: Json | None = None,
        data: Data | None = None,
        files: Files | None = None,
        timeout: float | None = None,
    ) -> RestResponse[Body]:
        url = self._build_url(path)

        print(self._headers)

        try:
            with httpx.Client(
                headers=self._headers, timeout=timeout or self._timeout
            ) as client:
                response = client.request(
                    method=method,
                    url=url,
                    params=query_params,
                    json=body,
                    data=data,
                    files=files,
                )
        except httpx.HTTPError as exception:
            return RestResponse(error_message=str(exception), status_code=500)

        if response.is_error:
            return RestResponse(
                error_message=response.text, status_code=response.status_code
            )

        parsed_body = self._parse_response_body(response, response_model)
        return RestResponse(body=parsed_body, status_code=response.status_code)

    def _build_url(self, path: str) -> str:
        if path.startswith(("http://", "https://")):
            return path
        return f"{self._base_url}/{path.lstrip('/')}"

    def _parse_response_body[Body](
        self, response: httpx.Response, response_model: type[Body]
    ) -> Body:
        if response_model is type(None):
            return cast(Body, None)

        payload = response.json()
        if issubclass(response_model, BaseModel):
            return cast(Body, response_model.model_validate(payload))

        return cast(Body, payload)
