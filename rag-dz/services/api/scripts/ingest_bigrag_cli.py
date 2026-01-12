#!/usr/bin/env python3
"""
INGEST_BIGRAG_CLI - Script d'ingestion BIG RAG
==============================================
Script CLI pour ingérer des documents dans les collections Qdrant

Usage:
    python ingest_bigrag_cli.py --dz            # Ingère data/rag_dz_seed.json
    python ingest_bigrag_cli.py --ch            # Ingère data/rag_ch_seed.json
    python ingest_bigrag_cli.py --global        # Ingère data/rag_global_seed.json
    python ingest_bigrag_cli.py --all           # Ingère tous les fichiers
    python ingest_bigrag_cli.py --file data/custom.json --collection rag_dz
    python ingest_bigrag_cli.py --sample-dz     # Données de test DZ
    python ingest_bigrag_cli.py --sample-ch     # Données de test CH
    python ingest_bigrag_cli.py --status        # Affiche le statut des collections

Options:
    --dz            Ingérer les documents Algérie depuis data/rag_dz_seed.json
    --ch            Ingérer les documents Suisse depuis data/rag_ch_seed.json
    --global        Ingérer les documents internationaux depuis data/rag_global_seed.json
    --all           Ingérer tous les fichiers seed
    --file PATH     Ingérer un fichier spécifique
    --collection    Collection cible (rag_dz, rag_ch, rag_global)
    --sample-dz     Ingérer des données de test pour DZ
    --sample-ch     Ingérer des données de test pour CH
    --status        Afficher le statut des collections
    --clear COLL    Vider une collection (demande confirmation)
    --ensure        S'assurer que les collections existent
"""

import os
import sys
import json
import argparse
import asyncio
from pathlib import Path
from datetime import datetime

# Ajouter le path du projet
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.bigrag_ingest.ingest_models import (
    RAGDocument,
    RAGIngestBatch,
    IngestStatus,
)
from app.bigrag_ingest.ingest_service import (
    IngestService,
    get_ingest_service,
    init_ingest_service,
)


# Configuration
DATA_DIR = project_root / "data"
DEFAULT_FILES = {
    "dz": DATA_DIR / "rag_dz_seed.json",
    "ch": DATA_DIR / "rag_ch_seed.json",
    "global": DATA_DIR / "rag_global_seed.json",
}


def print_banner():
    """Affiche la bannière"""
    print("""
╔════════════════════════════════════════════════════════════╗
║           🌱 BIGRAG INGEST CLI - Multi-Pays                ║
║                  DZ 🇩🇿  CH 🇨🇭  GLOBAL 🌍                   ║
╚════════════════════════════════════════════════════════════╝
    """)


def print_result(result, collection):
    """Affiche le résultat d'une ingestion"""
    status_icon = "✅" if result.success else "❌"
    print(f"\n{status_icon} {collection.upper()}")
    print(f"   Total: {result.total}")
    print(f"   Inserted: {result.inserted}")
    print(f"   Failed: {result.failed}")
    print(f"   Processing time: {result.processing_time_ms}ms")
    
    if result.errors:
        print(f"   Errors:")
        for err in result.errors[:5]:
            print(f"      - {err}")
        if len(result.errors) > 5:
            print(f"      ... and {len(result.errors) - 5} more")


async def ingest_file(service: IngestService, file_path: Path, collection: str):
    """Ingère un fichier"""
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return None
    
    print(f"\n📄 Loading {file_path.name}...")
    
    try:
        content = file_path.read_text(encoding="utf-8")
        
        # Parser
        docs = []
        if str(file_path).endswith(".json"):
            data = json.loads(content)
            if isinstance(data, list):
                docs = [RAGDocument(**d) for d in data]
            elif isinstance(data, dict) and "docs" in data:
                docs = [RAGDocument(**d) for d in data["docs"]]
        elif str(file_path).endswith((".ndjson", ".jsonl")):
            for line in content.strip().split("\n"):
                if line.strip():
                    docs.append(RAGDocument(**json.loads(line)))
        
        if not docs:
            print(f"⚠️ No documents found in {file_path}")
            return None
        
        print(f"   Found {len(docs)} documents")
        
        # Ingérer
        batch = RAGIngestBatch(collection=collection, docs=docs)
        result = await service.ingest_batch(batch)
        
        print_result(result, collection)
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def ingest_sample_dz(service: IngestService):
    """Ingère des données de test DZ"""
    sample_docs = [
        RAGDocument(
            title="TVA en Algérie - Taux et obligations",
            text="""La taxe sur la valeur ajoutée (TVA) en Algérie est un impôt indirect 
            prélevé sur la consommation. Elle est appliquée aux taux suivants:
            - Taux normal: 19% (applicable à la plupart des biens et services)
            - Taux réduit: 9% (applicable à certains produits de première nécessité)
            
            Les entreprises dont le chiffre d'affaires annuel dépasse 30 millions DA 
            sont assujetties à la TVA.""",
            country="DZ",
            language="fr",
            theme="Fiscalité",
            source="DGI",
            tags=["TVA", "DGI", "Fiscalité"],
            is_official=True,
        ),
        RAGDocument(
            title="CNAS - Cotisations sociales employeur",
            text="""La Caisse Nationale des Assurances Sociales (CNAS) gère le régime 
            de sécurité sociale des travailleurs salariés en Algérie.
            
            Taux de cotisation:
            - Part employeur: 25%
            - Part salarié: 9%
            - Total: 34% du salaire brut""",
            country="DZ",
            language="fr",
            theme="Sécurité Sociale",
            source="CNAS",
            tags=["CNAS", "Cotisations", "Sécurité sociale"],
            is_official=True,
        ),
        RAGDocument(
            title="ضريبة القيمة المضافة في الجزائر",
            text="""ضريبة القيمة المضافة هي ضريبة غير مباشرة تفرض على الاستهلاك.
            
            معدلات الضريبة:
            - المعدل العادي: 19%
            - المعدل المخفض: 9% (للسلع الأساسية)""",
            country="DZ",
            language="ar",
            theme="Fiscalité",
            source="DGI",
            tags=["TVA", "DGI", "ضرائب"],
            is_official=True,
        ),
    ]
    
    print("\n🧪 Ingesting sample DZ documents...")
    result = await service.ingest_dz_docs(sample_docs)
    print_result(result, "rag_dz")
    return result


async def ingest_sample_ch(service: IngestService):
    """Ingère des données de test CH"""
    sample_docs = [
        RAGDocument(
            title="AVS - Assurance vieillesse et survivants",
            text="""L'AVS est le premier pilier du système de prévoyance suisse.
            
            Cotisations:
            - Salariés: 4.35% (part employé) + 4.35% (part employeur) = 8.7%
            - Indépendants: 7.8% à 8.1% selon le revenu""",
            country="CH",
            language="fr",
            theme="Sécurité Sociale",
            source="AVS",
            tags=["AVS", "Retraite", "Prévoyance"],
            is_official=True,
        ),
        RAGDocument(
            title="TVA Suisse - Taux et assujettissement",
            text="""La taxe sur la valeur ajoutée en Suisse est gérée par l'AFC.
            
            Taux de TVA (2024):
            - Taux normal: 8.1%
            - Taux réduit: 2.6%
            - Taux spécial hébergement: 3.8%""",
            country="CH",
            language="fr",
            theme="Fiscalité",
            source="TVA-CH",
            tags=["TVA", "AFC", "Fiscalité"],
            is_official=True,
        ),
    ]
    
    print("\n🧪 Ingesting sample CH documents...")
    result = await service.ingest_ch_docs(sample_docs)
    print_result(result, "rag_ch")
    return result


async def show_status(service: IngestService):
    """Affiche le statut des collections"""
    print("\n📊 Collections Status")
    print("=" * 50)
    
    status = await service.get_status()
    
    print(f"\n🔧 Configuration:")
    print(f"   Embedding model: {status.embedding_model}")
    print(f"   Qdrant: {status.qdrant_host}")
    
    print(f"\n📁 Collections:")
    for coll in status.collections:
        icon = "✅" if coll.exists else "❌"
        print(f"   {icon} {coll.name}")
        if coll.exists:
            print(f"      Documents: {coll.points_count}")
            print(f"      Vector size: {coll.vector_size}")
            print(f"      Status: {coll.status}")
    
    print(f"\n📈 Totals:")
    print(f"   DZ: {status.dz_count} documents")
    print(f"   CH: {status.ch_count} documents")
    print(f"   Global: {status.global_count} documents")
    print(f"   Total: {status.total_documents} documents")


async def clear_collection(service: IngestService, collection: str):
    """Vide une collection"""
    if collection not in ["rag_dz", "rag_ch", "rag_global"]:
        print(f"❌ Invalid collection: {collection}")
        return
    
    confirm = input(f"\n⚠️ Are you sure you want to clear '{collection}'? (yes/no): ")
    if confirm.lower() != "yes":
        print("Cancelled.")
        return
    
    try:
        service.qdrant.delete_collection(collection)
        service.ensure_collection(collection)
        print(f"✅ Collection '{collection}' cleared and recreated")
    except Exception as e:
        print(f"❌ Error: {e}")


async def ensure_collections(service: IngestService):
    """S'assure que les collections existent"""
    print("\n🔧 Ensuring collections exist...")
    
    for name in ["rag_dz", "rag_ch", "rag_global"]:
        success = service.ensure_collection(name)
        icon = "✅" if success else "❌"
        print(f"   {icon} {name}")


async def main():
    """Main CLI"""
    parser = argparse.ArgumentParser(
        description="BigRAG Ingest CLI - Ingestion documents multi-pays"
    )
    
    # Options d'ingestion par pays
    parser.add_argument("--dz", action="store_true", help="Ingérer data/rag_dz_seed.json")
    parser.add_argument("--ch", action="store_true", help="Ingérer data/rag_ch_seed.json")
    parser.add_argument("--global", dest="global_", action="store_true", help="Ingérer data/rag_global_seed.json")
    parser.add_argument("--all", action="store_true", help="Ingérer tous les fichiers seed")
    
    # Ingestion fichier custom
    parser.add_argument("--file", type=str, help="Chemin du fichier à ingérer")
    parser.add_argument("--collection", type=str, default="rag_dz", 
                       choices=["rag_dz", "rag_ch", "rag_global"],
                       help="Collection cible")
    
    # Données de test
    parser.add_argument("--sample-dz", action="store_true", help="Ingérer données de test DZ")
    parser.add_argument("--sample-ch", action="store_true", help="Ingérer données de test CH")
    
    # Administration
    parser.add_argument("--status", action="store_true", help="Afficher le statut")
    parser.add_argument("--clear", type=str, help="Vider une collection")
    parser.add_argument("--ensure", action="store_true", help="S'assurer que les collections existent")
    
    # Configuration
    parser.add_argument("--qdrant-host", type=str, default="localhost", help="Qdrant host")
    parser.add_argument("--qdrant-port", type=int, default=6333, help="Qdrant port")
    
    args = parser.parse_args()
    
    print_banner()
    
    # Initialiser le service
    service = init_ingest_service(
        qdrant_host=os.getenv("QDRANT_HOST", args.qdrant_host),
        qdrant_port=int(os.getenv("QDRANT_PORT", args.qdrant_port)),
    )
    
    # Actions
    if args.status:
        await show_status(service)
        return
    
    if args.ensure:
        await ensure_collections(service)
        return
    
    if args.clear:
        await clear_collection(service, args.clear)
        return
    
    if args.sample_dz:
        await ingest_sample_dz(service)
        return
    
    if args.sample_ch:
        await ingest_sample_ch(service)
        return
    
    if args.file:
        file_path = Path(args.file)
        if not file_path.is_absolute():
            file_path = project_root / args.file
        await ingest_file(service, file_path, args.collection)
        return
    
    if args.dz or args.all:
        await ingest_file(service, DEFAULT_FILES["dz"], "rag_dz")
    
    if args.ch or args.all:
        await ingest_file(service, DEFAULT_FILES["ch"], "rag_ch")
    
    if args.global_ or args.all:
        await ingest_file(service, DEFAULT_FILES["global"], "rag_global")
    
    if not any([args.dz, args.ch, args.global_, args.all, args.file, 
                args.sample_dz, args.sample_ch, args.status, args.clear, args.ensure]):
        parser.print_help()
        print("\n💡 Quick start:")
        print("   python ingest_bigrag_cli.py --sample-dz    # Test avec données DZ")
        print("   python ingest_bigrag_cli.py --status       # Voir le statut")


if __name__ == "__main__":
    asyncio.run(main())
