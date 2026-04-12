from pydantic import BaseModel, Field


class EditorialBriefSchema(BaseModel):
    selected_url: str = Field(min_length=1)
    title: str = Field(min_length=1)
    angle: str = Field(min_length=1)
    tone: str = Field(min_length=1)
    key_facts: list[str] = Field(min_length=3)
    structure: list[str] = Field(min_length=3)
