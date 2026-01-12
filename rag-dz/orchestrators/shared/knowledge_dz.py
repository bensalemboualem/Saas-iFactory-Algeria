"""
Knowledge Base Algérie - Indexation des réglementations algériennes.
Pré-indexe les sources officielles pour le RAG.
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Any
from enum import Enum

from pydantic import BaseModel, Field


class KnowledgeType(str, Enum):
    """Types de connaissances"""
    FISCAL = "fiscal"           # DGI, impôts
    SOCIAL = "social"           # CNAS, CASNOS
    COMMERCE = "commerce"       # CNRC, registre de commerce
    ACCOUNTING = "accounting"   # PCN, comptabilité
    LEGAL = "legal"             # Code de commerce, droit
    LABOR = "labor"             # Code du travail
    BANKING = "banking"         # Banque d'Algérie, réglementation bancaire
    CUSTOMS = "customs"         # Douanes
    INVESTMENT = "investment"   # ANDI, investissement


class KnowledgeSource(BaseModel):
    """Source de connaissance"""
    id: str
    name: str
    type: KnowledgeType
    url: str | None = None
    document_path: str | None = None
    description: str | None = None
    last_updated: datetime | None = None
    language: str = "fr"
    priority: int = 1  # 1 = haute priorité


# ============ SOURCES OFFICIELLES ALGÉRIENNES ============

DZ_KNOWLEDGE_SOURCES: list[KnowledgeSource] = [
    # Sources fiscales
    KnowledgeSource(
        id="dgi-impots",
        name="Direction Générale des Impôts",
        type=KnowledgeType.FISCAL,
        url="https://www.mfdgi.gov.dz",
        description="Réglementation fiscale algérienne - IRG, IBS, TAP, TVA",
        priority=1
    ),
    KnowledgeSource(
        id="code-impots",
        name="Code des Impôts Directs et Taxes Assimilées",
        type=KnowledgeType.FISCAL,
        document_path="docs/dz/Code_Impots_DZ.pdf",
        description="Code complet des impôts algériens",
        priority=1
    ),

    # Sources sociales
    KnowledgeSource(
        id="cnas-securite-sociale",
        name="CNAS - Sécurité Sociale",
        type=KnowledgeType.SOCIAL,
        url="https://www.cnas.dz",
        description="Cotisations sociales, affiliations, prestations",
        priority=1
    ),
    KnowledgeSource(
        id="casnos-non-salaries",
        name="CASNOS - Non-Salariés",
        type=KnowledgeType.SOCIAL,
        url="https://www.casnos.com.dz",
        description="Sécurité sociale des non-salariés",
        priority=2
    ),

    # Sources commerce
    KnowledgeSource(
        id="cnrc-registre-commerce",
        name="CNRC - Registre de Commerce",
        type=KnowledgeType.COMMERCE,
        url="https://www.cnrc.dz",
        description="Registre de commerce, création d'entreprise",
        priority=1
    ),
    KnowledgeSource(
        id="code-commerce",
        name="Code de Commerce Algérien",
        type=KnowledgeType.COMMERCE,
        document_path="docs/dz/Code_Commerce_DZ.pdf",
        description="Code de commerce - sociétés, obligations commerciales",
        priority=1
    ),

    # Sources comptables
    KnowledgeSource(
        id="pcn-algerie",
        name="Plan Comptable National",
        type=KnowledgeType.ACCOUNTING,
        document_path="docs/dz/PCN_Algerie.pdf",
        description="Plan Comptable National algérien - SCF",
        priority=1
    ),
    KnowledgeSource(
        id="scf-normes",
        name="Système Comptable Financier",
        type=KnowledgeType.ACCOUNTING,
        document_path="docs/dz/SCF_Normes.pdf",
        description="Normes SCF alignées IAS/IFRS",
        priority=1
    ),

    # Sources juridiques
    KnowledgeSource(
        id="code-travail",
        name="Code du Travail",
        type=KnowledgeType.LABOR,
        document_path="docs/dz/Code_Travail_DZ.pdf",
        description="Relations de travail, contrats, licenciements",
        priority=1
    ),
    KnowledgeSource(
        id="joradp",
        name="Journal Officiel",
        type=KnowledgeType.LEGAL,
        url="https://www.joradp.dz",
        description="Journal Officiel de la République Algérienne",
        priority=1
    ),

    # Services publics
    KnowledgeSource(
        id="sonelgaz",
        name="Sonelgaz",
        type=KnowledgeType.LEGAL,
        url="https://www.sonelgaz.dz",
        description="Électricité et gaz - tarification, contrats",
        priority=2
    ),

    # Investissement
    KnowledgeSource(
        id="andi-investissement",
        name="ANDI - Investissement",
        type=KnowledgeType.INVESTMENT,
        url="https://www.andi.dz",
        description="Agence Nationale de Développement de l'Investissement",
        priority=2
    ),

    # Banque
    KnowledgeSource(
        id="bank-algerie",
        name="Banque d'Algérie",
        type=KnowledgeType.BANKING,
        url="https://www.bank-of-algeria.dz",
        description="Réglementation bancaire et change",
        priority=2
    ),

    # Douanes
    KnowledgeSource(
        id="douanes-algerie",
        name="Douanes Algériennes",
        type=KnowledgeType.CUSTOMS,
        url="https://www.douane.gov.dz",
        description="Tarifs douaniers, import/export",
        priority=2
    ),
]


class KnowledgeIndexer:
    """
    Indexeur de connaissances pour le marché algérien.
    Intègre avec Archon pour l'indexation dans le KB.
    """

    def __init__(
        self,
        archon_url: str = "http://localhost:8051",
        docs_path: str = "docs/dz"
    ):
        """
        Initialize the indexer.

        Args:
            archon_url: URL de l'Archon Sync service
            docs_path: Chemin vers les documents locaux
        """
        self.archon_url = archon_url
        self.docs_path = Path(docs_path)
        self.indexed_sources: list[str] = []

    async def index_all_sources(self) -> dict:
        """
        Indexe toutes les sources de connaissances.

        Returns:
            Rapport d'indexation
        """
        results = {
            "indexed": [],
            "failed": [],
            "skipped": []
        }

        for source in DZ_KNOWLEDGE_SOURCES:
            try:
                if source.url:
                    success = await self.index_url(source)
                elif source.document_path:
                    success = await self.index_document(source)
                else:
                    results["skipped"].append(source.id)
                    continue

                if success:
                    results["indexed"].append(source.id)
                    self.indexed_sources.append(source.id)
                else:
                    results["failed"].append(source.id)

            except Exception as e:
                results["failed"].append({
                    "id": source.id,
                    "error": str(e)
                })

        return results

    async def index_url(self, source: KnowledgeSource) -> bool:
        """
        Indexe une source URL via crawling.

        Args:
            source: Source à indexer

        Returns:
            True si succès
        """
        import httpx

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.archon_url}/crawl",
                    json={
                        "url": source.url,
                        "metadata": {
                            "source_id": source.id,
                            "source_name": source.name,
                            "type": source.type.value,
                            "language": source.language,
                            "priority": source.priority
                        },
                        "max_pages": 100,
                        "follow_links": True
                    },
                    timeout=300.0
                )
                return response.status_code == 200

        except Exception:
            return False

    async def index_document(self, source: KnowledgeSource) -> bool:
        """
        Indexe un document local.

        Args:
            source: Source à indexer

        Returns:
            True si succès
        """
        import httpx

        doc_path = self.docs_path / Path(source.document_path).name

        if not doc_path.exists():
            # Essayer le chemin absolu
            doc_path = Path(source.document_path)

        if not doc_path.exists():
            return False

        try:
            content = doc_path.read_bytes()

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.archon_url}/ingest",
                    files={
                        "file": (doc_path.name, content, "application/pdf")
                    },
                    data={
                        "source_id": source.id,
                        "source_name": source.name,
                        "type": source.type.value,
                        "language": source.language,
                        "priority": str(source.priority)
                    },
                    timeout=120.0
                )
                return response.status_code == 200

        except Exception:
            return False

    async def search(
        self,
        query: str,
        knowledge_type: KnowledgeType | None = None,
        limit: int = 10
    ) -> list[dict]:
        """
        Recherche dans la base de connaissances.

        Args:
            query: Requête de recherche
            knowledge_type: Filtrer par type
            limit: Nombre maximum de résultats

        Returns:
            Liste de résultats
        """
        import httpx

        try:
            params = {
                "query": query,
                "limit": limit
            }

            if knowledge_type:
                params["filter"] = f"type:{knowledge_type.value}"

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.archon_url}/search",
                    params=params,
                    timeout=30.0
                )

                if response.status_code == 200:
                    return response.json().get("results", [])

        except Exception:
            pass

        return []

    def get_sources_by_type(self, knowledge_type: KnowledgeType) -> list[KnowledgeSource]:
        """
        Récupère les sources par type.

        Args:
            knowledge_type: Type de connaissance

        Returns:
            Liste de sources
        """
        return [s for s in DZ_KNOWLEDGE_SOURCES if s.type == knowledge_type]

    def get_source(self, source_id: str) -> KnowledgeSource | None:
        """
        Récupère une source par ID.

        Args:
            source_id: ID de la source

        Returns:
            KnowledgeSource ou None
        """
        return next((s for s in DZ_KNOWLEDGE_SOURCES if s.id == source_id), None)


# ============ QUICK REFERENCE DATA ============

# Taux de cotisations CNAS (2024)
CNAS_RATES = {
    "employeur": 0.26,      # 26%
    "salarie": 0.09,        # 9%
    "total": 0.35,          # 35%
    "plafond_mensuel": 48000,  # DZD
}

# Taux TVA
TVA_RATES = {
    "normal": 0.19,         # 19%
    "reduit": 0.09,         # 9%
    "exonere": 0.0,         # 0%
}

# Barème IRG (Impôt sur le Revenu Global) 2024
IRG_BAREME = [
    {"min": 0, "max": 240000, "taux": 0.0},
    {"min": 240001, "max": 480000, "taux": 0.23},
    {"min": 480001, "max": 960000, "taux": 0.27},
    {"min": 960001, "max": 1920000, "taux": 0.30},
    {"min": 1920001, "max": 3840000, "taux": 0.33},
    {"min": 3840001, "max": float("inf"), "taux": 0.35},
]

# Taux IBS (Impôt sur les Bénéfices des Sociétés)
IBS_RATES = {
    "production": 0.19,     # 19% - activités de production
    "btph": 0.23,           # 23% - bâtiment et travaux publics
    "autres": 0.26,         # 26% - autres activités
}

# Wilayas d'Algérie (codes)
WILAYAS = {
    "01": "Adrar",
    "02": "Chlef",
    "03": "Laghouat",
    "04": "Oum El Bouaghi",
    "05": "Batna",
    "06": "Béjaïa",
    "07": "Biskra",
    "08": "Béchar",
    "09": "Blida",
    "10": "Bouira",
    "11": "Tamanrasset",
    "12": "Tébessa",
    "13": "Tlemcen",
    "14": "Tiaret",
    "15": "Tizi Ouzou",
    "16": "Alger",
    "17": "Djelfa",
    "18": "Jijel",
    "19": "Sétif",
    "20": "Saïda",
    "21": "Skikda",
    "22": "Sidi Bel Abbès",
    "23": "Annaba",
    "24": "Guelma",
    "25": "Constantine",
    "26": "Médéa",
    "27": "Mostaganem",
    "28": "M'Sila",
    "29": "Mascara",
    "30": "Ouargla",
    "31": "Oran",
    "32": "El Bayadh",
    "33": "Illizi",
    "34": "Bordj Bou Arréridj",
    "35": "Boumerdès",
    "36": "El Tarf",
    "37": "Tindouf",
    "38": "Tissemsilt",
    "39": "El Oued",
    "40": "Khenchela",
    "41": "Souk Ahras",
    "42": "Tipaza",
    "43": "Mila",
    "44": "Aïn Defla",
    "45": "Naâma",
    "46": "Aïn Témouchent",
    "47": "Ghardaïa",
    "48": "Relizane",
    # Nouvelles wilayas (2019)
    "49": "El M'Ghair",
    "50": "El Menia",
    "51": "Ouled Djellal",
    "52": "Bordj Badji Mokhtar",
    "53": "Béni Abbès",
    "54": "Timimoun",
    "55": "Touggourt",
    "56": "Djanet",
    "57": "In Salah",
    "58": "In Guezzam",
}


def get_wilaya_name(code: str) -> str:
    """Récupère le nom d'une wilaya par code"""
    return WILAYAS.get(code.zfill(2), "Inconnue")


def calculate_irg(revenu_annuel: float) -> float:
    """
    Calcule l'IRG sur un revenu annuel.

    Args:
        revenu_annuel: Revenu imposable annuel en DZD

    Returns:
        Montant IRG
    """
    irg = 0.0
    revenu_restant = revenu_annuel

    for tranche in IRG_BAREME:
        if revenu_restant <= 0:
            break

        tranche_max = tranche["max"] - tranche["min"]
        revenu_tranche = min(revenu_restant, tranche_max)

        irg += revenu_tranche * tranche["taux"]
        revenu_restant -= revenu_tranche

    return irg


def calculate_cnas(salaire_brut: float) -> dict:
    """
    Calcule les cotisations CNAS.

    Args:
        salaire_brut: Salaire brut mensuel en DZD

    Returns:
        Dict avec cotisations employeur et salarié
    """
    return {
        "employeur": salaire_brut * CNAS_RATES["employeur"],
        "salarie": salaire_brut * CNAS_RATES["salarie"],
        "total": salaire_brut * CNAS_RATES["total"],
    }
