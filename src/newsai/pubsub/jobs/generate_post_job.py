from dataclasses import asdict
from typing import Any
from inngest import Inngest, Context, TriggerCron

from newsai.core.dtos.post_dto import PostDto
from newsai.pipes.ai_pipe import AiPipe
from newsai.pipes.rest_pipe import RestPipe


class GeneratePostJob:
    @staticmethod
    def handle(inngest: Inngest):
        @inngest.create_function(
            fn_id="generate.post.job",
            trigger=TriggerCron(cron="0 */8 * * *"),
        )
        async def _(ctx: Context) -> None:
            category = await ctx.step.run(
                "Get next category",
                GeneratePostJob._get_next_category,
            )
            post_data = await ctx.step.run(
                "Generate post",
                lambda: GeneratePostJob._generate_post(category),
            )
            await ctx.step.run(
                "Create post",
                lambda: GeneratePostJob._create_post(post_data),
            )

        return _

    @staticmethod
    async def _get_next_category() -> str:
        service = RestPipe.get_blog_service()
        return service.get_next_category().body

    @staticmethod
    async def _generate_post(category: str) -> dict[str, Any]:
        workflow = AiPipe.get_generate_post_workflow()
        post = workflow.run(category)
        return asdict(post)

    @staticmethod
    async def _create_post(post_data: dict[str, Any]):
        service = RestPipe.get_blog_service()
        response = service.create_post(PostDto(**post_data))
        if response.is_failure:
            response.throw_error()
