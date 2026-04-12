from typing import TypeVar
from agno.workflow import Workflow
from agno.run.workflow import WorkflowRunOutput
from agno.workflow import Step, StepInput, StepOutput
from pydantic import BaseModel

from newsai.ai.agno.schemas import (
    EditorialBriefSchema,
    FinalPostSchema,
    GeneratePostWorkflowInputSchema,
    NewsPostDraftSchema,
    ResearchCandidatesSchema,
    ScrapedArticleSchema,
    TagListSchema,
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
            description="Generate a blog post through explicit Agno workflow steps.",
            input_schema=GeneratePostWorkflowInputSchema,
            debug_mode=False,
            steps=[
                Step(
                    name="research_story",
                    executor=self._research_story_step,
                    description="Research the most relevant story for the requested category.",
                    max_retries=2,
                    strict_input_validation=True,
                ),
                Step(
                    name="create_editorial_brief",
                    executor=self._create_editorial_brief_step,
                    description="Create the editorial brief for the writer.",
                    max_retries=2,
                    strict_input_validation=True,
                ),
                Step(
                    name="scrape_story",
                    executor=self._scrape_story_step,
                    description="Scrape the selected story content.",
                    max_retries=2,
                    strict_input_validation=True,
                ),
                Step(
                    name="write_post",
                    executor=self._write_post_step,
                    description="Write the structured news post draft.",
                    max_retries=2,
                    strict_input_validation=True,
                ),
                Step(
                    name="review_post",
                    executor=self._review_post_step,
                    description="Review and improve the drafted news post.",
                    max_retries=2,
                    strict_input_validation=True,
                ),
                Step(
                    name="generate_tags",
                    executor=self._generate_tags_step,
                    description="Generate the final SEO tags for the post.",
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
            tags=final_post.tags,
        )

    def _research_story_step(self, step_input: StepInput) -> StepOutput:
        workflow_input = self._coerce_schema(
            step_input.input, GeneratePostWorkflowInputSchema
        )
        prompt = (
            "Pesquise a melhor noticia brasileira recente para a categoria abaixo.\n\n"
            f"Categoria: {workflow_input.category}"
        )

        try:
            response = self.squad.researcher_agent.run(
                prompt,
                output_schema=ResearchCandidatesSchema,
            )
        except Exception as exception:
            raise AppError(
                "AI Error", f"Failed to research the source story: {exception}"
            ) from exception

        research_candidates = self._coerce_schema(
            response.content, ResearchCandidatesSchema
        )
        return StepOutput(content=research_candidates)

    def _scrape_story_step(self, step_input: StepInput) -> StepOutput:
        editorial_brief = self._get_previous_step_schema(
            step_input, "create_editorial_brief", EditorialBriefSchema
        )

        prompt = (
            "Extraia o texto principal da noticia abaixo e retorne o artigo limpo.\n\n"
            f"URL: {editorial_brief.selected_url}\n"
            f"Titulo editorial: {editorial_brief.title}\n"
            f"Angulo: {editorial_brief.angle}\n"
            f"Questao central: {editorial_brief.central_question}"
        )

        try:
            response = self.squad.scrapper_agent.run(
                prompt,
                output_schema=ScrapedArticleSchema,
            )
        except Exception as exception:
            raise AppError(
                "AI Error", f"Failed to scrape the source story: {exception}"
            ) from exception
        scraped_article = self._coerce_schema(response.content, ScrapedArticleSchema)
        return StepOutput(content=scraped_article)

    def _create_editorial_brief_step(self, step_input: StepInput) -> StepOutput:
        workflow_input = self._coerce_schema(
            step_input.input, GeneratePostWorkflowInputSchema
        )
        research_candidates = self._get_previous_step_schema(
            step_input, "research_story", ResearchCandidatesSchema
        )

        prompt = self._join_prompt_sections(
            f"Escolha o melhor candidato e crie um brief editorial para um post sobre a categoria {workflow_input.category}.",
            "Candidatos pesquisados:",
            research_candidates.model_dump_json(indent=2),
        )

        try:
            response = self.squad.editor_agent.run(
                prompt,
                output_schema=EditorialBriefSchema,
            )
        except Exception as exception:
            raise AppError(
                "AI Error", f"Failed to create the editorial brief: {exception}"
            ) from exception

        editorial_brief = self._coerce_schema(response.content, EditorialBriefSchema)
        return StepOutput(content=editorial_brief)

    def _write_post_step(self, step_input: StepInput) -> StepOutput:
        workflow_input = self._coerce_schema(
            step_input.input, GeneratePostWorkflowInputSchema
        )
        research_candidates = self._get_previous_step_schema(
            step_input, "research_story", ResearchCandidatesSchema
        )
        editorial_brief = self._get_previous_step_schema(
            step_input, "create_editorial_brief", EditorialBriefSchema
        )
        scraped_article = self._get_previous_step_schema(
            step_input, "scrape_story", ScrapedArticleSchema
        )

        prompt = self._join_prompt_sections(
            f"Escreva um post jornalistico em PT-BR para a categoria {workflow_input.category}.",
            "Use o brief editorial como contrato principal.",
            "Nao retorne tags. As tags serao geradas em uma etapa separada.",
            "Candidatos pesquisados:",
            research_candidates.model_dump_json(indent=2),
            "Artigo raspado:",
            scraped_article.model_dump_json(indent=2),
            "Brief editorial:",
            editorial_brief.model_dump_json(indent=2),
        )

        try:
            response = self.squad.writer_agent.run(
                prompt,
                output_schema=NewsPostDraftSchema,
            )
        except Exception as exception:
            raise AppError(
                "AI Error", f"Failed to write the blog post: {exception}"
            ) from exception

        draft = self._coerce_schema(response.content, NewsPostDraftSchema)
        return StepOutput(content=draft)

    def _review_post_step(self, step_input: StepInput) -> StepOutput:
        research_candidates = self._get_previous_step_schema(
            step_input, "research_story", ResearchCandidatesSchema
        )
        scraped_article = self._get_previous_step_schema(
            step_input, "scrape_story", ScrapedArticleSchema
        )
        editorial_brief = self._get_previous_step_schema(
            step_input, "create_editorial_brief", EditorialBriefSchema
        )
        draft = self._get_previous_step_schema(
            step_input, "write_post", NewsPostDraftSchema
        )

        prompt = self._join_prompt_sections(
            "Revise e melhore o post abaixo sem inventar informacoes novas.",
            "Candidatos pesquisados:",
            research_candidates.model_dump_json(indent=2),
            "Artigo raspado:",
            scraped_article.model_dump_json(indent=2),
            "Brief editorial:",
            editorial_brief.model_dump_json(indent=2),
            "Rascunho do post:",
            draft.model_dump_json(indent=2),
        )

        try:
            response = self.squad.reviewer_agent.run(
                prompt,
                output_schema=NewsPostDraftSchema,
            )
        except Exception as exception:
            raise AppError(
                "AI Error", f"Failed to review the blog post: {exception}"
            ) from exception

        reviewed_draft = self._coerce_schema(response.content, NewsPostDraftSchema)
        return StepOutput(content=reviewed_draft)

    def _generate_tags_step(self, step_input: StepInput) -> StepOutput:
        draft = self._get_previous_step_schema(
            step_input, "review_post", NewsPostDraftSchema
        )

        prompt = self._join_prompt_sections(
            "Gere as tags finais de SEO para o post abaixo.",
            draft.model_dump_json(indent=2),
        )

        try:
            response = self.squad.tagger_agent.run(
                prompt,
                output_schema=TagListSchema,
            )
        except Exception as exception:
            raise AppError(
                "AI Error", f"Failed to generate final tags: {exception}"
            ) from exception

        tags = self._coerce_schema(response.content, TagListSchema)
        return StepOutput(content=tags)

    def _build_post_step(self, step_input: StepInput) -> StepOutput:
        workflow_input = self._coerce_schema(
            step_input.input, GeneratePostWorkflowInputSchema
        )
        draft = self._get_previous_step_schema(
            step_input, "review_post", NewsPostDraftSchema
        )
        tags = self._get_previous_step_schema(
            step_input, "generate_tags", TagListSchema
        )

        final_post = FinalPostSchema(
            title=draft.title,
            content=draft.content,
            category=workflow_input.category,
            reading_time=draft.reading_time,
            tags=tags.tags,
            original_url=draft.original_url,
        )

        return StepOutput(content=final_post)

    def _join_prompt_sections(self, *sections: str) -> str:
        return "\n\n".join(section.strip() for section in sections if section.strip())

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
