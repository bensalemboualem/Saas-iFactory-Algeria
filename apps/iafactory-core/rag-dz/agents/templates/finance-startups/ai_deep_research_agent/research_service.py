# research_service.py

import asyncio
from typing import Dict, Any, List
import logging

from agents import Agent, Runner, set_default_openai_key
from firecrawl import FirecrawlApp
from agents.tool import function_tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResearchService:
    """
    A service to perform deep research using OpenAI agents and Firecrawl,
    decoupled from any specific UI.
    """
    
    def __init__(self, openai_api_key: str, firecrawl_api_key: str):
        if not openai_api_key or not firecrawl_api_key:
            raise ValueError("OpenAI and Firecrawl API keys are required.")
        self.openai_api_key = openai_api_key
        self.firecrawl_api_key = firecrawl_api_key
        
        # Set the default OpenAI key for the agents SDK
        set_default_openai_key(self.openai_api_key)
        
        # Define agents and tools within the service context
        self._define_tools_and_agents()

    def _define_tools_and_agents(self):
        """Initializes the tools and agents."""
        
        # The tool needs access to the firecrawl_api_key from the instance
        @function_tool
        async def deep_research(query: str, max_depth: int = 3, time_limit: int = 180, max_urls: int = 10) -> Dict[str, Any]:
            """
            Perform comprehensive web research using Firecrawl's deep research endpoint.
            """
            logger.info(f"[Firecrawl] Starting deep research for query: {query}")
            try:
                firecrawl_app = FirecrawlApp(api_key=self.firecrawl_api_key)
                params = {"maxDepth": max_depth, "timeLimit": time_limit, "maxUrls": max_urls}
                
                # Note: on_activity callback is removed as it's a UI feature.
                # Logging can be used for tracking progress in a backend context.
                results = firecrawl_app.deep_research(query=query, params=params)
                
                logger.info("[Firecrawl] Deep research completed successfully.")
                return {
                    "success": True,
                    "final_analysis": results['data']['finalAnalysis'],
                    "sources_count": len(results['data']['sources']),
                    "sources": results['data']['sources']
                }
            except Exception as e:
                logger.error(f"[Firecrawl] Deep research error: {str(e)}")
                return {"error": str(e), "success": False}

        self.research_agent = Agent(
            name="research_agent",
            instructions="""You are a research assistant that can perform deep web research on any topic.
            When given a research topic or question:
            1. Use the deep_research tool to gather comprehensive information.
            2. The tool will search the web, analyze multiple sources, and provide a synthesis.
            3. Review the research results and organize them into a well-structured report.
            4. Include proper citations for all sources.
            5. Highlight key findings and insights.
            """,
            tools=[deep_research]
        )

        self.elaboration_agent = Agent(
            name="elaboration_agent",
            instructions="""You are an expert content enhancer specializing in research elaboration.
            When given a research report:
            1. Analyze the structure and content of the report.
            2. Enhance the report by adding more detailed explanations, examples, case studies, and real-world applications.
            3. Expand on key points with additional context and nuance.
            4. Maintain academic rigor and factual accuracy.
            5. Ensure all additions are relevant and valuable to the topic.
            """
        )

    async def run_full_research(self, topic: str) -> Dict[str, Any]:
        """
        Run the complete two-step research process and return the results.
        """
        logger.info(f"Starting full research process for topic: '{topic}'")
        try:
            # Step 1: Initial Research
            logger.info("Running initial research agent...")
            research_result = await Runner.run(self.research_agent, topic)
            if not research_result or not research_result.final_output:
                raise RuntimeError("Initial research failed to produce an output.")
            initial_report = research_result.final_output
            logger.info("Initial research completed.")

            # Step 2: Enhance the report
            logger.info("Running elaboration agent...")
            elaboration_input = f"""
            RESEARCH TOPIC: {topic}
            
            INITIAL RESEARCH REPORT:
            {initial_report}
            
            Please enhance this research report with additional information, examples, case studies, 
            and deeper insights while maintaining its academic rigor and factual accuracy.
            """
            elaboration_result = await Runner.run(self.elaboration_agent, elaboration_input)
            if not elaboration_result or not elaboration_result.final_output:
                raise RuntimeError("Elaboration failed to produce an output.")
            enhanced_report = elaboration_result.final_output
            logger.info("Elaboration completed.")

            return {
                "success": True,
                "initial_report": initial_report,
                "enhanced_report": enhanced_report
            }

        except Exception as e:
            logger.error(f"An error occurred during the research process: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

# Example of how to use the service
async def main():
    import os
    from dotenv import load_dotenv
    load_dotenv()

    openai_key = os.getenv("OPENAI_API_KEY")
    firecrawl_key = os.getenv("FIRECRAWL_API_KEY")

    if not openai_key or not firecrawl_key:
        print("Please set OPENAI_API_KEY and FIRECRAWL_API_KEY in your .env file.")
        return

    service = ResearchService(openai_api_key=openai_key, firecrawl_api_key=firecrawl_key)
    research_topic = "Latest advancements in battery technology"
    results = await service.run_full_research(research_topic)

    if results["success"]:
        print("--- ENHANCED REPORT ---")
        print(results["enhanced_report"])
    else:
        print(f"--- ERROR ---")
        print(results["error"])

if __name__ == "__main__":
    asyncio.run(main())
