from datetime import datetime

from agno.team import Team
from agno.models.google import Gemini
from pydantic import BaseModel, Field

from ai.agents import (
    editor_agent,
    scrapper_agent,
    researcher_agent,
    tagger_agent,
    writer_agent,
)


class PostModel(BaseModel):
    title: str = Field(..., description="The title of the post.")
    content: str = Field(..., description="The content of the post.")
    tags: list[str] = Field(..., description="The tags of the post.")


class NewsWorkflow:
    team: Team

    def __init__(self) -> None:
        self.team = Team(
            name="New Writing Team",
            mode="coordinate",
            model=Gemini(id="gemini-2.0-flash-001"),
            team_session_state={
                "topic": "technology",
                "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
            members=[
                researcher_agent,
                editor_agent,
                scrapper_agent,
                writer_agent,
                tagger_agent,
            ],
            # debug_mode=True,
            instructions=[
                "You are a team of experts working together to create a blog post about the most relevant and engaging news story of a given topic in PT-BR.",
                "You will work together to research, edit, and write a blog post about the most relevant and engaging news story of a given topic.",
                "You will use the following agents to work together:",
                "1. Researcher Agent - to research the most relevant and engaging news story of the day",
                "2. Editor Agent - to edit the news story and make it more engaging and informative",
                "3. Scrapper Agent - to scrape the news story and get the full content",
                "4. Writer Agent - to write the blog post based on the news story",
                "5. Tagger Agent - to tag the blog post with the most relevant tags",
            ],
            share_member_interactions=False,
            show_members_responses=False,
            add_datetime_to_instructions=True,
            success_criteria="The team has provided a complete blog post in PT-BR about the most relevant and engaging news story of the given topic.",
        )

    def start(self) -> None:
        self.team.print_response(
            "Create a blog post about the technology topic",
            show_full_reasoning=True,
            stream=True,
        )
