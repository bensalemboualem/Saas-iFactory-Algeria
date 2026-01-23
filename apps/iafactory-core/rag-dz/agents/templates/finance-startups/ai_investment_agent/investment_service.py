# investment_service.py

import os
import logging
from typing import Dict, Any

from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InvestmentService:
    """
    A service to perform investment analysis by comparing two stocks,
    decoupled from any specific UI.
    """
    
    def __init__(self, openai_api_key: str):
        if not openai_api_key:
            raise ValueError("OpenAI API key is required.")
        
        self.assistant = Agent(
            model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
            tools=[
                YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)
            ],
            debug_mode=True, # Can be set to False in production
            description="You are an expert investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
            instructions=[
                "Format your response using markdown and use tables to display data where possible."
            ],
        )

    def compare_stocks(self, stock1: str, stock2: str) -> Dict[str, Any]:
        """
        Compares two stocks and generates a detailed report.
        """
        if not stock1 or not stock2:
            return {"success": False, "error": "Both stock symbols are required."}

        logger.info(f"Starting comparison between {stock1} and {stock2}.")
        
        try:
            query = f"Compare both the stocks - {stock1} and {stock2} and make a detailed report for an investor trying to invest and compare these stocks"
            
            # The .run() method in agno is synchronous
            response: RunOutput = self.assistant.run(query, stream=False)
            
            if response and response.content:
                logger.info(f"Successfully generated report for {stock1} vs {stock2}.")
                return {
                    "success": True,
                    "report": response.content
                }
            else:
                logger.error("Agent run did not produce any content.")
                return {
                    "success": False,
                    "error": "Agent run did not produce any content."
                }

        except Exception as e:
            logger.error(f"An error occurred during stock comparison: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

# Example of how to use the service
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY in your .env file.")
    else:
        service = InvestmentService(openai_api_key=api_key)
        stock_1 = "GOOGL"
        stock_2 = "META"
        
        print(f"--- Comparing {stock_1} and {stock_2} ---")
        result = service.compare_stocks(stock_1, stock_2)
        
        if result["success"]:
            print(result["report"])
        else:
            print(f"Error: {result['error']}")
