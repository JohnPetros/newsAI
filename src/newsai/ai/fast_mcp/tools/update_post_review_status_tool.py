from fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field

from newsai.pipes.rest_pipe import RestPipe


class Input(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    post_id: str = Field(min_length=1)
    is_reviewed: bool


class UpdatePostReviewStatusTool:
    @staticmethod
    def handle(mcp: FastMCP) -> None:
        @mcp.tool(
            name="update_post_review_status",
            description="Updates the isReviewed status of an existing post by id.",
        )
        def _(post_id: str, *, is_reviewed: bool) -> dict[str, str]:
            input_data = Input.model_validate(
                {
                    "post_id": post_id,
                    "is_reviewed": is_reviewed,
                }
            )

            blog_service = RestPipe.get_blog_service()
            response = blog_service.update_post_review_status(
                post_id=input_data.post_id,
                is_reviewed=input_data.is_reviewed,
            )

            if response.is_failure:
                response.throw_error()

            return {
                "message": "Post review status updated",
                "post_id": input_data.post_id,
            }
