# rag_reasoning_service.py

import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from agno.vectordb.lancedb import LanceDb, SearchType
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RagReasoningService:
    """
    A service to perform agentic RAG with reasoning capabilities,
    decoupled from any specific UI.
    """
    
    def __init__(self, google_api_key: str, openai_api_key: str):
        if not google_api_key or not openai_api_key:
            raise ValueError("Google and OpenAI API keys are required.")
        
        # Initialize knowledge base (LanceDB with OpenAI embeddings)
        self.knowledge = Knowledge(
            vector_db=LanceDb(
                uri="tmp/lancedb",  # LanceDB will create files here
                table_name="agno_docs",
                search_type=SearchType.vector,
                embedder=OpenAIEmbedder(api_key=openai_api_key),
            ),
        )
        
        # Initialize Agno agent with Gemini and reasoning tools
        self.agent = Agent(
            model=Gemini(id="gemini-1.5-flash", api_key=google_api_key),
            knowledge=self.knowledge,
            search_knowledge=True,
            tools=[ReasoningTools(add_instructions=True)],
            instructions=[
                "Include sources in your response.",
                "Always search your knowledge before answering the question.",
            ],
            markdown=True,
        )
        
        self.urls_loaded = set() # To track loaded URLs

        # Load default URL if not already loaded
        default_url = "https://www.theunwindai.com/p/mcp-vs-a2a-complementing-or-supplementing"
        if default_url not in self.urls_loaded:
            self.add_knowledge_source(default_url)

    def add_knowledge_source(self, url: str) -> Dict[str, Any]:
        """
        Adds a URL to the knowledge base.
        """
        if not url:
            return {"success": False, "error": "URL cannot be empty."}
        
        if url in self.urls_loaded:
            return {"success": True, "message": f"URL '{url}' already loaded."}

        logger.info(f"Adding knowledge source: {url}")
        try:
            self.knowledge.add_content(url=url)
            self.urls_loaded.add(url)
            logger.info(f"Successfully added URL '{url}' to knowledge base.")
            return {"success": True, "message": f"Added URL '{url}'."}
        except Exception as e:
            logger.error(f"Error adding URL '{url}': {str(e)}")
            return {"success": False, "error": str(e)}

    def answer_question(self, query: str) -> Dict[str, Any]:
        """
        Asks a question to the RAG agent and returns the answer with reasoning.
        """
        if not query:
            return {"success": False, "error": "Query cannot be empty."}
        
        logger.info(f"Answering question: '{query[:50]}'...")
        
        reasoning_text = ""
        answer_text = ""
        citations = []

        try:
            # The agent.run method in agno is synchronous.
            # It can be wrapped in asyncio.to_thread if an async API is needed.
            
            # For streaming, agno's .run() can take a stream=True parameter.
            # To get reasoning, it would depend on how agno exposes it in non-Streamlit context.
            # For simplicity, we'll run it in non-streaming mode for a single report.
            
            # If `stream_events=True` is used, the generator yields chunks with reasoning and content.
            # For a service, we'd want to capture these and return them.
            
            full_response = ""
            for chunk in self.agent.run(query, stream=True, stream_events=True):
                if hasattr(chunk, 'reasoning_content') and chunk.reasoning_content:
                    reasoning_text = chunk.reasoning_content
                if hasattr(chunk, 'content') and chunk.content and isinstance(chunk.content, str):
                    full_response += chunk.content
                if hasattr(chunk, 'citations') and chunk.citations:
                    if hasattr(chunk.citations, 'urls') and chunk.citations.urls:
                        citations = [{"url": c.url, "title": c.title} for c in chunk.citations.urls]
            
            answer_text = full_response # The full content is the answer

            logger.info(f"Successfully answered question: '{query[:50]}'...")
            return {
                "success": True,
                "reasoning": reasoning_text,
                "answer": answer_text,
                "citations": citations
            }

        except Exception as e:
            logger.error(f"An error occurred while answering the question: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

# Example of how to use the service
if __name__ == '__main__':
    load_dotenv()

    google_key = os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not google_key or not openai_key:
        print("Please set GOOGLE_API_KEY and OPENAI_API_KEY in your .env file.")
    else:
        service = RagReasoningService(google_api_key=google_key, openai_api_key=openai_key)
        
        # Example 1: Add a new knowledge source
        # print("--- Adding a new knowledge source ---")
        # new_url = "https://example.com/some-new-article"
        # add_result = service.add_knowledge_source(new_url)
        # print(add_result)
        
        # Example 2: Ask a question
        print("\n--- Asking a question ---")
        question = "What is the primary difference between MCP and A2A protocols, according to the documents?"
        answer_result = service.answer_question(question)
        
        if answer_result["success"]:
            print("\n--- REASONING ---")
            print(answer_result["reasoning"])
            print("\n--- ANSWER ---")
            print(answer_result["answer"])
            print("\n--- CITATIONS ---")
            for cite in answer_result["citations"]:
                print(f"- [{cite['title']}]({cite['url']})")
        else:
            print(f"\n--- ERROR ---")
            print(answer_result["error"])
