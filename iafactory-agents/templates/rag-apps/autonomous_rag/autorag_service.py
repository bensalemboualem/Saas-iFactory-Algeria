# autorag_service.py

import logging
from io import BytesIO
from typing import Dict, Any, List, Optional
import os

from agno.agent import Agent
from agno.document.reader.pdf_reader import PDFReader
from agno.models.openai import OpenAIChat
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.embedder.openai import OpenAIEmbedder
from agno.vectordb.pgvector import PgVector, SearchType
from agno.storage.agent.postgres import PostgresAgentStorage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutoRagService:
    """
    A service for Autonomous RAG using GPT-4o and PgVector,
    decoupled from any specific UI.
    """
    
    def __init__(self, openai_api_key: str, db_url: str):
        if not openai_api_key or not db_url:
            raise ValueError("OpenAI API key and Database URL are required.")
        
        self.openai_api_key = openai_api_key
        self.db_url = db_url
        self._assistant = self._setup_assistant()
        logger.info("AutoRagService initialized.")

    def _setup_assistant(self) -> Agent:
        """Initializes and returns an AI Assistant agent."""
        llm = OpenAIChat(id="gpt-4o-mini", api_key=self.openai_api_key)
        
        return Agent(
            id="auto_rag_agent",
            model=llm,
            storage=PostgresAgentStorage(table_name="auto_rag_storage", db_url=self.db_url),  
            knowledge_base=PDFUrlKnowledgeBase(
                vector_db=PgVector(
                    db_url=self.db_url,  
                    collection="auto_rag_docs",  
                    embedder=OpenAIEmbedder(id="text-embedding-ada-002", dimensions=1536, api_key=self.openai_api_key),  
                ),
                num_documents=3,  
            ),
            tools=[DuckDuckGoTools()],
            instructions=[
                "Search your knowledge base first.",  
                "If not found, search the internet.",  
                "Provide clear and concise answers.",  
            ],
            show_tool_calls=True,  
            search_knowledge=True,  
            markdown=True,  
            debug_mode=False, # Set to False for service
        )

    def add_pdf_document(self, file_content: bytes, file_name: str) -> Dict[str, Any]:
        """
        Adds a PDF document to the agent's knowledge base.
        """
        logger.info(f"Attempting to add PDF document: {file_name}")
        try:
            reader = PDFReader()
            docs = reader.read(BytesIO(file_content))
            if docs:
                self._assistant.knowledge_base.load_documents(docs, upsert=True)
                logger.info(f"Successfully added document '{file_name}' to knowledge base.")
                return {"success": True, "message": f"Document '{file_name}' added to knowledge base."}
            else:
                logger.error(f"Failed to read document '{file_name}'.")
                return {"success": False, "error": f"Failed to read document '{file_name}'."}
        except Exception as e:
            logger.error(f"Error adding PDF '{file_name}': {str(e)}")
            return {"success": False, "error": str(e)}

    def query_assistant(self, question: str) -> Dict[str, Any]:
        """
        Queries the RAG assistant and returns a response.
        """
        if not question:
            return {"success": False, "error": "Question cannot be empty."}
        
        logger.info(f"Querying assistant with: '{question[:50]}...'")
        try:
            # The agent.run method in agno is synchronous
            response = self._assistant.run(question)
            
            if response and response.content:
                logger.info("Assistant successfully generated a response.")
                return {
                    "success": True,
                    "answer": response.content,
                    # Add citations if available
                    "citations": [{"url": c.url, "title": c.title} for c in response.citations.urls] if hasattr(response, 'citations') and response.citations and response.citations.urls else []
                }
            else:
                logger.error("Assistant did not produce any content.")
                return {
                    "success": False,
                    "error": "Assistant did not produce any content."
                }
        except Exception as e:
            logger.error(f"An error occurred while querying the assistant: {str(e)}")
            return {"success": False, "error": str(e)}

# Example of how to use the service
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    openai_key = os.getenv("OPENAI_API_KEY")
    # For local testing, ensure a PgVector DB is running at this URL
    db_url = os.getenv("DB_URL", "postgresql+psycopg://ai:ai@localhost:5532/ai")

    if not openai_key:
        print("Please set OPENAI_API_KEY in your .env file.")
    else:
        service = AutoRagService(openai_api_key=openai_key, db_url=db_url)
        
        # --- Example: Querying the assistant ---
        question = "What is Agno?"
        print(f"--- Asking: {question} ---")
        answer_result = service.query_assistant(question)
        
        if answer_result["success"]:
            print("\n--- ANSWER ---")
            print(answer_result["answer"])
            if answer_result["citations"]:
                print("\n--- CITATIONS ---")
                for cite in answer_result["citations"]:
                    print(f"- [{cite['title']}]({cite['url']})")
        else:
            print(f"\n--- ERROR ---")
            print(answer_result["error"])
