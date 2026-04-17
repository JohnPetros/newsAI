from newsai.core.decorators.dto import dto


@dto
class ReviewedPostDto:
    id: str
    title: str
