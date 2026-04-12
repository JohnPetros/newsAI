from pydantic import Field

from .news_post_draft_schema import NewsPostDraftSchema


class GenerateImageInputSchema(NewsPostDraftSchema):
    tags: list[str] = Field(min_length=1)
    category: str = Field(min_length=1)
