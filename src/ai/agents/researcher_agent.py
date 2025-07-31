from textwrap import dedent

from agno.agent import Agent

from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.google import Gemini


researcher_agent = Agent(
    name="Researcher Agent",
    model=Gemini(id="gemini-2.0-flash"),
    role="Conduct research to identify the top trending news stories of the day that can inspire engaging and relevant blog content",
    debug_mode=True,
    description=dedent(
        """
        You are an expert researcher, your task is to uncover the most current and impactful news stories, ensuring they are timely and suitable for creating compelling blog posts",
        "Research the top trending news stories in Brazil for the past 12 hours from reliable Brazilian news sources about the topic {topic}.
        """
    ),
    instructions=[
        "Research 5 top trending news stories in Brazil for the past 12 hours from reliable Brazilian news sources about the topic {topic}.",
        "If the news story is already in the database, you should not research it again.",
        "The news stories should be in Portuguese.",
        "Use the DuckDuckGoTools to search for the news stories.",
        "You should return a list of five top Brazilian news story including titles, their corresponding URLs, and a brief summary for each story from the past 24 hours. All in Portuguese.",
    ],
    add_datetime_to_instructions=True,
    tools=[DuckDuckGoTools()],
    tool_call_limit=2,
    show_tool_calls=True,
)
