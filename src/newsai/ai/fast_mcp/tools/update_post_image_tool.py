from os.path import basename
from urllib.parse import urlparse

import httpx
from fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field

from newsai.pipes.rest_pipe import RestPipe


class Input(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    post_id: str = Field(min_length=1)
    file_url: str = Field(min_length=1)
    alt: str = Field(min_length=1)


class UpdatePostImageTool:
    @staticmethod
    def handle(mcp: FastMCP) -> None:
        @mcp.tool(
            name="update_post_image",
            description=(
                "Updates post image by id using multipart form-data with file and alt text."
            ),
        )
        def _(
            post_id: str,
            file_url: str,
            alt: str,
        ) -> dict[str, str]:
            input_data = Input.model_validate(
                {
                    "post_id": post_id,
                    "file_url": file_url,
                    "alt": alt,
                }
            )

            file_name, file_bytes, content_type = UpdatePostImageTool._download_file(
                input_data.file_url
            )
            print(file_name, file_bytes, content_type)

            blog_service = RestPipe.get_blog_service()
            response = blog_service.update_post_image(
                post_id=input_data.post_id,
                file_name=file_name,
                file_bytes=file_bytes,
                alt=input_data.alt,
                content_type=content_type,
            )

            if response.is_failure:
                response.throw_error()

            return {
                "message": "Post image updated",
                "post_id": input_data.post_id,
            }

    @staticmethod
    def _download_file(file_url: str) -> tuple[str, bytes, str]:
        parsed_url = urlparse(file_url)
        if parsed_url.scheme not in {"http", "https"}:
            raise ValueError("file_url must start with http:// or https://")

        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            response = client.get(file_url)
            response.raise_for_status()

        file_bytes = response.content
        content_type = response.headers.get("Content-Type", "application/octet-stream")
        file_name = basename(parsed_url.path) or "upload.bin"

        if not file_bytes:
            raise ValueError("Downloaded file content cannot be empty")

        return file_name, file_bytes, content_type
