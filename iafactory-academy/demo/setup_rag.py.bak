#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IAFactory-School - Setup RAG
Script d'initialisation du systeme RAG avec ChromaDB
"""

import sys
import io
import os
from pathlib import Path
from typing import List, Dict

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))


def print_header(title: str, char: str = "=", length: int = 70):
    print(char * length)
    print(title)
    print(char * length)


def check_dependencies() -> Dict[str, bool]:
    """Check if required dependencies are installed"""
    dependencies = {
        "langchain": False,
        "langchain_community": False,
        "langchain_openai": False,
        "langchain_ollama": False,
        "chromadb": False,
        "sentence_transformers": False,
    }

    for dep in dependencies:
        try:
            __import__(dep)
            dependencies[dep] = True
        except ImportError:
            dependencies[dep] = False

    return dependencies


def load_markdown_documents(docs_path: Path) -> List[Dict]:
    """Load all markdown documents from the documents folder"""
    documents = []

    if not docs_path.exists():
        print(f"[ERREUR] Dossier non trouve: {docs_path}")
        return documents

    for md_file in docs_path.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            documents.append({
                "filename": md_file.name,
                "content": content,
                "path": str(md_file),
                "size": len(content),
                "lines": len(content.split("\n"))
            })
            print(f"  [OK] {md_file.name} ({len(content):,} caracteres)")
        except Exception as e:
            print(f"  [ERREUR] {md_file.name}: {e}")

    return documents


def setup_chromadb(persist_dir: str) -> bool:
    """Initialize ChromaDB with the documents"""
    try:
        import chromadb
        from chromadb.config import Settings

        # Create persist directory
        Path(persist_dir).mkdir(parents=True, exist_ok=True)

        # Initialize client
        client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )

        print(f"  [OK] ChromaDB initialise dans: {persist_dir}")

        # List existing collections
        collections = client.list_collections()
        print(f"  [INFO] Collections existantes: {len(collections)}")
        for col in collections:
            print(f"    - {col.name}")

        return True

    except Exception as e:
        print(f"  [ERREUR] ChromaDB: {e}")
        return False


def ingest_documents_simple(documents: List[Dict], persist_dir: str) -> bool:
    """Ingest documents into ChromaDB (simple mode without embeddings API)"""
    try:
        import chromadb
        from chromadb.config import Settings

        client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )

        # Create or get collection
        collection_name = "iafactory_docs"

        # Delete existing collection if exists
        try:
            client.delete_collection(collection_name)
            print(f"  [INFO] Collection '{collection_name}' supprimee")
        except Exception:
            pass

        # Create new collection with default embeddings
        collection = client.create_collection(
            name=collection_name,
            metadata={"description": "IAFactory-School documentation"}
        )

        print(f"  [OK] Collection '{collection_name}' creee")

        # Add documents
        doc_ids = []
        doc_contents = []
        doc_metadatas = []

        for i, doc in enumerate(documents):
            # Split document into chunks
            content = doc["content"]
            chunks = split_into_chunks(content, chunk_size=1000, overlap=200)

            for j, chunk in enumerate(chunks):
                doc_id = f"{doc['filename']}_{j}"
                doc_ids.append(doc_id)
                doc_contents.append(chunk)
                doc_metadatas.append({
                    "source": doc["filename"],
                    "chunk_index": j,
                    "total_chunks": len(chunks)
                })

        # Add all documents at once
        collection.add(
            ids=doc_ids,
            documents=doc_contents,
            metadatas=doc_metadatas
        )

        print(f"  [OK] {len(doc_ids)} chunks ajoutes a la collection")

        return True

    except Exception as e:
        print(f"  [ERREUR] Ingestion: {e}")
        import traceback
        traceback.print_exc()
        return False


def split_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks"""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        # Try to break at paragraph or sentence boundary
        if end < len(text):
            # Look for paragraph break
            last_para = chunk.rfind("\n\n")
            if last_para > chunk_size // 2:
                end = start + last_para
                chunk = text[start:end]
            else:
                # Look for sentence break
                last_period = chunk.rfind(". ")
                if last_period > chunk_size // 2:
                    end = start + last_period + 1
                    chunk = text[start:end]

        chunks.append(chunk.strip())
        start = end - overlap

    return [c for c in chunks if c]  # Remove empty chunks


def test_search(persist_dir: str) -> bool:
    """Test the search functionality"""
    try:
        import chromadb
        from chromadb.config import Settings

        client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )

        collection = client.get_collection("iafactory_docs")

        # Test queries
        test_queries = [
            ("Prix par eleve", "fr"),
            ("Investissement IAFactory", "fr"),
            ("Technologies utilisees", "fr"),
        ]

        print("\nTest de recherche:")
        print("-" * 50)

        for query, lang in test_queries:
            results = collection.query(
                query_texts=[query],
                n_results=2
            )

            print(f"\n  Q: {query}")
            if results["documents"] and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0][:2]):
                    preview = doc[:100].replace("\n", " ")
                    print(f"    [{i+1}] {preview}...")
            else:
                print("    [Aucun resultat]")

        return True

    except Exception as e:
        print(f"  [ERREUR] Test recherche: {e}")
        return False


def main():
    print("\n")
    print_header("SETUP RAG - IAFactory-School")

    # Step 1: Check dependencies
    print("\n1. VERIFICATION DES DEPENDANCES")
    print("-" * 50)
    deps = check_dependencies()
    all_deps_ok = True

    for dep, installed in deps.items():
        status = "[OK]" if installed else "[MANQUANT]"
        print(f"  {status} {dep}")
        if not installed:
            all_deps_ok = False

    if not all_deps_ok:
        print("\n  [ATTENTION] Certaines dependances manquent.")
        print("  Executez: pip install langchain langchain-community langchain-openai langchain-ollama chromadb sentence-transformers")

    # Step 2: Load documents
    print("\n2. CHARGEMENT DES DOCUMENTS")
    print("-" * 50)
    docs_path = Path(__file__).parent / "documents"
    documents = load_markdown_documents(docs_path)

    if not documents:
        print("  [ERREUR] Aucun document trouve!")
        print(f"  Creez des fichiers .md dans: {docs_path}")
        return

    print(f"\n  Total: {len(documents)} documents charges")
    total_chars = sum(d["size"] for d in documents)
    print(f"  Taille totale: {total_chars:,} caracteres")

    # Step 3: Setup ChromaDB
    print("\n3. INITIALISATION CHROMADB")
    print("-" * 50)
    persist_dir = str(Path(__file__).parent / "data" / "chromadb")

    if deps.get("chromadb", False):
        chromadb_ok = setup_chromadb(persist_dir)
    else:
        print("  [SKIP] ChromaDB non installe")
        chromadb_ok = False

    # Step 4: Ingest documents
    print("\n4. INGESTION DES DOCUMENTS")
    print("-" * 50)

    if chromadb_ok:
        ingest_ok = ingest_documents_simple(documents, persist_dir)
    else:
        print("  [SKIP] ChromaDB non disponible")
        ingest_ok = False

    # Step 5: Test search
    print("\n5. TEST DE RECHERCHE")
    print("-" * 50)

    if ingest_ok:
        test_ok = test_search(persist_dir)
    else:
        print("  [SKIP] Documents non ingeres")
        test_ok = False

    # Summary
    print("\n")
    print_header("RESUME")
    print(f"""
  Documents charges: {len(documents)}
  ChromaDB: {"OK" if chromadb_ok else "NON"}
  Ingestion: {"OK" if ingest_ok else "NON"}
  Test recherche: {"OK" if test_ok else "NON"}
""")

    if chromadb_ok and ingest_ok and test_ok:
        print("  [SUCCES] Le systeme RAG est pret!")
        print(f"\n  Lancez le chatbot avec:")
        print(f"    python -m streamlit run demo/chatbot_rag.py --server.port 8504")
    else:
        print("  [ATTENTION] Le systeme fonctionne en mode simplifie.")
        print("  Installez les dependances pour le mode RAG complet.")

    print("\n")


if __name__ == "__main__":
    main()
