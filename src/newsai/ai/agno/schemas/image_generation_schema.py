from pydantic import BaseModel, Field


class ImageGenerationSchema(BaseModel):
    image_alt: str = Field(min_length=1)
