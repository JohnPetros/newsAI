from pydantic import BaseModel


class ExaResultSchema(BaseModel):
    title: str | None = None
    url: str | None = None
    publishedDate: str | None = None
    author: str | None = None
    highlights: list[str] | None = None
    text: str | None = None
