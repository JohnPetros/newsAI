from pathlib import Path
import requests as rest_client

from entities import Post

from constants import ENV


class BlogService:
    def create_post(self, post: Post) -> None:
        image = Path("image.png")

        with image.open("rb") as file:
            form_data = [
                ("title", post.title),
                ("content", post.content),
                ("category", post.category),
                ("readingTime", post.reading_time),
                ("imageAlt", post.image_alt),
            ]
            for tag in post.tags:
                form_data.append(("tags[]", tag))

            response = rest_client.post(
                f"{ENV.blog_api_url}/posts",
                data=form_data,
                files={"image": (image.name, file, "image/png")},
                timeout=30,
            )
            print(response.json())
