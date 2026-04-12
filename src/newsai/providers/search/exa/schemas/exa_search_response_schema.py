from pydantic import BaseModel, Field

from .exa_result_schema import ExaResultSchema


class ExaSearchResponseSchema(BaseModel):
    results: list[ExaResultSchema] = Field(default_factory=list)
