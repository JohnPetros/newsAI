from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from newsai.core.interfaces.blog_service import BlogService
from newsai.pipes.ai_pipe import AiPipe
from newsai.core.dtos.post_dto import PostDto
from newsai.core.interfaces.generate_post_workflow import GeneratePostWorkflow
from newsai.pipes.rest_pipe import RestPipe
from newsai.rest.middleware import Middleware


class Body(BaseModel):
    category: str


class GeneratePostController:
    @staticmethod
    def handle(router: APIRouter) -> None:
        @router.post(
            "/post",
            dependencies=[Depends(Middleware.verify_api_key)],
            response_model=PostDto,
        )
        def _(
            body: Body,
            generate_post_workflow: Annotated[
                GeneratePostWorkflow, Depends(AiPipe.get_generate_post_workflow)
            ],
            blog_service: Annotated[BlogService, Depends(RestPipe.get_blog_service)],
        ) -> PostDto:
            post = generate_post_workflow.run(body.category)

            blog_service.create_post(post)

            return post
