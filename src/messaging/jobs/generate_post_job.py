from inngest import Inngest, Context, TriggerCron

from ai import Workflow
from entities import Post
from rest.services import BlogService


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
            workflow = Workflow()
            post = workflow.generate_post(category)
            await ctx.step.run(
                "Generate post",
                lambda: GeneratePostJob._create_post(post),
            )

        return _

    @staticmethod
    async def _get_next_category():
        service = BlogService()
        return service.get_next_category()

    @staticmethod
    async def _generate_post(category: str):
        workflow = Workflow()
        return workflow.generate_post(category)

    @staticmethod
    async def _create_post(post: Post):
        service = BlogService()
        return service.create_post(post)
