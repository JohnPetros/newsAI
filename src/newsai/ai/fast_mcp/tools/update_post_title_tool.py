from fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field

from newsai.pipes.rest_pipe import RestPipe


class Input(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    post_id: str = Field(min_length=1)
    title: str = Field(min_length=1)


class UpdatePostTitleTool:
    @staticmethod
    def handle(mcp: FastMCP) -> None:
        @mcp.tool(
            name="update_post_title",
            description="Updates the title of an existing post by id.",
        )
        def _(post_id: str, title: str) -> dict[str, str]:
            input_data = Input.model_validate({"post_id": post_id, "title": title})

            blog_service = RestPipe.get_blog_service()
            response = blog_service.update_post_title(
                post_id=input_data.post_id,
                title=input_data.title,
            )

            if response.is_failure:
                response.throw_error()

            return {"message": "Post title updated", "post_id": input_data.post_id}
