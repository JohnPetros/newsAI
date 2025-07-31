from dataclasses import dataclass


@dataclass
class Post:
    title: str
    content: str
    category: str
    reading_time: int
    image_alt: str
    tags: list[str]
