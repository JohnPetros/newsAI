from pydantic import BaseModel, Field


class GeneratePostWorkflowInputSchema(BaseModel):
    category: str = Field(min_length=1)
