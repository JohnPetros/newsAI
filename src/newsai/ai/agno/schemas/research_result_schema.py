from pydantic import BaseModel, Field


class ResearchResultSchema(BaseModel):
    title: str = Field(min_length=1)
    url: str = Field(min_length=1)
    summary: str = Field(min_length=1)
