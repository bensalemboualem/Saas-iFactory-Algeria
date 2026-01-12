"""
Notebook LM Service - Interrogation de documents avec IA
Extraction de texte et RAG pour répondre aux questions
"""

import os
import uuid
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime
import anthropic
import openai

# Text extraction
import PyPDF2
from docx import Document
import pandas as pd

# Vector store
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings

class NotebookLMService:
    """Service pour interroger des documents avec IA (RAG)"""

    def __init__(self, upload_dir: str = "./uploads"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

        # API keys
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")

        # Vector store
        self.vector_stores = {}  # file_id -> FAISS

        # Embeddings
        if self.openai_key:
            self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_key)
        else:
            # Fallback: local embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
            )

        # Text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

    async def upload_document(
        self,
        file_path: str,
        filename: str,
        file_type: str
    ) -> Dict[str, Any]:
        """
        Upload et indexe un document

        Args:
            file_path: Chemin du fichier uploadé
            filename: Nom du fichier
            file_type: Type MIME du fichier

        Returns:
            Métadonnées du fichier indexé
        """

        file_id = str(uuid.uuid4())

        # Extract text
        text = await self._extract_text(file_path, file_type)

        if not text or len(text.strip()) < 10:
            raise ValueError("Aucun texte extractible du fichier")

        # Split into chunks
        chunks = self.text_splitter.split_text(text)

        # Create vector store
        texts_with_metadata = []
        for i, chunk in enumerate(chunks):
            texts_with_metadata.append({
                "text": chunk,
                "metadata": {
                    "file_id": file_id,
                    "filename": filename,
                    "chunk_id": i,
                    "total_chunks": len(chunks)
                }
            })

        # Create FAISS index
        vector_store = FAISS.from_texts(
            texts=[t["text"] for t in texts_with_metadata],
            embedding=self.embeddings,
            metadatas=[t["metadata"] for t in texts_with_metadata]
        )

        self.vector_stores[file_id] = vector_store

        return {
            "file_id": file_id,
            "filename": filename,
            "chunks": len(chunks),
            "total_chars": len(text),
            "indexed_at": datetime.now().isoformat()
        }

    async def query_documents(
        self,
        question: str,
        file_ids: List[str],
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Interroge les documents avec une question

        Args:
            question: Question de l'utilisateur
            file_ids: IDs des fichiers à interroger
            top_k: Nombre de chunks à récupérer

        Returns:
            Réponse avec sources
        """

        if not file_ids:
            raise ValueError("Aucun document sélectionné")

        # Retrieve relevant chunks from all files
        all_chunks = []
        for file_id in file_ids:
            if file_id not in self.vector_stores:
                continue

            vector_store = self.vector_stores[file_id]
            docs = vector_store.similarity_search(question, k=top_k)

            for doc in docs:
                all_chunks.append({
                    "text": doc.page_content,
                    "metadata": doc.metadata
                })

        if not all_chunks:
            return {
                "answer": "Aucun contexte pertinent trouvé dans les documents.",
                "sources": []
            }

        # Generate answer with AI
        answer = await self._generate_answer(question, all_chunks)

        # Extract sources
        sources = []
        seen_files = set()
        for chunk in all_chunks[:3]:  # Top 3 sources
            file_id = chunk["metadata"].get("file_id")
            if file_id not in seen_files:
                sources.append({
                    "filename": chunk["metadata"].get("filename"),
                    "chunk": chunk["metadata"].get("chunk_id"),
                    "file_id": file_id
                })
                seen_files.add(file_id)

        return {
            "answer": answer,
            "sources": sources,
            "context_used": len(all_chunks)
        }

    async def _extract_text(self, file_path: str, file_type: str) -> str:
        """Extrait le texte d'un fichier"""

        try:
            # PDF
            if file_type == "application/pdf" or file_path.endswith('.pdf'):
                return self._extract_pdf(file_path)

            # DOCX
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or file_path.endswith('.docx'):
                return self._extract_docx(file_path)

            # TXT/MD
            elif file_type in ["text/plain", "text/markdown"] or file_path.endswith(('.txt', '.md')):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()

            # CSV
            elif file_type == "text/csv" or file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                return df.to_string()

            # XLSX
            elif file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
                return df.to_string()

            else:
                raise ValueError(f"Type de fichier non supporté: {file_type}")

        except Exception as e:
            raise ValueError(f"Erreur extraction texte: {str(e)}")

    def _extract_pdf(self, file_path: str) -> str:
        """Extrait texte d'un PDF"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n\n"
        return text

    def _extract_docx(self, file_path: str) -> str:
        """Extrait texte d'un DOCX"""
        doc = Document(file_path)
        text = "\n\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text

    async def _generate_answer(
        self,
        question: str,
        chunks: List[Dict[str, Any]]
    ) -> str:
        """Génère une réponse avec l'IA"""

        # Build context from chunks
        context = "\n\n".join([
            f"[Document: {chunk['metadata']['filename']}, Chunk {chunk['metadata']['chunk_id']}]\n{chunk['text']}"
            for chunk in chunks
        ])

        prompt = f"""Tu es un assistant IA spécialisé dans l'analyse de documents.

CONTEXTE EXTRAIT DES DOCUMENTS:
{context}

QUESTION:
{question}

INSTRUCTIONS:
- Réponds à la question en te basant UNIQUEMENT sur le contexte fourni
- Si l'information n'est pas dans le contexte, dis-le clairement
- Cite les sources (nom du fichier) dans ta réponse
- Sois précis et concis
- Réponds en français

RÉPONSE:"""

        try:
            if self.anthropic_key:
                return await self._generate_with_claude(prompt)
            elif self.openai_key:
                return await self._generate_with_gpt(prompt)
            else:
                # Fallback: simple extraction
                return self._fallback_answer(question, chunks)

        except Exception as e:
            return f"Erreur génération réponse: {str(e)}"

    async def _generate_with_claude(self, prompt: str) -> str:
        """Génère avec Claude"""
        client = anthropic.Anthropic(api_key=self.anthropic_key)

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    async def _generate_with_gpt(self, prompt: str) -> str:
        """Génère avec GPT"""
        client = openai.OpenAI(api_key=self.openai_key)

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "Tu es un assistant IA spécialisé dans l'analyse de documents."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )

        return response.choices[0].message.content

    def _fallback_answer(self, question: str, chunks: List[Dict[str, Any]]) -> str:
        """Réponse basique sans IA"""
        return f"Voici les extraits pertinents trouvés:\n\n" + "\n\n---\n\n".join([
            f"Source: {chunk['metadata']['filename']}\n{chunk['text'][:500]}..."
            for chunk in chunks[:2]
        ])

# Export service instance
notebook_lm_service = NotebookLMService()
