from pydantic import BaseModel, Field

from .research_candidate_schema import ResearchCandidateSchema


class ResearchCandidatesSchema(BaseModel):
    candidates: list[ResearchCandidateSchema] = Field(min_length=5, max_length=5)
