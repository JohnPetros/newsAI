from newsai.constants import ENV
from newsai.core.interfaces.image_generator_provider import ImageGeneratorProvider
from newsai.core.interfaces.notification_provider import NotificationProvider
from newsai.core.interfaces.web_searcher_provider import WebSearcherProvider
from newsai.core.interfaces.website_scraper_provider import WebsiteScraperProvider
from newsai.providers.image_generator.noop.noop_image_generator_provider import (
    NoopImageGeneratorProvider,
)
from newsai.providers.notification.discord.discord_notification_provider import (
    DiscordNotificationService,
)
from newsai.providers.search.exa.exa_web_searcher_provider import ExaWebSearcherProvider
from newsai.providers.website_scraper.firecrawl.firecrawl_website_scraper_provider import (
    FirecrawlWebsiteScraperProvider,
)
from newsai.rest.httpx.httpx_rest_client import HttpxRestClient


class ProvidersPipe:
    @staticmethod
    def get_web_searcher_provider() -> WebSearcherProvider:
        return ExaWebSearcherProvider(
            HttpxRestClient(
                base_url="https://api.exa.ai",
                headers={
                    "x-api-key": ENV.exa_api_key,
                    "Content-Type": "application/json",
                },
            )
        )

    @staticmethod
    def get_website_scraper_provider() -> WebsiteScraperProvider:
        return FirecrawlWebsiteScraperProvider()

    @staticmethod
    def get_image_generator_provider() -> ImageGeneratorProvider:
        return NoopImageGeneratorProvider()

    @staticmethod
    def get_notification_provider() -> NotificationProvider:
        if not ENV.discord_webhook_url:
            raise ValueError("DISCORD_WEBHOOK_URL is required")

        return DiscordNotificationService(
            rest_client=HttpxRestClient(
                base_url=ENV.discord_webhook_url,
                headers={"Content-Type": "application/json"},
            ),
        )
