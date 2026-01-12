"""
IA Factory - Legal Document Chunker
Chunking structurel pour documents juridiques (Algerie/Suisse)
"""

import re
import os
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from uuid import uuid4
import httpx
from dotenv import load_dotenv

load_dotenv()

@dataclass
class LegalChunk:
    """Represente un chunk de document juridique"""
    id: str
    content: str
    content_with_context: str
    context_prefix: str
    hierarchy_path: List[str]
    article_number: Optional[str]
    chunk_index: int
    char_start: int
    char_end: int
    metadata: Dict

class LegalDocumentParser:
    """Parser pour documents juridiques structures"""

    # Patterns pour detecter la structure juridique
    PATTERNS = {
        'livre': r'^(LIVRE|Livre)\s+([IVXLCDM]+|\d+)',
        'titre': r'^(TITRE|Titre)\s+([IVXLCDM]+|\d+)',
        'chapitre': r'^(CHAPITRE|Chapitre)\s+([IVXLCDM]+|\d+)',
        'section': r'^(SECTION|Section)\s+(\d+)',
        'article': r'^(Art\.?|Article)\s*(\d+[\-\w]*)',
        'alinea': r'^(\d+[\.\)°]|\-)\s+',
    }

    def __init__(self, source_code: str, source_title: str, jurisdiction: str = "DZ"):
        self.source_code = source_code
        self.source_title = source_title
        self.jurisdiction = jurisdiction
        self.current_hierarchy = []

    def parse_document(self, text: str) -> List[Dict]:
        """Parse un document juridique et extrait la structure"""
        documents = []
        lines = text.split('\n')

        current_article = None
        current_content = []

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # Detecter les niveaux hierarchiques
            hierarchy_match = self._detect_hierarchy(line)
            if hierarchy_match:
                level, number, title = hierarchy_match
                self._update_hierarchy(level, f"{level} {number}")
                continue

            # Detecter un nouvel article
            article_match = re.match(self.PATTERNS['article'], line, re.IGNORECASE)
            if article_match:
                # Sauvegarder l'article precedent
                if current_article and current_content:
                    documents.append(self._create_document(
                        current_article,
                        '\n'.join(current_content)
                    ))

                current_article = article_match.group(2)
                # Le reste de la ligne apres le numero d'article
                rest = line[article_match.end():].strip()
                current_content = [rest] if rest else []
            else:
                # Continuer l'article courant
                if current_article:
                    current_content.append(line)

        # Dernier article
        if current_article and current_content:
            documents.append(self._create_document(
                current_article,
                '\n'.join(current_content)
            ))

        return documents

    def _detect_hierarchy(self, line: str) -> Optional[Tuple[str, str, str]]:
        """Detecte le niveau hierarchique d'une ligne"""
        for level in ['livre', 'titre', 'chapitre', 'section']:
            match = re.match(self.PATTERNS[level], line, re.IGNORECASE)
            if match:
                return (level.upper(), match.group(2), line)
        return None

    def _update_hierarchy(self, level: str, value: str):
        """Met a jour la hierarchie courante"""
        level_order = ['LIVRE', 'TITRE', 'CHAPITRE', 'SECTION']
        level_idx = level_order.index(level) if level in level_order else -1

        if level_idx >= 0:
            self.current_hierarchy = self.current_hierarchy[:level_idx]
            self.current_hierarchy.append(value)

    def _create_document(self, article_number: str, content: str) -> Dict:
        """Cree un document structure"""
        return {
            'article_number': f"Art. {article_number}",
            'content': content.strip(),
            'hierarchy_path': self.current_hierarchy.copy(),
            'hierarchy_level': 5,  # Article level
            'word_count': len(content.split()),
        }


class LegalChunker:
    """Chunker semantique pour documents juridiques"""

    def __init__(
        self,
        source_code: str,
        source_title: str,
        jurisdiction: str = "DZ",
        max_chunk_size: int = 1000,
        overlap: int = 100
    ):
        self.source_code = source_code
        self.source_title = source_title
        self.jurisdiction = jurisdiction
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap

    def chunk_article(self, article: Dict) -> List[LegalChunk]:
        """Decoupe un article en chunks avec contexte"""
        chunks = []
        content = article['content']
        article_number = article['article_number']
        hierarchy_path = article.get('hierarchy_path', [])

        # Contexte prefix pour chaque chunk
        hierarchy_str = ' > '.join(hierarchy_path) if hierarchy_path else ''
        context_prefix = f"[{self.source_title} - {article_number}]"
        if hierarchy_str:
            context_prefix = f"[{self.source_title} - {hierarchy_str} - {article_number}]"

        # Si l'article est assez court, un seul chunk
        if len(content) <= self.max_chunk_size:
            chunks.append(LegalChunk(
                id=str(uuid4()),
                content=content,
                content_with_context=f"{context_prefix}\n{content}",
                context_prefix=context_prefix,
                hierarchy_path=hierarchy_path,
                article_number=article_number,
                chunk_index=0,
                char_start=0,
                char_end=len(content),
                metadata={
                    'source_code': self.source_code,
                    'jurisdiction': self.jurisdiction,
                    'word_count': len(content.split())
                }
            ))
            return chunks

        # Decoupage par alineas ou phrases
        segments = self._split_by_structure(content)

        current_chunk = ""
        chunk_start = 0
        chunk_index = 0

        for segment in segments:
            if len(current_chunk) + len(segment) <= self.max_chunk_size:
                current_chunk += segment
            else:
                # Sauvegarder le chunk courant
                if current_chunk.strip():
                    chunks.append(LegalChunk(
                        id=str(uuid4()),
                        content=current_chunk.strip(),
                        content_with_context=f"{context_prefix}\n{current_chunk.strip()}",
                        context_prefix=context_prefix,
                        hierarchy_path=hierarchy_path,
                        article_number=article_number,
                        chunk_index=chunk_index,
                        char_start=chunk_start,
                        char_end=chunk_start + len(current_chunk),
                        metadata={
                            'source_code': self.source_code,
                            'jurisdiction': self.jurisdiction,
                            'word_count': len(current_chunk.split())
                        }
                    ))
                    chunk_index += 1
                    chunk_start += len(current_chunk)

                current_chunk = segment

        # Dernier chunk
        if current_chunk.strip():
            chunks.append(LegalChunk(
                id=str(uuid4()),
                content=current_chunk.strip(),
                content_with_context=f"{context_prefix}\n{current_chunk.strip()}",
                context_prefix=context_prefix,
                hierarchy_path=hierarchy_path,
                article_number=article_number,
                chunk_index=chunk_index,
                char_start=chunk_start,
                char_end=chunk_start + len(current_chunk),
                metadata={
                    'source_code': self.source_code,
                    'jurisdiction': self.jurisdiction,
                    'word_count': len(current_chunk.split())
                }
            ))

        return chunks

    def _split_by_structure(self, content: str) -> List[str]:
        """Decoupe par structure (alineas, phrases)"""
        # D'abord par alineas (numeros, tirets)
        alinea_pattern = r'(?=\n\s*(?:\d+[\.\)°]|\-)\s+)'
        segments = re.split(alinea_pattern, content)

        # Si pas d'alineas, decouper par phrases
        if len(segments) <= 1:
            # Decoupage par phrases (. suivi de majuscule ou fin)
            segments = re.split(r'(?<=[.!?])\s+(?=[A-Z])', content)

        return segments


class EmbeddingGenerator:
    """Genere les embeddings via OpenAI ou autre provider"""

    def __init__(self, provider: str = "openai"):
        self.provider = provider
        self.api_key = os.getenv("OPENAI_API_KEY")

    async def generate(self, texts: List[str]) -> List[List[float]]:
        """Genere les embeddings pour une liste de textes"""
        if self.provider == "openai":
            return await self._openai_embed(texts)
        else:
            raise ValueError(f"Provider {self.provider} non supporte")

    async def _openai_embed(self, texts: List[str]) -> List[List[float]]:
        """Embeddings via OpenAI API"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/embeddings",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "text-embedding-3-small",
                    "input": texts
                },
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            return [item["embedding"] for item in data["data"]]


class LegalRAGIndexer:
    """Indexe les documents juridiques dans Supabase"""

    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.embedder = EmbeddingGenerator()

    async def index_document(
        self,
        text: str,
        source_code: str,
        source_title: str,
        jurisdiction: str = "DZ",
        legal_type: str = "code"
    ):
        """Indexe un document juridique complet"""
        # 1. Parser le document
        parser = LegalDocumentParser(source_code, source_title, jurisdiction)
        articles = parser.parse_document(text)

        print(f"Trouve {len(articles)} articles")

        # 2. Creer la source
        source_id = await self._create_source(
            source_code, source_title, jurisdiction, legal_type
        )

        # 3. Chunker et indexer chaque article
        chunker = LegalChunker(source_code, source_title, jurisdiction)

        all_chunks = []
        for article in articles:
            # Creer le document
            doc_id = await self._create_document(source_id, article)

            # Chunker
            chunks = chunker.chunk_article(article)
            for chunk in chunks:
                chunk.metadata['document_id'] = doc_id
                chunk.metadata['source_id'] = source_id
            all_chunks.extend(chunks)

        print(f"Genere {len(all_chunks)} chunks")

        # 4. Generer les embeddings par batch
        batch_size = 100
        for i in range(0, len(all_chunks), batch_size):
            batch = all_chunks[i:i+batch_size]
            texts = [c.content_with_context for c in batch]
            embeddings = await self.embedder.generate(texts)

            # Inserer les chunks
            for chunk, embedding in zip(batch, embeddings):
                await self._insert_chunk(chunk, embedding)

            print(f"Indexe {min(i+batch_size, len(all_chunks))}/{len(all_chunks)} chunks")

        print(f"Indexation terminee: {source_title}")
        return source_id

    async def _create_source(
        self, code: str, title: str, jurisdiction: str, legal_type: str
    ) -> str:
        """Cree une source juridique"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.supabase_url}/rest/v1/legal_sources",
                headers={
                    "apikey": self.supabase_key,
                    "Authorization": f"Bearer {self.supabase_key}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation"
                },
                json={
                    "code": code,
                    "title": title,
                    "jurisdiction": jurisdiction,
                    "legal_type": legal_type,
                    "language": "fr"
                }
            )
            response.raise_for_status()
            return response.json()[0]["id"]

    async def _create_document(self, source_id: str, article: Dict) -> str:
        """Cree un document (article)"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.supabase_url}/rest/v1/legal_documents",
                headers={
                    "apikey": self.supabase_key,
                    "Authorization": f"Bearer {self.supabase_key}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation"
                },
                json={
                    "source_id": source_id,
                    "article_number": article["article_number"],
                    "content": article["content"],
                    "hierarchy_path": article.get("hierarchy_path", []),
                    "hierarchy_level": article.get("hierarchy_level", 5),
                    "word_count": article.get("word_count", 0)
                }
            )
            response.raise_for_status()
            return response.json()[0]["id"]

    async def _insert_chunk(self, chunk: LegalChunk, embedding: List[float]):
        """Insere un chunk vectorise"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.supabase_url}/rest/v1/document_chunks",
                headers={
                    "apikey": self.supabase_key,
                    "Authorization": f"Bearer {self.supabase_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "document_id": chunk.metadata["document_id"],
                    "source_id": chunk.metadata["source_id"],
                    "content": chunk.content,
                    "content_with_context": chunk.content_with_context,
                    "context_prefix": chunk.context_prefix,
                    "embedding": embedding,
                    "chunk_index": chunk.chunk_index,
                    "char_start": chunk.char_start,
                    "char_end": chunk.char_end,
                    "metadata": chunk.metadata
                }
            )
            response.raise_for_status()


# Exemple d'utilisation
if __name__ == "__main__":
    import asyncio

    # Exemple de document juridique
    sample_text = """
    LIVRE I - DES PERSONNES

    TITRE I - DES PERSONNES PHYSIQUES

    CHAPITRE 1 - DE LA PERSONNALITE

    Article 25
    La personnalite commence avec la naissance accomplie de l'enfant vivant et finit par la mort.

    Article 26
    Toute personne doit avoir un nom et un ou plusieurs prenoms.
    Le nom d'un homme s'etend a ses enfants.

    Article 27
    L'enfant a droit a une filiation maternelle et paternelle.
    1) La filiation maternelle resulte de l'accouchement.
    2) La filiation paternelle resulte du mariage.
    """

    async def main():
        indexer = LegalRAGIndexer(
            supabase_url=os.getenv("SUPABASE_URL"),
            supabase_key=os.getenv("SUPABASE_KEY")
        )

        await indexer.index_document(
            text=sample_text,
            source_code="CODE_CIVIL_DZ",
            source_title="Code Civil Algerien",
            jurisdiction="DZ",
            legal_type="code"
        )

    asyncio.run(main())
