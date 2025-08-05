from json import loads as load_json
from typing import Any

from agno.team import Team
from agno.models.google import Gemini
from ai.agents import (
    editor_agent,
    scrapper_agent,
    researcher_agent,
    tagger_agent,
    writer_agent,
    image_generator_agent,
)
from entities.post import Post
from errors.app_error import AppError


class GeneratePostWorkflow:
    team: Team

    def __init__(self) -> None:
        self.team = Team(
            name="News Writing Team",
            mode="coordinate",
            model=Gemini(id="gemini-2.5-flash"),
            members=[
                researcher_agent,
                editor_agent,
                scrapper_agent,
                writer_agent,
                tagger_agent,
            ],
            debug_mode=False,
            instructions=[
                "You are a team of experts working together to create a blog post about the most relevant and engaging news story of a given topic in PT-BR.",
                "You will work together to research, edit, and write a blog post about the most relevant and engaging news story of a given topic.",
                "You will use the following agents to work together and in this order:",
                "1. Researcher Agent - to research the most relevant and engaging news story of the day",
                "2. Editor Agent - to edit the news story and make it more engaging and informative",
                "3. Scrapper Agent - to scrape the news story and get the full content",
                "4. Writer Agent - to write the blog post based on the news story",
                "5. Tagger Agent - to create a list of tags for the blog post",
                "After think the reading time the reader will spend reading the post, you should add the reading time in minutes to the JSON resonse.",
                "Give me the final blog post with the title, content, tags and the original url of the news story in JSON format.",
                "The JSON should be in the following format:",
                """
                {
                    "title": "The title of the post.",
                    "content": "The content of the post in HTML format.",
                    "tags": ["The tags of the post."],
                    "reading_time": "The reading time of the post in minutes. (only numbers)",
                    "original_url": "The original url of the news story."
                }
                """,
            ],
            share_member_interactions=False,
            show_members_responses=False,
            add_datetime_to_instructions=True,
            success_criteria="The team has provided a complete blog post in PT-BR about the most relevant and engaging news story of the given topic.",
        )

    def start(self, post_category: str) -> Post:
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
        return dict(
            load_json(
                response.replace("```json", "").replace("```", "").replace("\n", "")
            )
        )

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
