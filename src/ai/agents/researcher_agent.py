from textwrap import dedent

from agno.agent import Agent

from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.google import Gemini


researcher_agent = Agent(
    name="Researcher Agent",
    model=Gemini(id="gemini-2.0-flash-001"),
    role="Conduct research to identify the top trending news stories of the day that can inspire engaging and relevant blog content",
    debug_mode=True,
    description=dedent(
        """
        You are an expert researcher, your task is to uncover the most current and impactful news stories, ensuring they are timely and suitable for creating compelling blog posts",
        "Research the top trending news stories in Brazil for the past 12 hours from reliable Brazilian news sources about the topic {topic}.
        """
    ),
    instructions=[
        "Research the top trending news stories in Brazil for the past 12 hours from reliable Brazilian news sources about the topic {topic}.",
        "Use the TavilyTools to search for the news stories.",
        "You should return a list of five top Brazilian news story including titles, their corresponding URLs, and a brief summary for each story from the past 24 hours. All in Portuguese.",
    ],
    add_datetime_to_instructions=True,
    tools=[DuckDuckGoTools()],
    tool_call_limit=1,
    show_tool_calls=True,
)
