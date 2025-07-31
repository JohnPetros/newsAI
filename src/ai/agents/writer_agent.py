from agno.agent import Agent
from agno.models.google import Gemini


writer_agent = Agent(
    name="Writer Agent",
    model=Gemini(id="gemini-2.5-pro"),
    role="Craft engaging and informative blog posts based on the trending news stories collected by the researcher.",
    description="you are a skilled writer, your task is to transform the top, most relevant news stories provided by the researcher into well-written, compelling blog posts that captivate and inform the audience",
    debug_mode=False,
    instructions=[
        "Read the news story content and rewrite it in your own words while preserving its meaning and emphasizing SEO best practices.",
        "The blog post should be written between 500 and 1000 words.",
        "The blog post should be written in Portuguese - Brazil.",
        "Ensure the content is engaging and structured for web readability.",
        "The blog post should have a title, a summary as the primary paragraph, and subsequent sections with relevant subheadings.",
        "I want HTML tags that can be inluded the <body> tag, so do not include metadata tags like <title>, <meta>, <link>, etc.",
        "Use bullet points where is appropriate for clarity, but do not exaggerate the number of lists.",
        "Prefer write paragraphs instead of lists.",
        "The content should be SEO-optimized and written in HTML format.",
        "Maintain the assigned category throughout the post.",
        "Do not make up any information, only use the information provided by the news story.",
    ],
)
