from textwrap import dedent

from agno.agent import Agent
from agno.models.google import Gemini
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools

from newsai.ai.agno.schemas import (
    EditorialBriefSchema,
    ImageGenerationSchema,
    NewsPostDraftSchema,
    ResearchResultSchema,
    ScrapedArticleSchema,
    TagListSchema,
)
from newsai.ai.agno.toolset import Toolset


class Squad:
    @property
    def editor_agent(self) -> Agent:
        return Agent(
            id="editor-agent",
            name="Editor Agent",
            model=Gemini(id="gemini-3-flash-preview"),
            role="Select the most relevant and engaging news story to be used as the foundation for a compelling blog post",
            output_schema=EditorialBriefSchema,
            description=dedent(
                """
                You are an expert editor with extensive experience in digital content curation and SEO optimization. Your task is to analyze and select the most impactful and engaging news story in PT-BR that will serve as the foundation for a compelling blog post. You have a deep understanding of what makes content viral and resonates with Brazilian audiences. You should evaluate each story's potential for reader engagement, social sharing, and search engine visibility while ensuring the selected content maintains high journalistic standards and credibility. Your expertise in identifying trending topics and understanding audience preferences will be crucial in choosing content that will drive traffic and foster meaningful discussions.
                """
            ),
            debug_mode=True,
            instructions=[
                "Analyze the research results and the scraped article to define the editorial direction for the post.",
                "Select the most relevant story based on credibility, timeliness, and engagement potential.",
                "Return the selected source URL in `selected_url`.",
                "Return a concise PT-BR article title in `title`.",
                "Return the editorial angle in `angle`.",
                "Return the journalistic tone in `tone`.",
                "Return exactly 3 key factual bullet points in `key_facts`.",
                "Return at least 3 ordered sections for the writer in `structure`.",
                "Use only facts present in the provided content.",
            ],
        )

    @property
    def researcher_agent(self) -> Agent:
        return Agent(
            id="researcher-agent",
            name="Researcher Agent",
            model=Gemini(id="gemini-3-pro-preview"),
            role="Conduct research to identify the top trending news stories of the day that can inspire engaging and relevant blog content",
            debug_mode=True,
            output_schema=ResearchResultSchema,
            description=dedent(
                """
                You are an expert researcher, your task is to uncover the most current and impactful news stories, ensuring they are timely and suitable for creating compelling blog posts",
                "Research the top trending news stories in Brazil for the past 12 hours from reliable Brazilian news sources about the topic {topic}.
                """
            ),
            instructions=[
                "Research the single best Brazilian news story from the last 24 hours about the requested category.",
                "The news stories should be in Portuguese.",
                "Use the DuckDuckGoTools to search for the news stories.",
                "Return the selected story title in `title`.",
                "Return the story URL in `url`.",
                "Return a concise factual summary in `summary`.",
                "Do not invent sources or URLs.",
            ],
            add_datetime_to_context=True,
            tools=[DuckDuckGoTools()],
            tool_call_limit=1,
        )

    @property
    def scrapper_agent(self) -> Agent:
        return Agent(
            id="scrapper-agent",
            name="Scrapper Agent",
            model=Gemini(id="gemini-3-flash-preview"),
            role="Scrape the content of the selected website URL.",
            output_schema=ScrapedArticleSchema,
            description=dedent(
                """
                You are a news website scraper, your task is to extract the full body of a selected news article, ensuring all relevant.
                Text, media links, and content are captured accurately. This content will then be used for content generation by the writer agent who will craft compelling blog posts based on the scraped data. So, your role is critical in ensuring that the information extracted is comprehensive and clean
                """
            ),
            tools=[Toolset.scrape_website_tool],
            tool_call_limit=1,
            debug_mode=True,
            instructions=[
                "Scrape and extract the entire body of the most relevant and current news story from its URL for further analysis and transformation into engaging content.",
                "Use the scrap_website_tool to scrape the news story.",
                "Return the input URL in `url`.",
                "Return the cleaned article body in `content`.",
                "Get all the relevant information you can from the website without inventing missing details.",
            ],
        )

    @property
    def tagger_agent(self) -> Agent:
        return Agent(
            id="tagger-agent",
            name="Tagger Agent",
            model=Gemini(id="gemini-3-flash-preview"),
            role="Assign relevant and optimized tags to the blog post to enhance discoverability and help the audience find content more easily",
            description="You are a tagging expert, your task is to carefully select and apply the most appropriate tags to blog posts, ensuring they are easily searchable and accurately represent the content's themes and topics",
            debug_mode=False,
            output_schema=TagListSchema,
            instructions=[
                "Assign at least five relevant Portuguese tags to given blog post by the writer agent, ensuring they are coherent with the content and not already included in the post's title.",
                "The tags should be always in lowercase.",
                "The tags should be only one word, so if the tag is a phrase, you should split it into multiple tags.",
                "Return the final list in `tags`.",
            ],
        )

    @property
    def writer_agent(self) -> Agent:
        return Agent(
            id="writer-agent",
            name="Writer Agent",
            model=Gemini(id="gemini-3-pro-preview"),
            role="Craft engaging and informative blog posts based on the trending news stories collected by the researcher.",
            description="you are a very skilled senior writer, your task is to transform the top, most relevant news stories provided by the researcher into well-written, compelling blog posts that captivate and inform the audience",
            debug_mode=False,
            output_schema=NewsPostDraftSchema,
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
                "Avoid empty adjectives like 'vibrant', 'cultural tapestry', 'guiding thread', 'world in transformation'.",
                "Do not use retorical language, and do not repeat the same information.",
                "Do not write a moralizing conclusion. End with a powerful sentence or a useful piece of information.",
                "Do not make up any information, only use the information provided by the news story.",
                "Use proper names. Cite real people, places, and works (which was provided in context).",
                "Return the final title in `title`.",
                "Return the HTML body in `content`.",
                "Return the source URL in `original_url`.",
                "Return the calculated integer reading time in `reading_time`.",
                "Return preliminary tags in `tags` if available from the provided context.",
            ],
        )

    @property
    def image_generator_agent(self) -> Agent:
        return Agent(
            id="image-generator-agent",
            name="Image Generator Agent",
            model=Gemini(id="gemini-3-pro-preview"),
            role="Generate an image for a blog post according to the provided content using an advanced image generation tool that is able to generate images from textual prompts.",
            description="You are an expert image generator with extensive experience in generating images for blog posts using AI.",
            debug_mode=True,
            output_schema=ImageGenerationSchema,
            tools=[Toolset.generate_image_tool],
            tool_call_limit=1,
            instructions=[
                "Analyze the provided data of the blog post in JSON format and generate an image for it.",
                "The image should be realistic, not surreal, and very coherent with the content of the blog post.",
                "The image should trigger emotions and curiosity in the reader so that they want to read the blog post.",
                "Create a prompt for the image generation tool to generate the image.",
                "The prompt should be in English for better image generation results.",
                "Use the `gen_image_tool` to generate the image.",
                "After the image is generated, create an altertive text (alt) for the image in Portuguese - PT-BR.",
                "Return the alt text in `image_alt`.",
            ],
        )

    @property
    def news_writing_team(self) -> Team:
        return Team(
            name="News Writing Team",
            model=Gemini(id="gemini-3-pro-preview"),
            output_schema=NewsPostDraftSchema,
            members=[
                self.researcher_agent,
                self.editor_agent,
                self.scrapper_agent,
                self.writer_agent,
                self.tagger_agent,
            ],
            debug_mode=False,
            instructions=[
                "You are an elite journalistic team creating a high-quality blog post in PT-BR.",
                "CRITICAL RULE: You must be strictly faithful to the current date provided in the context. If today is Feb 3rd, DO NOT write about events in May or August as if they have already happened. Treat future events as future.",
                "CRITICAL RULE: Do not halluncinate information. All names, dates, and facts must come from the researched and scraped content.",
                "You will execute the pipeline in this strict order:",
                "1. Researcher Agent: Search for the most relevant/trending news story of the LAST 24 HOURS on the given topic. Return the specific URL.",
                "   - Filter out 'evergreen' content or generic articles. Look for breaking news.",
                "2. Scrapper Agent: Scrape the FULL content from the URL provided by the Researcher. Extract the raw text.",
                "3. Editor Agent: Analyze the scraped text and define the 'Angle' of the story.",
                "   - Identify the 3 most important facts.",
                "   - Decide on a journalistic tone (Serious, Analytic, or Enthusiastic).",
                "   - Create a structure for the Writer.",
                "4. Writer Agent: Write the blog post in PT-BR based ONLY on the Editor's plan and Scrapper's data.",
                "   - STYLE GUIDE: Write like a senior journalist from 'Folha de S.Paulo' or 'The New York Times'.",
                "   - Avoid AI clichés like 'No cenário atual', 'Tapeçaria cultural', 'Mergulhamos', 'Em suma'.",
                "   - Use specific entities (Names of people, places, values, dates).",
                "   - Paragraphs should be short and punchy.",
                "   - If the news is about the future, use 'Will', 'Expected to', 'Scheduled for'. Never use past tense for future events.",
                "5. Tagger Agent: Generate 5 relevant SEO tags in PT-BR.",
                "Calculate the reading time based on the final word count (avg 200 words/min).",
                "Return structured fields for title, content, tags, reading_time, and original_url.",
            ],
            share_member_interactions=False,
            show_members_responses=False,
            add_datetime_to_context=True,
        )
