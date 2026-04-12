from typing import TypeVar

from agno.workflow import Workflow
from agno.run.workflow import WorkflowRunOutput
from agno.workflow import Step, StepInput, StepOutput
from pydantic import BaseModel

from newsai.ai.agno.schemas import (
    FinalPostSchema,
    GenerateImageInputSchema,
    GeneratePostWorkflowInputSchema,
    ImageGenerationSchema,
    NewsPostDraftSchema,
)
from newsai.ai.agno.squad import Squad
from newsai.core.dtos.post_dto import PostDto
from newsai.core.errors.app_error import AppError
from newsai.core.interfaces.generate_post_workflow import GeneratePostWorkflow

SchemaT = TypeVar("SchemaT", bound=BaseModel)


class AgnoGeneratePostWorkflow(GeneratePostWorkflow):
    def __init__(self) -> None:
        self.squad = Squad()
        self.workflow = Workflow(
            name="Agno Generate Post Workflow",
            description="Generate a blog post and image metadata through explicit Agno workflow steps.",
            input_schema=GeneratePostWorkflowInputSchema,
            debug_mode=False,
            steps=[
                Step(
                    name="draft_post",
                    executor=self._draft_post_step,
                    description="Generate the structured news post draft.",
                    max_retries=2,
                    strict_input_validation=True,
                ),
                Step(
                    name="generate_image_metadata",
                    executor=self._generate_image_metadata_step,
                    description="Generate the image alt text for the post.",
                    max_retries=2,
                    strict_input_validation=True,
                ),
                Step(
                    name="build_post",
                    executor=self._build_post_step,
                    description="Assemble the final typed blog post output.",
                    max_retries=0,
                    strict_input_validation=True,
                ),
            ],
        )

    def run(self, post_category: str) -> PostDto:
        workflow_input = GeneratePostWorkflowInputSchema(category=post_category)

        try:
            workflow_response = self.workflow.run(workflow_input)
        except Exception as exception:
            raise AppError("AI Error", str(exception)) from exception

        final_post = self._extract_workflow_content(workflow_response, FinalPostSchema)

        return PostDto(
            title=final_post.title,
            content=final_post.content,
            category=final_post.category,
            reading_time=final_post.reading_time,
            image_alt=final_post.image_alt,
            tags=final_post.tags,
        )

    def _draft_post_step(self, step_input: StepInput) -> StepOutput:
        workflow_input = self._coerce_schema(
            step_input.input, GeneratePostWorkflowInputSchema
        )
        prompt = f"Crie um post de blog sobre o assunto de {workflow_input.category}"

        try:
            response = self.squad.news_writing_team.run(
                prompt,
                output_schema=NewsPostDraftSchema,
            )
        except Exception as exception:
            raise AppError(
                "AI Error", f"Failed to generate the news post draft: {exception}"
            ) from exception

        draft = self._coerce_schema(response.content, NewsPostDraftSchema)
        return StepOutput(content=draft)

    def _generate_image_metadata_step(self, step_input: StepInput) -> StepOutput:
        workflow_input = self._coerce_schema(
            step_input.input, GeneratePostWorkflowInputSchema
        )
        draft = self._get_previous_step_schema(
            step_input, "draft_post", NewsPostDraftSchema
        )

        image_input = GenerateImageInputSchema(
            title=draft.title,
            content=draft.content,
            tags=draft.tags,
            reading_time=draft.reading_time,
            original_url=draft.original_url,
            category=workflow_input.category,
        )

        try:
            response = self.squad.image_generator_agent.run(
                image_input.model_dump_json(indent=2),
                output_schema=ImageGenerationSchema,
            )
        except Exception as exception:
            raise AppError(
                "AI Error", f"Failed to generate image metadata: {exception}"
            ) from exception

        image_data = self._coerce_schema(response.content, ImageGenerationSchema)
        return StepOutput(content=image_data)

    def _build_post_step(self, step_input: StepInput) -> StepOutput:
        workflow_input = self._coerce_schema(
            step_input.input, GeneratePostWorkflowInputSchema
        )
        draft = self._get_previous_step_schema(
            step_input, "draft_post", NewsPostDraftSchema
        )
        image_data = self._get_previous_step_schema(
            step_input,
            "generate_image_metadata",
            ImageGenerationSchema,
        )

        final_post = FinalPostSchema(
            title=draft.title,
            content=draft.content,
            category=workflow_input.category,
            reading_time=draft.reading_time,
            image_alt=image_data.image_alt,
            tags=draft.tags,
        )

        return StepOutput(content=final_post)

    def _get_previous_step_schema(
        self,
        step_input: StepInput,
        step_name: str,
        schema: type[SchemaT],
    ) -> SchemaT:
        previous_step_outputs = step_input.previous_step_outputs or {}
        previous_step = previous_step_outputs.get(step_name)
        if previous_step is None:
            raise AppError(
                "AI Error", f"Missing workflow output from step '{step_name}'"
            )

        return self._coerce_schema(previous_step.content, schema)

    def _extract_workflow_content(
        self,
        workflow_response: WorkflowRunOutput,
        schema: type[SchemaT],
    ) -> SchemaT:
        return self._coerce_schema(workflow_response.content, schema)

    def _coerce_schema(self, value: object, schema: type[SchemaT]) -> SchemaT:
        try:
            if isinstance(value, schema):
                return value
            return schema.model_validate(value)
        except Exception as exception:
            raise AppError(
                "AI Error",
                f"Invalid structured output for {schema.__name__}: {exception}",
            ) from exception
