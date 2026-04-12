from pydantic import BaseModel, Field


class FinalPostSchema(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    category: str = Field(min_length=1)
    reading_time: int = Field(ge=1)
    tags: list[str] = Field(min_length=1)
    original_url: str = Field(min_length=1)
