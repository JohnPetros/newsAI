from newsai.core.dtos.post_dto import PostDto

from newsai.core.interfaces.blog_service import BlogService
from newsai.core.interfaces.rest_client import RestClient
from newsai.core.responses.rest_response import RestResponse


class PuloDoGatoNewsBlogService(BlogService):
    def __init__(self, rest_client: RestClient) -> None:
        self._rest_client = rest_client

    def create_post(self, post: PostDto) -> RestResponse[None]:
        body = {
            "title": post.title,
            "content": post.content,
            "category": post.category,
            "readingTime": post.reading_time,
            "tags": post.tags,
        }

        return self._rest_client.post(
            "/posts/create",
            type(None),
            body=body,
            timeout=30,
        )

    def get_next_category(self) -> RestResponse[str]:
        response = self._rest_client.get("/posts/next", dict, timeout=30)
        return response.map_body(self._map_category)

    def update_post_content(self, post_id: str, content: str) -> RestResponse[None]:
        return self._rest_client.patch(
            f"/posts/{post_id}/content",
            type(None),
            body={"content": content},
            timeout=30,
        )

    def update_post_title(self, post_id: str, title: str) -> RestResponse[None]:
        return self._rest_client.patch(
            f"/posts/{post_id}/title",
            type(None),
            body={"title": title},
            timeout=30,
        )

    def update_post_slug(self, post_id: str, slug: str) -> RestResponse[None]:
        return self._rest_client.patch(
            f"/posts/{post_id}/slug",
            type(None),
            body={"slug": slug},
            timeout=30,
        )

    def update_post_review_status(
        self,
        post_id: str,
        *,
        is_reviewed: bool,
    ) -> RestResponse[None]:
        return self._rest_client.patch(
            f"/posts/{post_id}/review-status",
            type(None),
            body={"isReviewed": is_reviewed},
            timeout=30,
        )

    def update_post_image(
        self,
        post_id: str,
        *,
        file_name: str,
        file_bytes: bytes,
        alt: str,
        content_type: str,
    ) -> RestResponse[None]:
        return self._rest_client.patch(
            f"/posts/{post_id}/image",
            type(None),
            data={"alt": alt},
            files={"file": (file_name, file_bytes, content_type)},
            timeout=30,
        )

    def _map_category(self, body: dict[object, object]) -> str:
        category = body.get("category")
        if not isinstance(category, str):
            raise TypeError("Expected 'category' to be a string")
        return category
