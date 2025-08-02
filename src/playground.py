from sys import path as sys_path
from os import path as os_path

from agno.playground import Playground
from dotenv import load_dotenv

load_dotenv()

from ai import CreatePostWorkflow
from ai.agents import (
    editor_agent,
    scrapper_agent,
    researcher_agent,
    tagger_agent,
    writer_agent,
    image_generator_agent,
)

sys_path.append(os_path.dirname(os_path.abspath(__file__)))


playground = Playground(
    name="News Workflow",
    agents=[
        editor_agent,
        scrapper_agent,
        researcher_agent,
        tagger_agent,
        writer_agent,
        image_generator_agent,
    ],
    teams=[CreatePostWorkflow().team],
)

app = playground.get_app()

if __name__ == "__main__":
    playground.serve(app="playground:app", reload=True)
