from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field

from newsai.core.interfaces.blog_service import BlogService
from newsai.pipes.rest_pipe import RestPipe


class Body(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, populate_by_name=True)

    title: str = Field(min_length=1)
    is_reviewed: bool = Field(alias="isReviewed")


class UpdatePostTitleAndReviewController:
    @staticmethod
    def handle(router: APIRouter) -> None:
        @router.patch(
            "/post/{post_id}",
            dependencies=[Depends(RestPipe.verify_api_key)],
        )
        def _(
            post_id: str,
            body: Body,
            blog_service: Annotated[BlogService, Depends(RestPipe.get_blog_service)],
        ) -> dict[str, str]:
            response = blog_service.update_post_title_and_review_status(
                post_id=post_id,
                title=body.title,
                is_reviewed=body.is_reviewed,
            )

            if response.is_failure:
                response.throw_error()

            return {"message": "Post updated", "post_id": post_id}
