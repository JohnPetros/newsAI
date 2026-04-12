from pydantic import BaseModel, Field


class ScrapedArticleSchema(BaseModel):
    url: str = Field(min_length=1)
    content: str = Field(min_length=1)
