from datetime import UTC, datetime, timedelta
from json import dumps

from newsai.core.interfaces.rest_client import RestClient
from newsai.core.interfaces.web_searcher_provider import WebSearcherProvider
from newsai.providers.search.exa.schemas import ExaResultSchema, ExaSearchResponseSchema


class ExaWebSearcherProvider(WebSearcherProvider):
    def __init__(self, rest_client: RestClient) -> None:
        self._rest_client = rest_client

    def search(self, query: str) -> str:
        start_published_date = (datetime.now(UTC) - timedelta(days=1)).strftime(
            "%Y-%m-%d"
        )

        response = self._rest_client.post(
            "/search",
            dict,
            body={
                "query": query,
                "type": "auto",
                "category": "news",
                "numResults": 10,
                "startPublishedDate": start_published_date,
                "contents": {
                    "text": {"maxCharacters": 2000},
                    "highlights": {"maxCharacters": 2000},
                },
            },
            timeout=30,
        )

        payload = ExaSearchResponseSchema.model_validate(response.body)

        normalized_results: list[dict[str, object]] = []
        for result in payload.results:
            if not self._is_viable_news_result(result):
                continue

            title = self._clean_text(result.title, fallback="Untitled result")
            url = self._clean_text(result.url, fallback="https://example.com")
            summary = self._build_summary(result)
            author = self._clean_text(result.author, fallback="the reported source")
            published_date = self._clean_text(result.publishedDate, fallback="recently")
            normalized_results.append(
                {
                    "title": title,
                    "url": url,
                    "summary": summary,
                    "why_it_matters": (
                        f"This story is relevant now because it reflects a recent development published {published_date}."
                    ),
                    "main_development": summary,
                    "affected_people": [author],
                }
            )

            if len(normalized_results) == 5:
                break

        if len(normalized_results) < 5:
            raise ValueError("Exa did not return enough viable news candidates")

        return dumps({"candidates": normalized_results}, ensure_ascii=True)

    def _is_viable_news_result(self, result: ExaResultSchema) -> bool:
        title = self._clean_text(result.title)
        url = self._clean_text(result.url)
        published_date = self._clean_text(result.publishedDate)

        if not title or not url or not published_date:
            return False

        lowered_title = title.lower()
        return "archive" not in lowered_title and "latest news" not in lowered_title

    def _build_summary(self, result: ExaResultSchema) -> str:
        highlights = result.highlights or []
        for highlight in highlights:
            cleaned_highlight = self._clean_highlight(highlight)
            if cleaned_highlight:
                return cleaned_highlight

        text = self._clean_highlight(result.text)
        if text:
            return text

        return "Recent news result returned by Exa without a usable summary."

    def _clean_highlight(self, value: str | None) -> str:
        cleaned_value = self._clean_text(value)
        if not cleaned_value:
            return ""

        shortened_value = cleaned_value.split("###")[0].split("##")[0].strip()
        if len(shortened_value) > 400:
            return f"{shortened_value[:397].rstrip()}..."
        return shortened_value

    def _clean_text(self, value: str | None, fallback: str = "") -> str:
        if value is None:
            return fallback
        cleaned_value = " ".join(value.split()).strip()
        return cleaned_value or fallback
