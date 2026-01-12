# rag_as_a_service_service.py

import logging
import requests
from anthropic import Anthropic
from typing import List, Dict, Optional
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RagAsAService:
    """
    A service to perform RAG using Ragie.ai and Anthropic's Claude,
    decoupled from any specific UI.
    """
    def __init__(self, ragie_api_key: str, anthropic_api_key: str):
        """
        Initialize the RAG pipeline with API keys.
        """
        if not ragie_api_key or not anthropic_api_key:
            raise ValueError("Ragie and Anthropic API keys are required.")
            
        self.ragie_api_key = ragie_api_key
        self.anthropic_api_key = anthropic_api_key
        self.anthropic_client = Anthropic(api_key=anthropic_api_key)
        
        # API endpoints
        self.RAGIE_UPLOAD_URL = "https://api.ragie.ai/documents/url"
        self.RAGIE_RETRIEVAL_URL = "https://api.ragie.ai/retrievals"
        logger.info("RagAsAService initialized.")

    def upload_document(self, url: str, name: Optional[str] = None, mode: str = "fast") -> Dict:
        """
        Upload a document to Ragie from a URL.
        """
        if not name:
            name = urlparse(url).path.split('/')[-1] or "document"
            
        payload = {
            "mode": mode,
            "name": name,
            "url": url
        }
        
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.ragie_api_key}"
        }
        
        logger.info(f"Uploading document to Ragie: {url} (mode: {mode})")
        response = requests.post(self.RAGIE_UPLOAD_URL, json=payload, headers=headers)
        
        if not response.ok:
            logger.error(f"Document upload failed: {response.status_code} {response.reason} - {response.text}")
            return {"success": False, "error": f"Document upload failed: {response.status_code} {response.reason} - {response.text}"}
            
        return {"success": True, "data": response.json()}
    
    def _retrieve_chunks(self, query: str, scope: str = "tutorial") -> List[str]:
        """
        Retrieve relevant chunks from Ragie for a given query.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.ragie_api_key}"
        }
        
        payload = {
            "query": query,
            "filters": {
                "scope": scope
            }
        }
        
        logger.info(f"Retrieving chunks from Ragie for query: {query}")
        response = requests.post(
            self.RAGIE_RETRIEVAL_URL,
            headers=headers,
            json=payload
        )
        
        if not response.ok:
            logger.error(f"Retrieval failed: {response.status_code} {response.reason} - {response.text}")
            raise Exception(f"Retrieval failed: {response.status_code} {response.reason}")
            
        data = response.json()
        return [chunk["text"] for chunk in data["scored_chunks"]]

    def _create_system_prompt(self, chunk_texts: List[str]) -> str:
        """
        Create the system prompt with the retrieved chunks.
        """
        return f"""These are very important to follow: You are "Ragie AI", a professional but friendly AI chatbot working as an assistant to the user. Your current task is to help the user based on all of the information available to you shown below. Answer informally, directly, and concisely without a heading or greeting but include everything relevant. Use richtext Markdown when appropriate including bold, italic, paragraphs, and lists when helpful. If using LaTeX, use double $$ as delimiter instead of single $. Use $$...$$ instead of parentheses. Organize information into multiple sections or points when appropriate. Don't include raw item IDs or other raw fields from the source. Don't use XML or other markup unless requested by the user. Here is all of the information available to answer the user: === {chunk_texts} === If the user asked for a search and there are no results, make sure to let the user know that you couldn't find anything, and what they might be able to do to find the information they need. END SYSTEM INSTRUCTIONS"""

    def _generate_response(self, system_prompt: str, query: str) -> str:
        """
        Generate response using Claude 3.5 Sonnet.
        """
        logger.info("Generating response with Claude 3.5 Sonnet...")
        message = self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20240620", # Use latest sonnet model
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": query
                }
            ]
        )
        
        return message.content[0].text

    def query_rag(self, query: str, scope: str = "tutorial") -> Dict[str, Any]:
        """
        Process a query through the complete RAG pipeline.
        """
        if not query:
            return {"success": False, "error": "Query cannot be empty."}
            
        logger.info(f"Processing RAG query: '{query[:50]}'...")
        try:
            chunks = self._retrieve_chunks(query, scope)
            
            if not chunks:
                logger.warning("No relevant information found for the query.")
                return {"success": True, "answer": "I couldn't find relevant information in the knowledge base for your query. Please try rephrasing or adding more documents.", "citations": []}
            
            system_prompt = self._create_system_prompt(chunks)
            response_text = self._generate_response(system_prompt, query)
            
            # For citations, Ragie.ai's retrieval might include source URLs in chunks
            # We would need to parse them from the original 'data' from _retrieve_chunks
            # For simplicity, returning empty citations for now, or parsing from response_text
            citations = [] # TODO: Extract citations from chunks if available
            
            return {"success": True, "answer": response_text, "citations": citations}
        except Exception as e:
            logger.error(f"Error processing RAG query: {str(e)}")
            return {"success": False, "error": str(e)}

# Example of how to use the service
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    ragie_key = os.getenv("RAGIE_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if not ragie_key or not anthropic_key:
        print("Please set RAGIE_API_KEY and ANTHROPIC_API_KEY in your .env file.")
    else:
        service = RagAsAService(ragie_api_key=ragie_key, anthropic_api_key=anthropic_key)
        
        # --- Example: Upload a document ---
        print("--- Uploading a sample document ---")
        sample_url = "https://www.theunwindai.com/p/mcp-vs-a2a-complementing-or-supplementing"
        upload_result = service.upload_document(sample_url)
        print(upload_result)
        
        # Give Ragie some time to index
        import time
        time.sleep(10) 
        
        # --- Example: Query the RAG system ---
        print("\n--- Querying the RAG system ---")
        question = "What is MCP and how does it compare to A2A protocols?"
        query_result = service.query_rag(question)
        
        if query_result["success"]:
            print("\n--- ANSWER ---")
            print(query_result["answer"])
            if query_result["citations"]:
                print("\n--- CITATIONS ---")
                for cite in query_result["citations"]:
                    print(f"- {cite}")
        else:
            print(f"\n--- ERROR ---")
            print(query_result["error"])
