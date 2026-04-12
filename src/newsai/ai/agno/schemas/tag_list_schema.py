from pydantic import BaseModel, Field


class TagListSchema(BaseModel):
    tags: list[str] = Field(min_length=5)
