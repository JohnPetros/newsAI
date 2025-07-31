from textwrap import dedent

from agno.agent import Agent
from agno.models.google import Gemini

from agno.tools.agentql import AgentQLTools

scrapper_agent = Agent(
    name="Scrapper Agent",
    model=Gemini(id="gemini-2.5-pro"),
    role="Scrape the content of the selected website URL.",
    description=dedent(
        """
        You are a news website scraper, your task is to extract the full body of a selected news article, ensuring all relevant.
        Text, media links, and content are captured accurately. This content will then be used for content generation by the writer agent who will craft compelling blog posts based on the scraped data. So, your role is critical in ensuring that the information extracted is comprehensive and clean
        """
    ),
    tools=[AgentQLTools()],
    tool_call_limit=1,
    debug_mode=False,
    instructions=[
        "Scrape and extract the entire body of the most relevant and current news story from its URL for further analysis and transformation into engaging content.",
        "Use the AgentQLTools to scrape the news story.",
        "You should return only the full body of the news story, do not include any other text or information from the website.",
        "Get all the relevant information as you can from the website, do not miss any information.",
    ],
)
