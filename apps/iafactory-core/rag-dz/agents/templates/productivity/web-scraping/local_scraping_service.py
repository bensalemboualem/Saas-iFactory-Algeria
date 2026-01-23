# local_scraping_service.py

import logging
from typing import Dict, Any, Optional

from scrapegraphai.graphs import SmartScraperGraph

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LocalScrapingService:
    """
    A service to perform web scraping using ScrapeGraphAI's SmartScraperGraph,
    supporting both OpenAI and Ollama LLM configurations.
    """
    
    def __init__(self, llm_config: Dict[str, Any]):
        if not llm_config:
            raise ValueError("LLM configuration is required.")
        
        self.llm_config = llm_config
        logger.info(f"LocalScrapingService initialized with LLM config: {llm_config.get('llm', {}).get('model', 'Unknown')}")

    def scrape_url(self, url: str, user_prompt: str) -> Dict[str, Any]:
        """
        Scrapes the given URL using the configured SmartScraperGraph.
        """
        if not url or not user_prompt:
            return {"success": False, "error": "URL and user prompt are required for scraping."}

        logger.info(f"Starting scraping for URL: '{url}' with prompt: '{user_prompt[:50]}...'")
        
        try:
            # SmartScraperGraph is initialized here with the given prompt and source
            # The config object should already contain the LLM details
            smart_scraper_graph = SmartScraperGraph(
                prompt=user_prompt,
                source=url,
                config=self.llm_config
            )
            
            result = smart_scraper_graph.run()
            
            if result:
                logger.info(f"Successfully scraped URL: '{url}'.")
                return {
                    "success": True,
                    "result": result
                }
            else:
                logger.info(f"ScrapeGraphAI did not produce any content for '{url}'.")
                return {
                    "success": False,
                    "error": "ScrapeGraphAI did not produce any content."
                }

        except Exception as e:
            logger.error(f"An error occurred during web scraping: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

# Example of how to use the service
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    # --- OpenAI Configuration Example ---
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        openai_llm_config = {
            "llm": {
                "api_key": openai_key,
                "model": "gpt-4o", # or "gpt-5"
            },
        }
        openai_service = LocalScrapingService(llm_config=openai_llm_config)
        print("--- OpenAI Scraping Example ---")
        openai_result = openai_service.scrape_url(
            url="https://www.cnbc.com/id/10000113",
            user_prompt="Summarize the article"
        )
        if openai_result["success"]:
            print(openai_result["result"])
        else:
            print(f"OpenAI Scraping Error: {openai_result['error']}")
    else:
        print("OPENAI_API_KEY not set. Skipping OpenAI example.")

    print("\n" + "="*50 + "\n")

    # --- Ollama Configuration Example ---
    # Ensure Ollama is running locally on port 11434
    ollama_llm_config = {
        "llm": {
            "model": "ollama/llama3.2", # Make sure this model is downloaded in Ollama
            "temperature": 0,
            "format": "json",
            "base_url": "http://localhost:11434",
        },
        "embeddings": {
            "model": "ollama/nomic-embed-text",
            "base_url": "http://localhost:11434",
        },
        "verbose": False,
    }
    ollama_service = LocalScrapingService(llm_config=ollama_llm_config)
    print("--- Ollama Scraping Example ---")
    ollama_result = ollama_service.scrape_url(
        url="https://www.theguardian.com/science/2024/jan/01/ai-breakthrough-year-2023",
        user_prompt="Extract the main points about AI breakthroughs in 2023"
    )
    if ollama_result["success"]:
        print(ollama_result["result"])
    else:
        print(f"Ollama Scraping Error: {ollama_result['error']}")
