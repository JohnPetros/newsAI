from sys import path as sys_path
from os import path as os_path

from agno.playground import Playground
from dotenv import load_dotenv

load_dotenv()

from newsai.ai import Workflow
from newsai.ai.squad import Squad

sys_path.append(os_path.dirname(os_path.abspath(__file__)))

squad = Squad()


playground = Playground(
    name="News Workflow",
    agents=[
        squad.editor_agent,
        squad.scrapper_agent,
        squad.researcher_agent,
        squad.tagger_agent,
        squad.writer_agent,
        squad.image_generator_agent,
    ],
    teams=[Workflow().team],
)

app = playground.get_app()

if __name__ == "__main__":
    playground.serve(app="newsai.playground:app", reload=True)
