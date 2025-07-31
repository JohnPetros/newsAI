from json import loads as load_json

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


class CreatePostWorkflow:
    team: Team

    def __init__(self) -> None:
        self.team = Team(
            name="News Writing Team",
            mode="coordinate",
            model=Gemini(id="gemini-2.0-flash"),
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
                "After the post is written, you should save the post title and original url in the sqlite storage.",
                "Give me the final blog post with the title, content, tags and the original url of the news story in JSON format.",
                "The JSON should be in the following format:",
                """
                {
                    "title": "The title of the post.",
                    "content": "The content of the post in HTML format.",
                    "tags": ["The tags of the post."],
                    "original_url": "The original url of the news story."
                }
                """,
            ],
            share_member_interactions=False,
            show_members_responses=False,
            add_datetime_to_instructions=True,
            success_criteria="The team has provided a complete blog post in PT-BR about the most relevant and engaging news story of the given topic.",
        )

    def start(self, topic: str) -> Post:
        team_response = self._run_team(topic)
        final_response = self._run_image_agent(team_response)
        return self._convert_to_post(final_response)

    def _run_team(self, topic: str) -> str:
        team_response = self.team.run(
            f"Create a blog post about the {topic} topic",
            show_full_reasoning=False,
            stream=True,
        )
        final_response = ""
        can_include_content = False
        for chunk in team_response:
            if "```json" in str(chunk.content):
                can_include_content = True
            if can_include_content:
                final_response += str(chunk.content)

        return final_response

    def _run_image_agent(self, team_response: str) -> str:
        agent_response = image_generator_agent.run(team_response, stream=True)
        final_response = ""
        for chunk in agent_response:
            final_response += str(chunk.content)

        return final_response

    def _convert_to_post(self, response: str) -> Post:
        data = dict(
            load_json(
                response.replace("```json", "").replace("```", "").replace("\n", "")
            )
        )

        return Post(
            title=data["title"],
            content=data["content"],
            category=data["category"],
            reading_time=data["reading_time"],
            image_alt=data["image_alt"],
            tags=data["tags"],
        )
