# startup_trends_service.py

import os
import logging
from typing import Dict, Any

from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.google import Gemini
from agno.tools.newspaper4k import Newspaper4kTools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StartupTrendsService:
    """
    A service to perform startup trend analysis using a multi-agent system,
    decoupled from any specific UI.
    """
    
    def __init__(self, google_api_key: str):
        if not google_api_key:
            raise ValueError("Google API key is required.")
        
        self.gemini_model = Gemini(id="gemini-1.5-flash", api_key=google_api_key)
        self._define_agents()

    def _define_agents(self):
        """Initializes the agents for the trend analysis pipeline."""
        
        # Agent 1: Collects news articles
        search_tool = DuckDuckGoTools()
        self.news_collector = Agent(
            name="News Collector",
            role="Collects recent news articles on the given topic",
            tools=[search_tool],
            model=self.gemini_model,
            instructions=["Gather latest articles on the topic"],
            markdown=True,
        )

        # Agent 2: Summarizes the collected articles
        news_tool = Newspaper4kTools(enable_read_article=True, include_summary=True)
        self.summary_writer = Agent(
            name="Summary Writer",
            role="Summarizes collected news articles",
            tools=[news_tool],
            model=self.gemini_model,
            instructions=["Provide concise summaries of the articles"],
            markdown=True,
        )

        # Agent 3: Analyzes trends from the summaries
        self.trend_analyzer = Agent(
            name="Trend Analyzer",
            role="Analyzes trends from summaries",
            model=self.gemini_model,
            instructions=["Identify emerging trends and startup opportunities"],
            markdown=True,
        )

    def analyze_trends(self, topic: str) -> Dict[str, Any]:
        """
        Runs the full 3-step pipeline to analyze startup trends for a given topic.
        """
        if not topic:
            return {"success": False, "error": "A research topic is required."}

        logger.info(f"Starting trend analysis for topic: '{topic}'")
        
        try:
            # Step 1: Collect news
            logger.info("Step 1: Collecting news articles...")
            news_response: RunOutput = self.news_collector.run(f"Collect recent news on {topic}")
            articles = news_response.content
            if not articles:
                raise RuntimeError("News Collector failed to find any articles.")
            logger.info("News collection complete.")

            # Step 2: Summarize articles
            logger.info("Step 2: Summarizing articles...")
            summary_response: RunOutput = self.summary_writer.run(f"Summarize the following articles:\n{articles}")
            summaries = summary_response.content
            if not summaries:
                raise RuntimeError("Summary Writer failed to produce summaries.")
            logger.info("Summarization complete.")

            # Step 3: Analyze trends
            logger.info("Step 3: Analyzing trends...")
            trend_response: RunOutput = self.trend_analyzer.run(f"Analyze trends from the following summaries:\n{summaries}")
            analysis = trend_response.content
            if not analysis:
                raise RuntimeError("Trend Analyzer failed to produce an analysis.")
            logger.info("Trend analysis complete.")

            return {
                "success": True,
                "articles": articles,
                "summaries": summaries,
                "analysis": analysis
            }

        except Exception as e:
            logger.error(f"An error occurred during trend analysis: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

# Example of how to use the service
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Please set GOOGLE_API_KEY in your .env file.")
    else:
        service = StartupTrendsService(google_api_key=api_key)
        research_topic = "AI in personalized education"
        
        print(f"--- Analyzing trends for: {research_topic} ---")
        result = service.analyze_trends(research_topic)
        
        if result["success"]:
            print("\n--- FINAL ANALYSIS ---")
            print(result["analysis"])
        else:
            print(f"\n--- ERROR ---")
            print(result["error"])
