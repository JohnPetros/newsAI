from inngest import Inngest, Context, TriggerCron

from newsai.core.dtos.post_dto import PostDto
from newsai.pipes.ai_pipe import AiPipe
from newsai.pipes.rest_pipe import RestPipe


class GeneratePostJob:
    @staticmethod
    def handle(inngest: Inngest):
        @inngest.create_function(
            fn_id="generate.post.job",
            trigger=TriggerCron(cron="0 3 * * *"),
        )
        async def _(ctx: Context) -> None:
            category = await ctx.step.run(
                "Get next category",
                GeneratePostJob._get_next_category,
            )
            workflow = AiPipe.get_generate_post_workflow()
            post = workflow.generate_post(category)
            await ctx.step.run(
                "Generate post",
                lambda: GeneratePostJob._create_post(post),
            )

        return _

    @staticmethod
    async def _get_next_category():
        service = RestPipe.get_blog_service()
        return service.get_next_category().body

    @staticmethod
    async def _generate_post(category: str):
        workflow = AiPipe.get_generate_post_workflow()
        return workflow.generate_post(category)

    @staticmethod
    async def _create_post(post: PostDto):
        service = RestPipe.get_blog_service()
        return service.create_post(post)
