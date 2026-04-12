from enum import StrEnum

from pydantic import BaseModel, Field


class EditorialTone(StrEnum):
    SERIOUS = "serious"
    ANALYTIC = "analytic"
    ENTHUSIASTIC = "enthusiastic"


class EditorialBriefSchema(BaseModel):
    selected_url: str = Field(min_length=1)
    title: str = Field(min_length=1)
    angle: str = Field(min_length=1)
    tone: EditorialTone
    audience: str = Field(min_length=1)
    central_question: str = Field(min_length=1)
    key_facts: list[str] = Field(min_length=3)
    structure: list[str] = Field(min_length=3)
    avoid_points: list[str] = Field(default_factory=list)
