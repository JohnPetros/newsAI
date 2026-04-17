from typing import Protocol

from newsai.core.dtos.reviewed_post_dto import ReviewedPostDto


class NotificationProvider(Protocol):
    def send_posts_reviewed_notification(
        self, posts: list[ReviewedPostDto]
    ) -> None: ...
