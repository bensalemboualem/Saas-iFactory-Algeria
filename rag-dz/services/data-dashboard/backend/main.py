"""
DZ Data Dashboard - Backend API
Monitoring & pilotage du RAG Algérie
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional
import random
from collections import defaultdict

from models import (
    DocumentIndexed, IngestionLog, DocumentType, DocumentStatus, RunStatus,
    DataSummaryResponse, SourceSummary, TypeSummary, RunSummary,
    SourceDetailResponse, DocumentDetail, RunsListResponse,
    HealthResponse, SourceHealthStatus, PublicStatsResponse, SourceHealth
)

app = FastAPI(
    title="DZ Data Dashboard API",
    description="API de monitoring et pilotage du RAG Algérie",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== IN-MEMORY DATA STORE (Demo) ====================
# En production, utiliser PostgreSQL avec SQLAlchemy

SOURCES_CONFIG = {
    "DZ_JO": {
        "name": "Journal Officiel",
        "description": "Lois, décrets et textes officiels de la République Algérienne",
        "types": [DocumentType.LAW, DocumentType.DECREE, DocumentType.CIRCULAR]
    },
    "DZ_DGI": {
        "name": "Direction Générale des Impôts",
        "description": "Notes fiscales, instructions et barèmes",
        "types": [DocumentType.TAX, DocumentType.INSTRUCTION, DocumentType.CIRCULAR]
    },
    "DZ_ONS": {
        "name": "Office National des Statistiques",
        "description": "Données statistiques et rapports économiques",
        "types": [DocumentType.STATISTIC, DocumentType.REPORT]
    },
    "DZ_DOUANE": {
        "name": "Douanes Algériennes",
        "description": "Tarifs douaniers et procédures d'import/export",
        "types": [DocumentType.PROCEDURE, DocumentType.TAX]
    },
    "DZ_NEWS": {
        "name": "Actualités Économiques",
        "description": "Veille actualités business et économie algérienne",
        "types": [DocumentType.NEWS]
    },
    "DZ_CNRC": {
        "name": "CNRC - Registre du Commerce",
        "description": "Procédures d'enregistrement et formulaires",
        "types": [DocumentType.PROCEDURE]
    },
    "DZ_CNAS": {
        "name": "CNAS - Sécurité Sociale",
        "description": "Cotisations sociales et prestations",
        "types": [DocumentType.PROCEDURE, DocumentType.CIRCULAR]
    },
    "DZ_BOAMP": {
        "name": "Marchés Publics",
        "description": "Appels d'offres et avis de marchés",
        "types": [DocumentType.PROCEDURE, DocumentType.NEWS]
    }
}

# Générer des données de démonstration
documents_store: list[DocumentIndexed] = []
ingestion_logs_store: list[IngestionLog] = []


def generate_demo_data():
    """Génère des données de démonstration réalistes"""
    global documents_store, ingestion_logs_store
    
    documents_store = []
    ingestion_logs_store = []
    
    now = datetime.utcnow()
    
    # Documents par source avec données réalistes
    demo_docs = {
        "DZ_JO": [
            ("Loi de Finances 2025", DocumentType.LAW, 45),
            ("Décret exécutif n°24-312 relatif aux start-ups", DocumentType.DECREE, 28),
            ("Loi n°23-12 sur le commerce électronique", DocumentType.LAW, 67),
            ("Ordonnance n°24-01 portant réforme fiscale", DocumentType.LAW, 89),
            ("Décret n°24-156 sur les zones franches", DocumentType.DECREE, 34),
            ("Loi organique sur l'investissement", DocumentType.LAW, 112),
            ("Arrêté fixant les taux de TVA", DocumentType.CIRCULAR, 15),
            ("Loi sur la protection des données personnelles", DocumentType.LAW, 78),
            ("Décret portant statut de l'auto-entrepreneur", DocumentType.DECREE, 42),
            ("Loi relative aux sociétés commerciales", DocumentType.LAW, 156),
        ],
        "DZ_DGI": [
            ("Note n°2024-089 - Modalités IBS PME", DocumentType.TAX, 12),
            ("Instruction n°2024-045 - TVA import", DocumentType.INSTRUCTION, 18),
            ("Barème IRG 2024", DocumentType.TAX, 8),
            ("Guide déclaration G50", DocumentType.PROCEDURE, 24),
            ("Circulaire TAP collectivités locales", DocumentType.CIRCULAR, 15),
            ("Note avantages fiscaux zones Sud", DocumentType.TAX, 22),
            ("Instruction retenue à la source", DocumentType.INSTRUCTION, 19),
            ("Guide télédéclaration JIBAYA'TIC", DocumentType.PROCEDURE, 35),
        ],
        "DZ_ONS": [
            ("Indices des prix à la consommation Q3 2024", DocumentType.STATISTIC, 6),
            ("Rapport PIB sectoriel 2023", DocumentType.REPORT, 45),
            ("Statistiques commerce extérieur", DocumentType.STATISTIC, 12),
            ("Démographie des entreprises 2024", DocumentType.STATISTIC, 28),
            ("Indice production industrielle", DocumentType.STATISTIC, 8),
        ],
        "DZ_DOUANE": [
            ("Tarif douanier intégré 2024", DocumentType.TAX, 234),
            ("Procédure dédouanement simplifié", DocumentType.PROCEDURE, 18),
            ("Guide opérateur économique agréé", DocumentType.PROCEDURE, 42),
            ("Liste produits contingentés", DocumentType.TAX, 15),
            ("Formulaires SYDONIA", DocumentType.PROCEDURE, 8),
        ],
        "DZ_NEWS": [
            ("Banque d'Algérie - nouveau taux directeur", DocumentType.NEWS, 3),
            ("Partenariat Sonatrach-ENI renouvelé", DocumentType.NEWS, 5),
            ("Forum investissement Algérie-France", DocumentType.NEWS, 4),
            ("Lancement bourse PME Alger", DocumentType.NEWS, 6),
            ("Réforme bancaire digitale annoncée", DocumentType.NEWS, 4),
        ],
        "DZ_CNRC": [
            ("Guide création SARL", DocumentType.PROCEDURE, 25),
            ("Formulaire immatriculation registre commerce", DocumentType.PROCEDURE, 8),
            ("Procédure modification statuts", DocumentType.PROCEDURE, 12),
            ("Liste activités réglementées", DocumentType.PROCEDURE, 45),
        ],
        "DZ_CNAS": [
            ("Barème cotisations sociales 2024", DocumentType.PROCEDURE, 10),
            ("Guide affiliation employeur", DocumentType.PROCEDURE, 18),
            ("Déclaration annuelle des salaires", DocumentType.PROCEDURE, 14),
            ("Prestations familiales - conditions", DocumentType.CIRCULAR, 22),
        ],
        "DZ_BOAMP": [
            ("Avis AO - Autoroute Est-Ouest lot 3", DocumentType.NEWS, 8),
            ("Marché fourniture équipements hospitaliers", DocumentType.NEWS, 5),
            ("Cahier des charges type marchés publics", DocumentType.PROCEDURE, 67),
        ],
    }
    
    # Créer les documents
    for source_name, docs in demo_docs.items():
        for i, (title, doc_type, nb_chunks) in enumerate(docs):
            days_ago = random.randint(1, 180)
            doc_date = now - timedelta(days=days_ago + random.randint(0, 30))
            ingest_date = now - timedelta(days=days_ago)
            
            doc = DocumentIndexed(
                doc_id=f"{source_name}_{i+1:04d}",
                title=title,
                source_name=source_name,
                type=doc_type,
                source_url=f"https://source.dz/{source_name.lower()}/doc_{i+1}",
                date_document=doc_date,
                date_ingested=ingest_date,
                nb_chunks=nb_chunks,
                status=DocumentStatus.OK if random.random() > 0.05 else DocumentStatus.PARTIAL
            )
            documents_store.append(doc)
    
    # Créer les logs d'ingestion
    for source_name in SOURCES_CONFIG.keys():
        # Générer 5-10 runs par source
        num_runs = random.randint(5, 10)
        for i in range(num_runs):
            days_ago = i * random.randint(3, 7)
            start = now - timedelta(days=days_ago, hours=random.randint(0, 12))
            duration = random.randint(30, 600)  # 30s à 10min
            end = start + timedelta(seconds=duration)
            
            # 85% success, 10% partial, 5% error
            rand = random.random()
            if rand > 0.95:
                status = RunStatus.ERROR
                error_msg = random.choice([
                    "Timeout lors de la connexion au serveur source",
                    "Erreur parsing PDF - format non reconnu",
                    "Rate limit atteint sur l'API source",
                    "Certificat SSL expiré"
                ])
            elif rand > 0.85:
                status = RunStatus.PARTIAL
                error_msg = "Certains documents n'ont pas pu être traités"
            else:
                status = RunStatus.SUCCESS
                error_msg = None
            
            nb_docs = random.randint(1, 15) if status != RunStatus.ERROR else 0
            nb_chunks = nb_docs * random.randint(10, 50) if status != RunStatus.ERROR else 0
            
            log = IngestionLog(
                source_name=source_name,
                run_id=f"run_{source_name}_{now.strftime('%Y%m%d')}_{i+1:03d}",
                start_time=start,
                end_time=end,
                status=status,
                nb_documents=nb_docs,
                nb_chunks=nb_chunks,
                error_message=error_msg
            )
            ingestion_logs_store.append(log)


# Initialiser les données de démo au démarrage
generate_demo_data()


# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    return {
        "service": "DZ Data Dashboard API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "summary": "/api/dz-data/summary",
            "source": "/api/dz-data/source/{source_name}",
            "runs": "/api/dz-data/runs",
            "health": "/api/dz-data/health",
            "public_stats": "/api/public/dz-data/stats"
        }
    }


@app.get("/api/dz-data/summary", response_model=DataSummaryResponse)
async def get_summary():
    """Résumé global des données indexées dans le RAG-DZ"""
    
    # Calculs par source
    by_source_dict = defaultdict(lambda: {"docs": 0, "chunks": 0, "last_doc": None, "last_ingest": None})
    for doc in documents_store:
        src = by_source_dict[doc.source_name]
        src["docs"] += 1
        src["chunks"] += doc.nb_chunks
        if doc.date_document:
            if not src["last_doc"] or doc.date_document > src["last_doc"]:
                src["last_doc"] = doc.date_document
        if not src["last_ingest"] or doc.date_ingested > src["last_ingest"]:
            src["last_ingest"] = doc.date_ingested
    
    by_source = [
        SourceSummary(
            source_name=name,
            document_count=data["docs"],
            chunk_count=data["chunks"],
            last_document_date=data["last_doc"].strftime("%Y-%m-%d") if data["last_doc"] else None,
            last_ingested_at=data["last_ingest"].isoformat() if data["last_ingest"] else None
        )
        for name, data in sorted(by_source_dict.items(), key=lambda x: x[1]["docs"], reverse=True)
    ]
    
    # Calculs par type
    by_type_dict = defaultdict(int)
    for doc in documents_store:
        by_type_dict[doc.type.value] += 1
    
    by_type = [
        TypeSummary(type=t, document_count=c)
        for t, c in sorted(by_type_dict.items(), key=lambda x: x[1], reverse=True)
    ]
    
    # Derniers runs
    sorted_logs = sorted(ingestion_logs_store, key=lambda x: x.start_time, reverse=True)[:10]
    last_runs = [
        RunSummary(
            source_name=log.source_name,
            run_id=log.run_id,
            start_time=log.start_time.isoformat(),
            end_time=log.end_time.isoformat() if log.end_time else None,
            status=log.status.value,
            nb_documents=log.nb_documents,
            nb_chunks=log.nb_chunks,
            error_message=log.error_message,
            duration_seconds=int((log.end_time - log.start_time).total_seconds()) if log.end_time else None
        )
        for log in sorted_logs
    ]
    
    return DataSummaryResponse(
        total_documents=len(documents_store),
        total_chunks=sum(doc.nb_chunks for doc in documents_store),
        sources_count=len(by_source_dict),
        by_source=by_source,
        by_type=by_type,
        last_runs=last_runs
    )


@app.get("/api/dz-data/source/{source_name}", response_model=SourceDetailResponse)
async def get_source_detail(
    source_name: str,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    doc_type: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
):
    """Détails d'une source spécifique"""
    
    # Filtrer les documents
    filtered = [doc for doc in documents_store if doc.source_name == source_name]
    
    if not filtered:
        raise HTTPException(status_code=404, detail=f"Source '{source_name}' non trouvée")
    
    # Filtres optionnels
    if doc_type:
        filtered = [doc for doc in filtered if doc.type.value == doc_type]
    
    if date_from:
        try:
            from_dt = datetime.fromisoformat(date_from)
            filtered = [doc for doc in filtered if doc.date_document and doc.date_document >= from_dt]
        except ValueError:
            pass
    
    if date_to:
        try:
            to_dt = datetime.fromisoformat(date_to)
            filtered = [doc for doc in filtered if doc.date_document and doc.date_document <= to_dt]
        except ValueError:
            pass
    
    # Tri et pagination
    filtered = sorted(filtered, key=lambda x: x.date_ingested, reverse=True)
    total = len(filtered)
    paginated = filtered[offset:offset + limit]
    
    documents = [
        DocumentDetail(
            id=doc.id,
            title=doc.title,
            type=doc.type.value,
            source_url=doc.source_url,
            date_document=doc.date_document.strftime("%Y-%m-%d") if doc.date_document else None,
            date_ingested=doc.date_ingested.isoformat(),
            nb_chunks=doc.nb_chunks,
            status=doc.status.value
        )
        for doc in paginated
    ]
    
    return SourceDetailResponse(
        source_name=source_name,
        total_documents=total,
        total_chunks=sum(doc.nb_chunks for doc in filtered),
        documents=documents,
        page=(offset // limit) + 1,
        limit=limit,
        has_more=(offset + limit) < total
    )


@app.get("/api/dz-data/runs", response_model=RunsListResponse)
async def get_runs(
    source_name: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100)
):
    """Liste des derniers runs d'ingestion"""
    
    filtered = ingestion_logs_store.copy()
    
    if source_name:
        filtered = [log for log in filtered if log.source_name == source_name]
    
    if status:
        filtered = [log for log in filtered if log.status.value == status]
    
    # Tri par date décroissante
    filtered = sorted(filtered, key=lambda x: x.start_time, reverse=True)[:limit]
    
    runs = [
        RunSummary(
            source_name=log.source_name,
            run_id=log.run_id,
            start_time=log.start_time.isoformat(),
            end_time=log.end_time.isoformat() if log.end_time else None,
            status=log.status.value,
            nb_documents=log.nb_documents,
            nb_chunks=log.nb_chunks,
            error_message=log.error_message,
            duration_seconds=int((log.end_time - log.start_time).total_seconds()) if log.end_time else None
        )
        for log in filtered
    ]
    
    return RunsListResponse(runs=runs, total=len(runs))


@app.get("/api/dz-data/health", response_model=HealthResponse)
async def get_health():
    """Statut de santé des sources de données"""
    
    now = datetime.utcnow()
    sources_health = []
    overall_issues = 0
    
    for source_name in SOURCES_CONFIG.keys():
        # Derniers documents de cette source
        source_docs = [doc for doc in documents_store if doc.source_name == source_name]
        
        # Dernier run de cette source
        source_runs = [log for log in ingestion_logs_store if log.source_name == source_name]
        source_runs = sorted(source_runs, key=lambda x: x.start_time, reverse=True)
        last_run = source_runs[0] if source_runs else None
        
        # Dernière date de document
        last_doc_date = None
        if source_docs:
            dates = [doc.date_document for doc in source_docs if doc.date_document]
            if dates:
                last_doc_date = max(dates)
        
        # Calcul de la fraîcheur
        freshness_days = None
        if last_doc_date:
            freshness_days = (now - last_doc_date).days
        
        # Déterminer le statut
        if last_run and last_run.status == RunStatus.ERROR:
            status = SourceHealth.ERROR
            overall_issues += 1
        elif freshness_days and freshness_days > 30:
            status = SourceHealth.WARNING
            overall_issues += 1
        elif last_run and last_run.status == RunStatus.PARTIAL:
            status = SourceHealth.WARNING
        else:
            status = SourceHealth.OK
        
        sources_health.append(SourceHealthStatus(
            source_name=source_name,
            status=status.value,
            last_run_at=last_run.start_time.isoformat() if last_run else None,
            last_run_status=last_run.status.value if last_run else None,
            last_document_date=last_doc_date.strftime("%Y-%m-%d") if last_doc_date else None,
            freshness_days=freshness_days,
            document_count=len(source_docs)
        ))
    
    # Statut global
    if overall_issues == 0:
        overall = "healthy"
    elif overall_issues <= 2:
        overall = "degraded"
    else:
        overall = "critical"
    
    return HealthResponse(
        overall_status=overall,
        sources=sources_health,
        last_check=now.isoformat()
    )


@app.get("/api/public/dz-data/stats", response_model=PublicStatsResponse)
async def get_public_stats():
    """Stats publiques pour affichage marketing"""
    
    now = datetime.utcnow()
    
    # Compter par type
    laws = sum(1 for doc in documents_store if doc.type in [DocumentType.LAW, DocumentType.DECREE])
    tax_docs = sum(1 for doc in documents_store if doc.type in [DocumentType.TAX, DocumentType.INSTRUCTION])
    procedures = sum(1 for doc in documents_store if doc.type == DocumentType.PROCEDURE)
    
    # Sources actives
    sources = set(doc.source_name for doc in documents_store)
    
    # Dernière mise à jour
    if documents_store:
        last_update = max(doc.date_ingested for doc in documents_store)
    else:
        last_update = now
    
    # Couverture
    coverage = {
        "journal_officiel": "DZ_JO" in sources,
        "dgi_fiscalite": "DZ_DGI" in sources,
        "statistiques_ons": "DZ_ONS" in sources,
        "douanes": "DZ_DOUANE" in sources,
        "actualites": "DZ_NEWS" in sources,
        "registre_commerce": "DZ_CNRC" in sources,
        "securite_sociale": "DZ_CNAS" in sources,
        "marches_publics": "DZ_BOAMP" in sources
    }
    
    return PublicStatsResponse(
        total_laws_indexed=laws,
        total_tax_documents=tax_docs,
        total_procedures=procedures,
        total_sources=len(sources),
        last_update=last_update.isoformat(),
        coverage=coverage
    )


@app.get("/api/dz-data/sources")
async def list_sources():
    """Liste des sources configurées"""
    return {
        "sources": [
            {
                "id": source_id,
                "name": config["name"],
                "description": config["description"],
                "types": [t.value for t in config["types"]]
            }
            for source_id, config in SOURCES_CONFIG.items()
        ]
    }


@app.post("/api/dz-data/refresh-demo")
async def refresh_demo_data():
    """Régénère les données de démo (pour tests)"""
    generate_demo_data()
    return {"message": "Données de démonstration régénérées", "documents": len(documents_store), "runs": len(ingestion_logs_store)}


# ==================== INGESTION API (pour les connecteurs DZ) ====================

@app.post("/api/dz-data/ingest/document")
async def ingest_document(
    doc_id: str,
    title: str,
    source_name: str,
    doc_type: str,
    nb_chunks: int,
    source_url: Optional[str] = None,
    date_document: Optional[str] = None
):
    """Endpoint pour que les connecteurs DZ enregistrent un document indexé"""
    
    doc_date = None
    if date_document:
        try:
            doc_date = datetime.fromisoformat(date_document)
        except ValueError:
            pass
    
    doc = DocumentIndexed(
        doc_id=doc_id,
        title=title,
        source_name=source_name,
        type=DocumentType(doc_type) if doc_type in DocumentType.__members__.values() else DocumentType.OTHER,
        source_url=source_url,
        date_document=doc_date,
        nb_chunks=nb_chunks,
        status=DocumentStatus.OK
    )
    
    documents_store.append(doc)
    
    return {"message": "Document enregistré", "id": doc.id}


@app.post("/api/dz-data/ingest/run")
async def log_ingestion_run(
    source_name: str,
    run_id: str,
    status: str,
    nb_documents: int,
    nb_chunks: int,
    start_time: str,
    end_time: Optional[str] = None,
    error_message: Optional[str] = None
):
    """Endpoint pour que les connecteurs DZ enregistrent un run d'ingestion"""
    
    log = IngestionLog(
        source_name=source_name,
        run_id=run_id,
        start_time=datetime.fromisoformat(start_time),
        end_time=datetime.fromisoformat(end_time) if end_time else None,
        status=RunStatus(status) if status in RunStatus.__members__.values() else RunStatus.SUCCESS,
        nb_documents=nb_documents,
        nb_chunks=nb_chunks,
        error_message=error_message
    )
    
    ingestion_logs_store.append(log)
    
    return {"message": "Run enregistré", "id": log.id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8205)
