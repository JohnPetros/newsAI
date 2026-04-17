from pydantic import BaseModel, ConfigDict, Field

from fastmcp import FastMCP

from newsai.pipes.rest_pipe import RestPipe


class Input(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    post_id: str = Field(min_length=1)
    content: str = Field(min_length=1)


class UpdatePostContentTool:
    @staticmethod
    def handle(mcp: FastMCP) -> None:
        @mcp.tool(
            name="update_post_content",
            description="Updates the content of an existing blog post by its id.",
        )
        def _(post_id: str, content: str) -> dict[str, str]:
            input_data = Input.model_validate({"post_id": post_id, "content": content})

            blog_service = RestPipe.get_blog_service()
            response = blog_service.update_post_content(
                post_id=input_data.post_id,
                content=input_data.content,
            )

            if response.is_failure:
                response.throw_error()

            return {"message": "Post content updated", "post_id": input_data.post_id}
