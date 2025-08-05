from fastapi import APIRouter
from pydantic import BaseModel

from ai import GeneratePostWorkflow
from entities import Post
from rest.services import BlogService


class Body(BaseModel):
    category: str


class GeneratePostController:
    def __init__(self, router: APIRouter) -> None:
        @router.post("/post")
        def _(body: Body) -> Post:
            workflow = GeneratePostWorkflow()
            post = workflow.start(body.category)

            service = BlogService()
            service.create_post(post)

            return post
