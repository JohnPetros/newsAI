import firecrawl  # pyright: ignore[reportMissingTypeStubs]
from firecrawl.types import Document  # pyright: ignore[reportMissingTypeStubs]

from newsai.constants import ENV
from newsai.core.interfaces.website_scraper_provider import WebsiteScraperProvider


class FirecrawlWebsiteScraperProvider(WebsiteScraperProvider):
    def scrape(self, url: str) -> str:
        firecrawl_client = firecrawl.Firecrawl(api_key=ENV.firecrawl_api_key)
        response: Document = firecrawl_client.scrape(url=url, formats=["markdown"])

        markdown = response.markdown
        print(markdown)
        if isinstance(markdown, str):
            return markdown

        raise ValueError("Firecrawl did not return markdown content")
