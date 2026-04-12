from newsai.core.decorators.dto import dto


@dto
class PostDto:
    title: str
    content: str
    category: str
    reading_time: int
    image_alt: str
    tags: list[str]
