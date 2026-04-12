from pydantic import BaseModel, Field


class ScrapedArticleSchema(BaseModel):
    url: str = Field(min_length=1)
    headline: str = Field(min_length=1)
    source_name: str = Field(min_length=1)
    published_at: str = Field(min_length=1)
    content: str = Field(min_length=1)
    key_quotes: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
