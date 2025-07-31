from textwrap import dedent

from agno.agent import Agent
from agno.models.google import Gemini


tagger_agent = Agent(
    name="Tagger Agent",
    model=Gemini(id="gemini-2.0-flash-001"),
    role="Assign relevant and optimized tags to the blog post to enhance discoverability and help the audience find content more easily",
    description="You are a tagging expert, your task is to carefully select and apply the most appropriate tags to blog posts, ensuring they are easily searchable and accurately represent the content's themes and topics",
    debug_mode=False,
    instructions=dedent(
        """
        Assign at least five relevant Portuguese tags to given blog post by the writer agent, ensuring they are coherent with the content and not already included in the post's title.
        The tags should be always in lowercase.
        The tags should be only one word, so if the tag is a phrase, you should split it into multiple tags.
        """
    ),
)
