from fastapi import APIRouter
from pydantic import BaseModel

from ai import CreatePostWorkflow
from entities import Post


class Body(BaseModel):
    category: str


class CreatePostController:
    def __init__(self, router: APIRouter) -> None:
        @router.post("/post")
        async def _(body: Body) -> Post:
            workflow = CreatePostWorkflow()
            post = workflow.start(body.category)

            # service = BlogService()
            # service.create_post(post)

            return post
