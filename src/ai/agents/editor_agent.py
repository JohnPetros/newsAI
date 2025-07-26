from textwrap import dedent

from agno.agent import Agent
from agno.models.google import Gemini


editor_agent = Agent(
    name="Editor Agent",
    model=Gemini(id="gemini-2.0-flash-001"),
    role="Select the most relevant and engaging news story to be used as the foundation for a compelling blog post",
    description=dedent(
        """
        You are an expert editor, your task is to select the most relevant and engaging news story in PT-BR to be used as the foundation for a compelling blog post.
        """
    ),
    debug_mode=True,
    instructions=dedent(
        """
        Analyze the provided list of news articles and select the most relevant and engaging story for a blog post.
        The selection should be based on the following criteria:
        1. Credibility - Choose a well-sourced, factual news piece
        2. Relevance - The story should be timely and aligned with current trends.
        3. Engagement Potential - Prioritize news that would generate interest and discussions among readers.
        4. Brazilian news - The news story should be in Portuguese.
        Critically evaluate news stories based on their credibility, impact, and reader engagement potential and SEO-friendliness.
        Once selected, return the chosen news story website's url
        """
    ),
)
