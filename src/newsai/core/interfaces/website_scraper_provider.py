from typing import Protocol


class WebsiteScraperProvider(Protocol):
    def scrape(self, url: str) -> str: ...
