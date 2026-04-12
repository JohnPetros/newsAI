from pydantic import BaseModel, Field


class NewsPostDraftSchema(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    reading_time: int = Field(ge=1)
    original_url: str = Field(min_length=1)
