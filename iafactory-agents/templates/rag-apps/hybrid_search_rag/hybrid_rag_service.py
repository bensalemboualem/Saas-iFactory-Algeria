# hybrid_rag_service.py

import os
import logging
import warnings
from typing import Dict, Any, List, Optional
from pathlib import Path
import anthropic
from io import BytesIO

from raglite import RAGLiteConfig, insert_document, hybrid_search, retrieve_chunks, rerank_chunks, rag
from rerankers import Reranker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore", message=".*torch.classes.*") # Ignore PyTorch warnings


RAG_SYSTEM_PROMPT = """
You are a friendly and knowledgeable assistant that provides complete and insightful answers.
Answer the user's question using only the context below.
When responding, you MUST NOT reference the existence of the context, directly or indirectly.
Instead, you MUST treat the context as if its contents are entirely part of your working memory.
""".strip()


class HybridRagService:
    """
    A service for Hybrid Search RAG using RAGLite, Claude, OpenAI embeddings, and Cohere reranker,
    decoupled from any specific UI.
    """
    
    def __init__(self, openai_key: str, anthropic_key: str, cohere_key: str, db_url: str):
        if not all([openai_key, anthropic_key, cohere_key, db_url]):
            raise ValueError("All API keys (OpenAI, Anthropic, Cohere) and Database URL are required.")
        
        # Set API keys as environment variables
        os.environ["OPENAI_API_KEY"] = openai_key
        os.environ["ANTHROPIC_API_KEY"] = anthropic_key
        os.environ["COHERE_API_KEY"] = cohere_key
        
        self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
        
        try:
            self.rag_config = RAGLiteConfig(
                db_url=db_url,
                llm="claude-3-opus-20240229", # Specified in README
                embedder="text-embedding-3-large", # Specified in README
                embedder_normalize=True,
                chunk_max_size=2000,
                embedder_sentence_window_size=2,
                reranker=Reranker("cohere", api_key=cohere_key, lang="en")
            )
            logger.info("HybridRagService initialized with RAGLiteConfig.")
        except Exception as e:
            logger.error(f"Error initializing RAGLiteConfig: {str(e)}")
            raise ValueError(f"Failed to initialize RAGLiteConfig: {str(e)}")

    def add_pdf_document(self, file_content: bytes, file_name: str) -> Dict[str, Any]:
        """
        Adds a PDF document to the RAG knowledge base.
        """
        logger.info(f"Attempting to add PDF document: {file_name}")
        try:
            # RAGLite's insert_document expects a file path
            # Need to save the BytesIO content to a temporary file
            temp_dir = Path("tmp_docs")
            temp_dir.mkdir(exist_ok=True)
            temp_file_path = temp_dir / file_name
            
            with open(temp_file_path, "wb") as f:
                f.write(file_content)
            
            insert_document(temp_file_path, config=self.rag_config)
            
            os.remove(temp_file_path) # Clean up temporary file
            
            logger.info(f"Successfully added document '{file_name}' to knowledge base.")
            return {"success": True, "message": f"Document '{file_name}' added to knowledge base."}
        except Exception as e:
            logger.error(f"Error adding PDF '{file_name}': {str(e)}")
            return {"success": False, "error": str(e)}

    def add_url_to_knowledge_base(self, url: str) -> Dict[str, Any]:
        """
        Adds a URL's content to the RAG knowledge base.
        """
        logger.info(f"Attempting to add URL: {url}")
        try:
            # RAGLite's insert_document can handle URLs directly
            insert_document(url, config=self.rag_config)
            logger.info(f"Successfully added URL '{url}' to knowledge base.")
            return {"success": True, "message": f"URL '{url}' added to knowledge base."}
        except Exception as e:
            logger.error(f"Error adding URL '{url}': {str(e)}")
            return {"success": False, "error": str(e)}

    def answer_question(self, query: str) -> Dict[str, Any]:
        """
        Answers a question using the hybrid search RAG system.
        """
        if not query:
            return {"success": False, "error": "Query cannot be empty."}
        
        logger.info(f"Querying RAG system with: '{query[:50]}'...")
        
        try:
            # Perform hybrid search and rerank
            reranked_chunks = self._perform_hybrid_search(query)
            
            if not reranked_chunks or len(reranked_chunks) == 0:
                logger.info("No relevant documents found. Falling back to Claude.")
                full_response = self._handle_fallback(query)
                citations = []
            else:
                # Use RAGLite's rag function for generation
                # We need to adapt the message history if any
                # For a service, we'll assume a fresh query for now or manage history externally
                
                # RAGLite's rag function typically takes a list of messages.
                # Since we don't have a chat history stored in the service itself,
                # we pass just the current query.
                response_stream = rag(
                    prompt=query, 
                    system_prompt=RAG_SYSTEM_PROMPT,
                    search=self._perform_hybrid_search, # Pass the search function
                    messages=[], # No history for a stateless call
                    max_contexts=5, 
                    config=self.rag_config
                )
                
                full_response = ""
                citations = []
                # RAGLite's rag function returns a generator that yields chunks
                # The last chunk in the response might contain citations
                for chunk in response_stream:
                    full_response += chunk
                    # Check for citations in the final chunk if available
                    if isinstance(chunk, dict) and 'citations' in chunk:
                        citations = chunk['citations'] # RAGLite returns citations directly

                # Need to parse citations if they are embedded in the text
                # For simplicity, we assume RAGLite directly provides structured citations
                # if response_stream was a generator for structured outputs.
                # If not, a post-processing step would be needed.
            
            return {
                "success": True,
                "answer": full_response,
                "citations": citations
            }
        except Exception as e:
            logger.error(f"An error occurred while answering the question: {str(e)}")
            return {"success": False, "error": str(e)}

    def _perform_hybrid_search(self, query: str) -> List[dict]:
        """Internal helper to conduct hybrid search and rerank."""
        try:
            chunk_ids, scores = hybrid_search(query, num_results=10, config=self.rag_config)
            if not chunk_ids:
                return []
            chunks = retrieve_chunks(chunk_ids, config=self.rag_config)
            return rerank_chunks(query, chunks, config=self.rag_config)
        except Exception as e:
            logger.error(f"Hybrid search error: {str(e)}")
            return []

    def _handle_fallback(self, query: str) -> str:
        """Internal helper to handle fallback to Claude for general knowledge questions."""
        try:
            system_prompt = """You are a helpful AI assistant. When you don't know something, 
            be honest about it. Provide clear, concise, and accurate responses. If the question 
            is not related to any specific document, use your general knowledge to answer."""
            
            message = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229", # Using sonnet for fallback, as opus is for main RAG
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": query}],
                temperature=0.7
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Fallback LLM error: {str(e)}")
            return "I apologize, but I encountered an error while processing your request with general knowledge. Please try again."


# Example of how to use the service
if __name__ == '__main__':
    load_dotenv()

    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    cohere_key = os.getenv("COHERE_API_KEY")
    # For local testing, ensure a PostgreSQL DB is running at this URL
    db_url = os.getenv("DB_URL", "postgresql://user:password@localhost:5432/dbname")

    if not all([openai_key, anthropic_key, cohere_key, db_url]):
        print("Please set OPENAI_API_KEY, ANTHROPIC_API_KEY, COHERE_API_KEY, and DB_URL in your .env file.")
    else:
        service = HybridRagService(
            openai_key=openai_key,
            anthropic_key=anthropic_key,
            cohere_key=cohere_key,
            db_url=db_url
        )
        
        # --- Example: Add a PDF document ---
        # print("--- Adding a PDF document ---")
        # try:
        #     with open("sample.pdf", "rb") as f:
        #         pdf_content = f.read()
        #     add_result = service.add_pdf_document(pdf_content, "sample.pdf")
        #     print(add_result)
        # except FileNotFoundError:
        #     print("sample.pdf not found. Please create one for testing.")
        
        # --- Example: Add a URL ---
        print("\n--- Adding a URL ---")
        url_to_add = "https://www.example.com/some-article-on-rag"
        add_url_result = service.add_url_to_knowledge_base(url_to_add)
        print(add_url_result)

        # --- Example: Ask a question ---
        print("\n--- Asking a question ---")
        question = "What is hybrid search RAG?"
        answer_result = service.answer_question(question)
        
        if answer_result["success"]:
            print("\n--- ANSWER ---")
            print(answer_result["answer"])
            if answer_result["citations"]:
                print("\n--- CITATIONS ---")
                for cite in answer_result["citations"]:
                    print(f"- [{cite.get('title', cite['url'])}]({cite['url']})")
        else:
            print(f"\n--- ERROR ---")
            print(answer_result["error"])
