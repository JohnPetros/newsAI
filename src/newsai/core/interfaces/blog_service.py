from typing import Protocol

from newsai.core.dtos.post_dto import PostDto
from newsai.core.responses.rest_response import RestResponse


class BlogService(Protocol):
    def create_post(self, post: PostDto) -> RestResponse[None]: ...

    def get_next_category(self) -> RestResponse[str]: ...

    def update_post_content(self, post_id: str, content: str) -> RestResponse[None]: ...

    def update_post_title(self, post_id: str, title: str) -> RestResponse[None]: ...

    def update_post_slug(self, post_id: str, slug: str) -> RestResponse[None]: ...

    def update_post_review_status(
        self,
        post_id: str,
        *,
        is_reviewed: bool,
    ) -> RestResponse[None]: ...

    def update_post_image(
        self,
        post_id: str,
        *,
        file_name: str,
        file_bytes: bytes,
        alt: str,
        content_type: str,
    ) -> RestResponse[None]: ...
