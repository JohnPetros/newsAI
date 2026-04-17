from newsai.core.dtos.reviewed_post_dto import ReviewedPostDto
from newsai.core.interfaces.notification_provider import NotificationProvider
from newsai.core.interfaces.rest_client import RestClient


class DiscordNotificationService(NotificationProvider):
    def __init__(self, rest_client: RestClient) -> None:
        self._rest_client = rest_client

    def send_posts_reviewed_notification(self, posts: list[ReviewedPostDto]) -> None:
        if not posts:
            return

        content = self._build_content(posts)
        response = self._rest_client.post(
            self._rest_client.get_base_url(),
            dict,
            body={"content": content},
            timeout=30,
        )

        if response.is_failure:
            response.throw_error()

    def _build_content(self, posts: list[ReviewedPostDto]) -> str:
        title = "Posts revisados e prontos para publicacao:"
        lines: list[str] = [title]

        for post in posts:
            post_title = " ".join(post.title.split()).strip()
            line = f"- [{post.id}] {post_title}"
            lines.append(line)

        content = "\n".join(lines)
        if len(content) <= 2000:
            return content

        return f"{content[:1997].rstrip()}..."
