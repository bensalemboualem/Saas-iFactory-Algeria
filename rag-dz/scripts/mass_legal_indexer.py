#!/usr/bin/env python3
"""
IA Factory - Mass Legal Document Indexer
Indexation automatique de multiples codes juridiques (DZ, CH, FR)
"""

import os
import re
import asyncio
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from uuid import uuid4
import httpx
from dotenv import load_dotenv

load_dotenv()

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "http://localhost:8000")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", os.getenv("SUPABASE_SERVICE_KEY", ""))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DATA_DIR = Path(__file__).parent.parent / "data" / "legal"

# Sources juridiques disponibles
LEGAL_SOURCES = {
    "DZ": {
        "CODE_CIVIL_DZ": {
            "title": "Code Civil Algerien",
            "short_title": "CC-DZ",
            "legal_type": "code",
            "file_pattern": "code_civil_dz*.txt"
        },
        "CODE_PENAL_DZ": {
            "title": "Code Penal Algerien",
            "short_title": "CP-DZ",
            "legal_type": "code",
            "file_pattern": "code_penal_dz*.txt"
        },
        "CODE_COMMERCE_DZ": {
            "title": "Code de Commerce Algerien",
            "short_title": "CCOM-DZ",
            "legal_type": "code",
            "file_pattern": "code_commerce_dz*.txt"
        },
        "CODE_TRAVAIL_DZ": {
            "title": "Code du Travail Algerien",
            "short_title": "CT-DZ",
            "legal_type": "code",
            "file_pattern": "code_travail_dz*.txt"
        },
        "CODE_FAMILLE_DZ": {
            "title": "Code de la Famille Algerien",
            "short_title": "CF-DZ",
            "legal_type": "code",
            "file_pattern": "code_famille_dz*.txt"
        }
    },
    "CH": {
        "CODE_CIVIL_CH": {
            "title": "Code Civil Suisse",
            "short_title": "CC-CH",
            "legal_type": "code",
            "file_pattern": "code_civil_ch*.txt"
        },
        "CODE_OBLIGATIONS_CH": {
            "title": "Code des Obligations Suisse",
            "short_title": "CO-CH",
            "legal_type": "code",
            "file_pattern": "code_obligations_ch*.txt"
        }
    },
    "FR": {
        "CODE_CIVIL_FR": {
            "title": "Code Civil Francais",
            "short_title": "CC-FR",
            "legal_type": "code",
            "file_pattern": "code_civil_fr*.txt"
        }
    }
}


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

    PATTERNS = {
        'livre': r'^(LIVRE|Livre)\s+([IVXLCDM]+|\d+)',
        'titre': r'^(TITRE|Titre)\s+([IVXLCDM]+|\d+)',
        'chapitre': r'^(CHAPITRE|Chapitre)\s+([IVXLCDM]+|\d+)',
        'section': r'^(SECTION|Section)\s+(\d+)',
        'article': r'^(Art\.?|Article)\s*(\d+[\-\w]*)',
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

        for line in lines:
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
                rest = line[article_match.end():].strip()
                current_content = [rest] if rest else []
            else:
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
            'hierarchy_level': 5,
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

        hierarchy_str = ' > '.join(hierarchy_path) if hierarchy_path else ''
        context_prefix = f"[{self.source_title} - {article_number}]"
        if hierarchy_str:
            context_prefix = f"[{self.source_title} - {hierarchy_str} - {article_number}]"

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

        # Decoupage par structure
        segments = self._split_by_structure(content)
        current_chunk = ""
        chunk_start = 0
        chunk_index = 0

        for segment in segments:
            if len(current_chunk) + len(segment) <= self.max_chunk_size:
                current_chunk += segment
            else:
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
        alinea_pattern = r'(?=\n\s*(?:\d+[\.°\)]|\-)\s+)'
        segments = re.split(alinea_pattern, content)

        if len(segments) <= 1:
            segments = re.split(r'(?<=[.!?])\s+(?=[A-Z])', content)

        return segments


class EmbeddingGenerator:
    """Genere les embeddings via OpenAI"""

    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model
        self.api_key = OPENAI_API_KEY

    async def generate(self, texts: List[str]) -> List[List[float]]:
        """Genere les embeddings pour une liste de textes"""
        if not self.api_key:
            print("WARNING: OPENAI_API_KEY not set, using zero embeddings")
            return [[0.0] * 1536 for _ in texts]

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/embeddings",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "input": texts
                },
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            return [item["embedding"] for item in data["data"]]


class MassLegalIndexer:
    """Indexeur de masse pour documents juridiques"""

    def __init__(self, batch_size: int = 50, use_embeddings: bool = True):
        self.batch_size = batch_size
        self.use_embeddings = use_embeddings
        self.embedder = EmbeddingGenerator() if use_embeddings else None
        self.stats = {
            "sources": 0,
            "documents": 0,
            "chunks": 0,
            "errors": []
        }

    async def index_all(self, jurisdictions: List[str] = None):
        """Indexe tous les codes juridiques disponibles"""
        print("=" * 60)
        print("IA FACTORY - MASS LEGAL INDEXER")
        print("=" * 60)

        jurisdictions = jurisdictions or list(LEGAL_SOURCES.keys())

        for jurisdiction in jurisdictions:
            if jurisdiction not in LEGAL_SOURCES:
                print(f"Jurisdiction {jurisdiction} not found, skipping...")
                continue

            print(f"\n### Processing jurisdiction: {jurisdiction}")
            sources = LEGAL_SOURCES[jurisdiction]

            for source_code, source_info in sources.items():
                await self._index_source(jurisdiction, source_code, source_info)

        print("\n" + "=" * 60)
        print("INDEXATION COMPLETE")
        print(f"Sources: {self.stats['sources']}")
        print(f"Documents: {self.stats['documents']}")
        print(f"Chunks: {self.stats['chunks']}")
        if self.stats['errors']:
            print(f"Errors: {len(self.stats['errors'])}")
            for err in self.stats['errors'][:5]:
                print(f"  - {err}")
        print("=" * 60)

    async def _index_source(self, jurisdiction: str, source_code: str, source_info: Dict):
        """Indexe une source juridique specifique"""
        print(f"\nIndexing: {source_info['title']}")

        # Chercher le fichier
        data_dir = DATA_DIR / jurisdiction.lower()
        if not data_dir.exists():
            data_dir = DATA_DIR

        files = list(data_dir.glob(source_info['file_pattern']))
        if not files:
            # Essayer le dossier parent
            files = list(DATA_DIR.parent.glob(f"*{source_code.lower()}*.txt"))
            if not files:
                print(f"  File not found: {source_info['file_pattern']}")
                self.stats['errors'].append(f"File not found: {source_info['file_pattern']}")
                return

        file_path = files[0]
        print(f"  Found file: {file_path.name}")

        try:
            text = file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            text = file_path.read_text(encoding='latin-1')

        # Parser le document
        parser = LegalDocumentParser(source_code, source_info['title'], jurisdiction)
        articles = parser.parse_document(text)
        print(f"  Found {len(articles)} articles")

        if not articles:
            print("  No articles found, skipping...")
            return

        # Creer la source dans Supabase
        source_id = await self._create_source(
            source_code,
            source_info['title'],
            source_info.get('short_title', ''),
            jurisdiction,
            source_info['legal_type']
        )

        if not source_id:
            print("  Failed to create source")
            return

        self.stats['sources'] += 1

        # Chunker et indexer
        chunker = LegalChunker(source_code, source_info['title'], jurisdiction)
        all_chunks = []

        for article in articles:
            doc_id = await self._create_document(source_id, article)
            if doc_id:
                self.stats['documents'] += 1
                chunks = chunker.chunk_article(article)
                for chunk in chunks:
                    chunk.metadata['document_id'] = doc_id
                    chunk.metadata['source_id'] = source_id
                all_chunks.extend(chunks)

        print(f"  Generated {len(all_chunks)} chunks")

        # Indexer par batch
        for i in range(0, len(all_chunks), self.batch_size):
            batch = all_chunks[i:i + self.batch_size]

            if self.use_embeddings and self.embedder:
                texts = [c.content_with_context for c in batch]
                try:
                    embeddings = await self.embedder.generate(texts)
                except Exception as e:
                    print(f"  Embedding error: {e}, using zero vectors")
                    embeddings = [[0.0] * 1536 for _ in batch]
            else:
                embeddings = [[0.0] * 1536 for _ in batch]

            for chunk, embedding in zip(batch, embeddings):
                if await self._insert_chunk(chunk, embedding):
                    self.stats['chunks'] += 1

            print(f"  Indexed {min(i + self.batch_size, len(all_chunks))}/{len(all_chunks)} chunks")

        print(f"  Done: {source_info['title']}")

    async def _create_source(
        self, code: str, title: str, short_title: str, jurisdiction: str, legal_type: str
    ) -> Optional[str]:
        """Cree ou recupere une source juridique"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Verifier si existe deja
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/legal_sources",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                },
                params={"code": f"eq.{code}"}
            )

            if response.status_code == 200 and response.json():
                source = response.json()[0]
                print(f"  Source exists: {source['id']}")
                return source['id']

            # Creer nouvelle source
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/legal_sources",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation"
                },
                json={
                    "code": code,
                    "title": title,
                    "short_title": short_title,
                    "jurisdiction": jurisdiction,
                    "legal_type": legal_type,
                    "language": "fr"
                }
            )

            if response.status_code in [200, 201]:
                source = response.json()[0]
                print(f"  Created source: {source['id']}")
                return source['id']
            else:
                print(f"  Error creating source: {response.text}")
                self.stats['errors'].append(f"Source creation failed: {code}")
                return None

    async def _create_document(self, source_id: str, article: Dict) -> Optional[str]:
        """Cree un document (article)"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/legal_documents",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
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

            if response.status_code in [200, 201]:
                return response.json()[0]["id"]
            return None

    async def _insert_chunk(self, chunk: LegalChunk, embedding: List[float]) -> bool:
        """Insere un chunk vectorise"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/document_chunks",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
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
            return response.status_code in [200, 201]


async def main():
    """Point d'entree principal"""
    import argparse

    parser = argparse.ArgumentParser(description="Mass Legal Document Indexer")
    parser.add_argument(
        "--jurisdictions", "-j",
        nargs="+",
        default=["DZ"],
        help="Jurisdictions to index (DZ, CH, FR)"
    )
    parser.add_argument(
        "--no-embeddings",
        action="store_true",
        help="Skip embedding generation (use zero vectors)"
    )
    parser.add_argument(
        "--batch-size", "-b",
        type=int,
        default=50,
        help="Batch size for embedding generation"
    )

    args = parser.parse_args()

    indexer = MassLegalIndexer(
        batch_size=args.batch_size,
        use_embeddings=not args.no_embeddings
    )

    await indexer.index_all(jurisdictions=args.jurisdictions)


if __name__ == "__main__":
    asyncio.run(main())
