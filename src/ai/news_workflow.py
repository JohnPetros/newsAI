from pathlib import Path
import requests as rest_client

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


class NewsWorkflow:
    team: Team

    def __init__(self) -> None:
        self.team = Team(
            name="News Writing Team",
            mode="coordinate",
            model=Gemini(id="gemini-2.5-pro"),
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

    def start(self) -> None:
        # response = self.team.run(
        #     "Create a blog post about the technology topic",
        #     show_full_reasoning=False,
        #     stream=False,
        # )
        # image_generator_agent.run(response.content)
        # print(f"Response: {response.content}")

        image = Path("image.png")

        with image.open("rb") as file:
            form_data = [
                ("title", "Teste"),
                ("content", "Teste"),
                ("category", "Tecnologia"),
                ("readingTime", "15"),
                ("imageAlt", "Texto da imagem alternativo"),
                ("tags[]", "Tag1"),
                ("tags[]", "Tag2"),
            ]

            response = rest_client.post(
                "http://localhost:4321/api/posts",
                data=form_data,
                files={"image": (image.name, file, "image/png")},
                timeout=30,
            )
            print(response.json())
