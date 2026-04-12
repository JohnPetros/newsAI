from newsai.providers.image_generator.gemini.gemini_image_generator_provider import (
    GeminiImageGeneratorProvider,
)
from newsai.providers.website_scraper.playright.playwright_website_scraper_provider import (
    PlaywrightWebsiteScraperProvider,
)


class Toolset:
    @staticmethod
    def generate_image_tool(prompt: str) -> bool:
        """
        Generate an image for a blog post according to the provided content.

        Args:
            prompt(str): The prompt to generate the image.

        Returns:
            bool: True if the image was generated successfully, False otherwise.
        """

        image_generator_provider = GeminiImageGeneratorProvider()
        return image_generator_provider.generate(prompt)

    @staticmethod
    def scrape_website_tool(url: str) -> str:
        """
        Scrape the website content from the provided URL.

        Args:
            url(str): The target URL.

        Returns:
            str: The scraped HTML content.
        """

        scraper_provider = PlaywrightWebsiteScraperProvider()
        return scraper_provider.scrape(url)
