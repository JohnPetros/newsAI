from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ai import Workflow
from core.entities import Post
from rest.middleware import Middleware
from rest.services import BlogService


class Body(BaseModel):
    category: str


class GeneratePostController:
    @staticmethod
    def handle(router: APIRouter) -> None:
        @router.post("/post", dependencies=[Depends(Middleware.verify_api_key)])
        def _(body: Body) -> Post:
            workflow = Workflow()
            post = workflow.generate_post(body.category)

            service = BlogService()
            service.create_post(post)

            return post
