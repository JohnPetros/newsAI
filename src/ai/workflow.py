from json import loads as load_json
from typing import Any

from agno.team import Team
from agno.models.google import Gemini
from tenacity import retry, stop_after_attempt, wait_exponential
from ai.agents import (
    editor_agent,
    scrapper_agent,
    researcher_agent,
    tagger_agent,
    writer_agent,
    image_generator_agent,
)
from core.entities import Post
from errors.app_error import AppError


class Workflow:
    team: Team

    def __init__(self) -> None:
        self.team = Team(
            name="News Writing Team",
            model=Gemini(id="gemini-3-pro-preview"),
            members=[
                researcher_agent,
                editor_agent,
                scrapper_agent,
                writer_agent,
                tagger_agent,
            ],
            debug_mode=False,
            instructions=[
                "You are an elite journalistic team creating a high-quality blog post in PT-BR.",
                "CRITICAL RULE: You must be strictly faithful to the current date provided in the context. If today is Feb 3rd, DO NOT write about events in May or August as if they have already happened. Treat future events as future.",
                "CRITICAL RULE: Do not halluncinate information. All names, dates, and facts must come from the researched and scraped content.",
                "You will execute the pipeline in this strict order:",
                "1. Researcher Agent: Search for the most relevant/trending news story of the LAST 24 HOURS on the given topic. Return the specific URL.",
                "   - Filter out 'evergreen' content or generic articles. Look for breaking news.",
                "2. Scrapper Agent: Scrape the FULL content from the URL provided by the Researcher. Extract the raw text.",
                "3. Editor Agent: Analyze the scraped text and define the 'Angle' of the story.",
                "   - Identify the 3 most important facts.",
                "   - Decide on a journalistic tone (Serious, Analytic, or Enthusiastic).",
                "   - Create a structure for the Writer.",
                "4. Writer Agent: Write the blog post in PT-BR based ONLY on the Editor's plan and Scrapper's data.",
                "   - STYLE GUIDE: Write like a senior journalist from 'Folha de S.Paulo' or 'The New York Times'.",
                "   - Avoid AI clichés like 'No cenário atual', 'Tapeçaria cultural', 'Mergulhamos', 'Em suma'.",
                "   - Use specific entities (Names of people, places, values, dates).",
                "   - Paragraphs should be short and punchy.",
                "   - If the news is about the future, use 'Will', 'Expected to', 'Scheduled for'. Never use past tense for future events.",
                "5. Tagger Agent: Generate 5 relevant SEO tags in PT-BR.",
                "Calculate the reading time based on the final word count (avg 200 words/min).",
                "Return the final output strictly in the requested JSON format.",
                """
                {
                    "title": "A catchy, SEO-friendly title in PT-BR.",
                    "content": "The full blog post in HTML format (use <h2>, <p>, <ul>).",
                    "tags": ["tag1", "tag2", "tag3"],
                    "reading_time": "integer_minutes",
                    "original_url": "The source URL found by the researcher"
                }
                """,
                "Before the json response, strictly say 'Here is the final blog post in JSON format:'",
            ],
            share_member_interactions=False,
            show_members_responses=False,
            add_datetime_to_context=True,
        )

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=15)
    )
    def generate_post(self, post_category: str) -> Post:
        post = None
        team_response = self._run_team(post_category)
        print("team_response", team_response)

        post = self._convert_to_post(team_response, post_category)

        image_agent_response = self._run_image_agent(post.content)
        print("image_agent_response", image_agent_response)
        image_data = self._load_json(image_agent_response)
        post.image_alt = image_data["image_alt"]

        return post

    def _run_team(self, post_category: str) -> str:
        team_response = None
        try:
            team_response = self.team.run(
                f"Crie um post de blog sobre o assunto de {post_category}",
                show_full_reasoning=False,
                stream=True,
            )
        except Exception as exception:
            raise AppError("AI Error", str(exception)) from exception

        final_response = ""
        can_include_content = False
        for chunk in team_response:
            print("chunk", str(chunk.content))
            if "```json" in str(chunk.content):
                can_include_content = True
            if can_include_content:
                final_response += str(chunk.content)

        print("final_response", final_response)

        if not final_response:
            raise AppError("AI Error", "No response from the news writing team")

        return final_response

    def _run_image_agent(self, team_response: str) -> str:
        agent_response = None
        try:
            agent_response = image_generator_agent.run(team_response, stream=True)
        except Exception as exception:
            raise AppError("AI Error", str(exception)) from exception

        print("agent_response", agent_response)

        final_response = ""
        can_include_content = False
        for chunk in agent_response:
            if "```json" in str(chunk.content):
                can_include_content = True
            if can_include_content:
                final_response += str(chunk.content)

        if not final_response:
            raise AppError("AI Error", "No response from the image agent")

        return final_response

    def _load_json(self, response: str) -> dict[str, Any]:
        start = response.find("{")
        end = response.rfind("}") + 1
        json_text = response[start:end]
        return dict(load_json(json_text))

    def _convert_to_post(self, response: str, post_category: str) -> Post:
        data = self._load_json(response)

        return Post(
            title=data["title"],
            content=data["content"],
            category=post_category,
            reading_time=int(data["reading_time"]),
            image_alt="",
            tags=data["tags"],
        )
