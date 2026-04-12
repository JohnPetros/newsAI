from typing import Protocol


class ImageGeneratorProvider(Protocol):
    def generate(self, prompt: str) -> bool: ...
