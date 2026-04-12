from pathlib import Path

from newsai.core.dtos.post_dto import PostDto

from newsai.core.interfaces.blog_service import BlogService
from newsai.core.interfaces.rest_client import RestClient
from newsai.core.responses.rest_response import RestResponse


class PuloDoGatoNewsBlogService(BlogService):
    def __init__(self, rest_client: RestClient) -> None:
        self.rest_client = rest_client

    def create_post(self, post: PostDto) -> RestResponse[None]:
        image = Path("image.png")

        with image.open("rb") as file:
            form_data = {
                "title": post.title,
                "content": post.content,
                "category": post.category,
                "readingTime": post.reading_time,
                "imageAlt": post.image_alt,
                "tags[]": post.tags,
            }

            response = self.rest_client.post(
                "/posts/create",
                type(None),
                data=form_data,
                files={"image": (image.name, file, "image/png")},
                timeout=30,
            )

            image.unlink()
            return response

    def get_next_category(self) -> RestResponse[str]:
        response = self.rest_client.get("/posts/next", dict, timeout=30)
        return response.map_body(self._map_category)

    def _map_category(self, body: dict[object, object]) -> str:
        category = body.get("category")
        if not isinstance(category, str):
            raise TypeError("Expected 'category' to be a string")
        return category
