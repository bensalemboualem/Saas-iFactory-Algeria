# journalist_service.py

from textwrap import dedent
import logging
from typing import Dict, Any
import os

from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.tools.serpapi import SerpApiTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.models.openai import OpenAIChat

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JournalistService:
    """
    A service to generate high-quality articles using a multi-agent system,
    decoupled from any specific UI.
    """
    
    def __init__(self, openai_api_key: str, serp_api_key: str):
        if not openai_api_key or not serp_api_key:
            raise ValueError("OpenAI and SerpAPI keys are required.")
        
        self.openai_api_key = openai_api_key
        self.serp_api_key = serp_api_key
        
        self._define_agents()

    def _define_agents(self):
        """Initializes the agents for the article generation pipeline."""
        
        # Searcher Agent
        search_tool = SerpApiTools(api_key=self.serp_api_key)
        self.searcher = Agent(
            name="Searcher",
            role="Searches for top URLs based on a topic",
            model=OpenAIChat(id="gpt-4o", api_key=self.openai_api_key),
            description=dedent(
                """
            You are a world-class journalist for the New York Times. Given a topic, generate a list of 3 search terms
            for writing an article on that topic. Then search the web for each term, analyse the results
            and return the 10 most relevant URLs.
            """
            ),
            instructions=[
                "Given a topic, first generate a list of 3 search terms related to that topic.",
                "For each search term, `search_google` and analyze the results."
                "From the results of all searcher, return the 10 most relevant URLs to the topic.",
                "Remember: you are writing for the New York Times, so the quality of the sources is important.",
            ],
            tools=[search_tool],
            add_datetime_to_context=True,
        )

        # Writer Agent
        news_tool = Newspaper4kTools(enable_read_article=True, include_summary=True)
        self.writer = Agent(
            name="Writer",
            role="Retrieves text from URLs and writes a high-quality article",
            model=OpenAIChat(id="gpt-4o", api_key=self.openai_api_key),
            description=dedent(
                """
            You are a senior writer for the New York Times. Given a topic and a list of URLs,
            your goal is to write a high-quality NYT-worthy article on the topic.
            """
            ),
            instructions=[
                "Given a topic and a list of URLs, first read the article using `get_article_text`."
                "Then write a high-quality NYT-worthy article on the topic."
                "The article should be well-structured, informative, and engaging",
                "Ensure the length is at least as long as a NYT cover story -- at a minimum, 15 paragraphs.",
                "Ensure you provide a nuanced and balanced opinion, quoting facts where possible.",
                "Remember: you are writing for the New York Times, so the quality of the article is important.",
                "Focus on clarity, coherence, and overall quality.",
                "Never make up facts or plagiarize. Always provide proper attribution.",
            ],
            tools=[news_tool],
            add_datetime_to_context=True,
            markdown=True,
        )

        # Editor Agent (coordinates Searcher and Writer)
        self.editor = Agent(
            name="Editor",
            model=OpenAIChat(id="gpt-4o", api_key=self.openai_api_key),
            team=[self.searcher, self.writer],
            description="You are a senior NYT editor. Given a topic, your goal is to write a NYT worthy article.",
            instructions=[
                "Given a topic, ask the search journalist to search for the most relevant URLs for that topic.",
                "Then pass a description of the topic and URLs to the writer to get a draft of the article.",
                "Edit, proofread, and refine the article to ensure it meets the high standards of the New York Times.",
                "The article should be extremely articulate and well written. "
                "Focus on clarity, coherence, and overall quality.",
                "Ensure the article is engaging and informative.",
                "Remember: you are the final gatekeeper before the article is published.",
            ],
            add_datetime_to_context=True,
            markdown=True,
        )

    def generate_article(self, topic: str) -> Dict[str, Any]:
        """
        Runs the full multi-agent pipeline to generate an article for a given topic.
        """
        if not topic:
            return {"success": False, "error": "An article topic is required."}

        logger.info(f"Starting article generation for topic: '{topic}'")
        
        try:
            # The editor agent orchestrates the entire process
            response: RunOutput = self.editor.run(topic, stream=False)
            
            if response and response.content:
                logger.info(f"Successfully generated article for '{topic}'.")
                return {
                    "success": True,
                    "article": response.content
                }
            else:
                logger.error("Editor agent run did not produce any content.")
                return {
                    "success": False,
                    "error": "Editor agent run did not produce any content."
                }

        except Exception as e:
            logger.error(f"An error occurred during article generation: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

# Example of how to use the service
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    openai_key = os.getenv("OPENAI_API_KEY")
    serp_key = os.getenv("SERP_API_KEY")

    if not openai_key or not serp_key:
        print("Please set OPENAI_API_KEY and SERP_API_KEY in your .env file.")
    else:
        service = JournalistService(openai_api_key=openai_key, serp_api_key=serp_key)
        article_topic = "The future of AI in content creation"
        
        print(f"--- Generating article for: {article_topic} ---")
        result = service.generate_article(article_topic)
        
        if result["success"]:
            print("\n--- GENERATED ARTICLE ---")
            print(result["article"])
        else:
            print(f"\n--- ERROR ---")
            print(result["error"])
