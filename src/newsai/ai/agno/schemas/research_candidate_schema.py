from pydantic import BaseModel, Field


class ResearchCandidateSchema(BaseModel):
    title: str = Field(min_length=1)
    url: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    why_it_matters: str = Field(min_length=1)
    main_development: str = Field(min_length=1)
    affected_people: list[str] = Field(min_length=1)
