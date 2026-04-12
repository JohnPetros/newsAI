from typing import Protocol


class WebSearcherProvider(Protocol):
    def search(self, query: str) -> str: ...
