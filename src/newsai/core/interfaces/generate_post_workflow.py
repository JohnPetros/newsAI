from typing import Protocol


from newsai.core.dtos.post_dto import PostDto


class GeneratePostWorkflow(Protocol):
    def run(self, post_category: str) -> PostDto: ...
