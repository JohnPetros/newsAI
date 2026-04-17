from fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field

from newsai.pipes.rest_pipe import RestPipe


class Input(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    post_id: str = Field(min_length=1)
    slug: str = Field(min_length=1)


class UpdatePostSlugTool:
    @staticmethod
    def handle(mcp: FastMCP) -> None:
        @mcp.tool(
            name="update_post_slug",
            description="Updates the slug of an existing post by id.",
        )
        def _(post_id: str, slug: str) -> dict[str, str]:
            input_data = Input.model_validate({"post_id": post_id, "slug": slug})

            blog_service = RestPipe.get_blog_service()
            response = blog_service.update_post_slug(
                post_id=input_data.post_id,
                slug=input_data.slug,
            )

            if response.is_failure:
                response.throw_error()

            return {"message": "Post slug updated", "post_id": input_data.post_id}
