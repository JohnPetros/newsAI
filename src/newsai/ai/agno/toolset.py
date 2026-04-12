from newsai.pipes.providers_pipe import ProvidersPipe


class Toolset:
    @staticmethod
    def search_news_tool(query: str) -> str:
        """
        Search for recent news stories matching the query.

        Args:
            query(str): The search query.

        Returns:
            str: A JSON string containing the top search results.
        """

        search_provider = ProvidersPipe.get_web_searcher_provider()
        return search_provider.search(query)

    @staticmethod
    def generate_image_tool(prompt: str) -> bool:
        """
        Generate an image for a blog post according to the provided content.

        Args:
            prompt(str): The prompt to generate the image.

        Returns:
            bool: True if the image was generated successfully, False otherwise.
        """

        image_generator_provider = ProvidersPipe.get_image_generator_provider()
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

        scraper_provider = ProvidersPipe.get_website_scraper_provider()
        return scraper_provider.scrape(url)
