from playwright.sync_api import sync_playwright

from newsai.core.interfaces.website_scraper_provider import WebsiteScraperProvider


class PlaywrightWebsiteScraperProvider(WebsiteScraperProvider):
    def scrape(self, url: str) -> str:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            content = page.content()
            browser.close()
            return content
