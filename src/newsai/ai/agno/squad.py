from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat

from newsai.ai.agno.schemas import (
    EditorialBriefSchema,
    EditorialTone,
    NewsPostDraftSchema,
    ResearchCandidatesSchema,
    ScrapedArticleSchema,
    TagListSchema,
)
from newsai.ai.agno.toolset import Toolset
from newsai.constants import ENV


class Squad:
    @property
    def fast_model(self) -> OpenAIChat:
        return OpenAIChat(id="gpt-4o-mini", api_key=ENV.openai_api_key)

    @property
    def reasoning_model(self) -> OpenAIChat:
        return OpenAIChat(id="gpt-4o", api_key=ENV.openai_api_key)

    @property
    def editor_agent(self) -> Agent:
        return Agent(
            id="editor-agent",
            name="Editor Agent",
            model=self.fast_model,
            role="Select the most relevant and engaging news story to be used as the foundation for a compelling blog post",
            output_schema=EditorialBriefSchema,
            description=dedent(
                """
                You are an expert editor with extensive experience in digital content curation and SEO optimization. Your task is to analyze and select the most impactful and engaging news story in PT-BR that will serve as the foundation for a compelling blog post. You have a deep understanding of what makes content viral and resonates with Brazilian audiences. You should evaluate each story's potential for reader engagement, social sharing, and search engine visibility while ensuring the selected content maintains high journalistic standards and credibility. Your expertise in identifying trending topics and understanding audience preferences will be crucial in choosing content that will drive traffic and foster meaningful discussions.
                """
            ),
            debug_mode=True,
            instructions=[
                "Analyze the research candidates and the scraped article to define the editorial direction for the post.",
                "Select the most relevant story candidate based on credibility, timeliness, and engagement potential.",
                "Return the selected source URL in `selected_url`.",
                "Return a concise PT-BR article title in `title`.",
                "Return the editorial angle in `angle`.",
                f"Return the journalistic tone in `tone` using one of: {EditorialTone.SERIOUS.value}, {EditorialTone.ANALYTIC.value}, {EditorialTone.ENTHUSIASTIC.value}.",
                "Return the intended audience in `audience`.",
                "Return the central question the article should answer in `central_question`.",
                "Return exactly 3 key factual bullet points in `key_facts`.",
                "Return at least 3 ordered sections for the writer in `structure`.",
                "Return optional editorial pitfalls to avoid in `avoid_points`.",
                "Use only facts present in the provided content.",
            ],
        )

    @property
    def researcher_agent(self) -> Agent:
        return Agent(
            id="researcher-agent",
            name="Researcher Agent",
            model=self.reasoning_model,
            role="Conduct research to identify the top trending news stories of the day that can inspire engaging and relevant blog content",
            debug_mode=True,
            output_schema=ResearchCandidatesSchema,
            description=dedent(
                """
                You are an expert researcher, your task is to uncover the most current and impactful news stories, ensuring they are timely and suitable for creating compelling blog posts",
                "Research the top trending news stories in Brazil for the past 12 hours from reliable Brazilian news sources about the topic {topic}.
                """
            ),
            instructions=[
                "Research exactly 5 strong Brazilian news story candidates from the last 24 hours about the requested category.",
                "The news stories should be in Portuguese.",
                "Use the search_news_tool to search for the news stories.",
                "Return the results in `candidates`.",
                "For each candidate, return `title`, `url`, `summary`, `why_it_matters`, `main_development`, and `affected_people`.",
                "Prefer candidates with clear novelty, impact, and trustworthy sourcing.",
                "Do not invent sources or URLs.",
            ],
            add_datetime_to_context=True,
            tools=[Toolset.search_news_tool],
            tool_call_limit=1,
        )

    @property
    def scrapper_agent(self) -> Agent:
        return Agent(
            id="scrapper-agent",
            name="Scrapper Agent",
            model=self.fast_model,
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
                "Return the article headline in `headline`.",
                "Return the publication or site name in `source_name`.",
                "Return the publication date or visible timestamp in `published_at`.",
                "Return the cleaned article body in `content`.",
                "Return notable direct quotes in `key_quotes` when available.",
                "Return the main named entities in `entities`.",
                "Get all the relevant information you can from the website without inventing missing details.",
            ],
        )

    @property
    def tagger_agent(self) -> Agent:
        return Agent(
            id="tagger-agent",
            name="Tagger Agent",
            model=self.fast_model,
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
            model=self.reasoning_model,
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
                "Use the editorial brief to define the lead, the narrative order, and the emphasis of the article.",
                "Write a strong opening paragraph with the most newsworthy fact.",
                "Use the scraped facts, entities, and quotes to make the article specific and concrete.",
                "Return the final title in `title`.",
                "Return the HTML body in `content`.",
                "Return the source URL in `original_url`.",
                "Return the calculated integer reading time in `reading_time`.",
            ],
        )

    @property
    def reviewer_agent(self) -> Agent:
        return Agent(
            id="reviewer-agent",
            name="Reviewer Agent",
            model=self.reasoning_model,
            role="Review and improve a drafted news blog post before publication.",
            description="You are a senior editorial reviewer responsible for improving clarity, factual discipline, structure, and style without inventing any information.",
            debug_mode=False,
            output_schema=NewsPostDraftSchema,
            instructions=[
                "Review the provided blog post draft against the research, scraped article, and editorial brief.",
                "Preserve all verified facts and never invent new information.",
                "Improve the lead, flow, paragraph rhythm, clarity, and specificity when needed.",
                "Remove repetition, vague statements, hype language, and moralizing conclusions.",
                "Keep the post in PT-BR and in HTML format suitable for the <body> tag.",
                "Preserve the original source URL in `original_url`.",
                "Return the improved title in `title`.",
                "Return the improved HTML body in `content`.",
                "Return the updated integer reading time in `reading_time`.",
            ],
        )
