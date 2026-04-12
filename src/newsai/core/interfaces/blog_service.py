from typing import Protocol

from newsai.core.dtos.post_dto import PostDto
from newsai.core.responses.rest_response import RestResponse


class BlogService(Protocol):
    def create_post(self, post: PostDto) -> RestResponse[None]: ...

    def get_next_category(self) -> RestResponse[str]: ...
