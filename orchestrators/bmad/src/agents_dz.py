"""
Custom Agents IA Factory - Agents spécifiques pour l'Algérie
"""

from typing import Any
from pydantic import BaseModel

from .runner import BMADRunner, AgentResult


# ============ PROMPTS DES AGENTS CUSTOM ============

CONFORMITY_DZ_AGENT = """
# Agent de Conformité Algérie

Tu es un expert en conformité réglementaire pour l'Algérie. Tu dois vérifier que les solutions proposées respectent:

## Réglementations à vérifier

### Paiement
- Utilisation obligatoire de solutions de paiement locales (Chargily, CIB, EDAHABIA)
- Pas de Stripe, PayPal ou autres solutions internationales non autorisées
- Monnaie: Dinar Algérien (DZD) uniquement

### Protection des données
- Hébergement des données en Algérie ou conformité avec la réglementation locale
- Respect de la loi 18-07 sur la protection des données personnelles
- Consentement explicite pour la collecte de données

### Commerce électronique
- Conformité avec le décret 05-468 sur le commerce électronique
- Mentions légales obligatoires
- Registre du commerce valide

### Secteur spécifique
- CNAS/CASNOS pour les applications RH
- Sonelgaz/SEAAL pour les services publics
- Banque d'Algérie pour les services financiers

## Format de réponse

Pour chaque point vérifié, indique:
1. ✅ Conforme / ⚠️ À vérifier / ❌ Non conforme
2. Explication
3. Action corrective si nécessaire
"""

DARIJA_CONTENT_AGENT = """
# Agent de Contenu Darija

Tu es un expert en localisation de contenu pour l'Algérie. Tu dois adapter le contenu en Darija algérien.

## Règles de localisation

### Langue
- Utiliser le Darija algérien authentique
- Éviter les expressions du Moyen-Orient ou du Maroc
- Mélanger arabe dialectal et français quand approprié (code-switching naturel)

### Expressions courantes
- "Wesh" au lieu de "Shno" ou "Eish"
- "Kayen" au lieu de "Fi"
- "Bezaf" pour "beaucoup"
- Intégrer des expressions locales: "Inchallah", "Hamdullah", "Mazel"

### Contexte culturel
- Références aux villes algériennes (Alger, Oran, Constantine...)
- Fêtes locales (Yennayer, Aid...)
- Habitudes de consommation locales

### Ton
- Chaleureux et familier
- Respectueux (vouvoiement pour les aînés)
- Humour subtil quand approprié

## Format de sortie

Fournis:
1. Version originale
2. Version Darija
3. Notes de localisation (expressions adaptées, contexte culturel)
"""

GOV_INTEGRATION_AGENT = """
# Agent d'Intégration GOV Algérie

Tu es un expert en intégration avec les systèmes gouvernementaux algériens.

## Systèmes GOV à intégrer

### CNAS (Caisse Nationale d'Assurances Sociales)
- Vérification des affiliés
- Attestations d'affiliation
- Déclarations sociales

### CASNOS (Caisse Nationale de Sécurité Sociale des Non-Salariés)
- Gestion des travailleurs indépendants
- Cotisations et attestations

### CNRC (Centre National du Registre du Commerce)
- Vérification registre du commerce
- Extrait de registre

### DGI (Direction Générale des Impôts)
- NIF (Numéro d'Identification Fiscale)
- Déclarations fiscales
- Attestations fiscales

### Sonelgaz
- Factures électricité/gaz
- Relevés de compteur
- Paiement en ligne

### Algérie Poste / BADR / BNA
- Services bancaires
- Paiement CIB
- Virement CNEP

## Spécifications techniques

Pour chaque intégration, fournis:
1. Endpoints API (si disponibles)
2. Format des données (XML/JSON)
3. Authentification requise
4. Flux de données
5. Gestion des erreurs
6. Fallback manuel si API indisponible
"""

CHARGILY_PAYMENT_AGENT = """
# Agent Paiement Chargily

Tu es un expert en intégration du système de paiement Chargily pour l'Algérie.

## À propos de Chargily
- Solution de paiement algérienne
- Supporte CIB et EDAHABIA
- API REST moderne

## Intégration

### Configuration
```python
CHARGILY_API_KEY = os.getenv("CHARGILY_API_KEY")
CHARGILY_SECRET = os.getenv("CHARGILY_SECRET_KEY")
CHARGILY_URL = "https://pay.chargily.com/api/v2"
```

### Endpoints principaux
- POST /checkouts - Créer un paiement
- GET /checkouts/{id} - Statut paiement
- POST /webhooks - Notifications

### Montants
- Toujours en DZD (Dinar Algérien)
- Minimum: 75 DZD
- Pas de centimes

### Webhooks
- Vérifier la signature
- Confirmer la réception (200 OK)
- Gérer les retries

## Bonnes pratiques
1. Toujours utiliser HTTPS
2. Stocker les transactions en base
3. Implémenter les retries
4. Logger toutes les transactions
5. Avoir un fallback manuel
"""

# ============ REGISTRATION ============

CUSTOM_AGENTS = {
    "conformity-dz": CONFORMITY_DZ_AGENT,
    "darija-content": DARIJA_CONTENT_AGENT,
    "gov-integration": GOV_INTEGRATION_AGENT,
    "chargily-payment": CHARGILY_PAYMENT_AGENT,
}


class CustomAgentInfo(BaseModel):
    """Information sur un agent custom"""
    name: str
    description: str
    category: str
    tags: list[str]


CUSTOM_AGENTS_INFO: dict[str, CustomAgentInfo] = {
    "conformity-dz": CustomAgentInfo(
        name="Conformity DZ Agent",
        description="Vérifie la conformité réglementaire pour l'Algérie",
        category="compliance",
        tags=["algérie", "conformité", "réglementation", "paiement"]
    ),
    "darija-content": CustomAgentInfo(
        name="Darija Content Agent",
        description="Adapte le contenu en Darija algérien",
        category="localization",
        tags=["algérie", "darija", "localisation", "contenu"]
    ),
    "gov-integration": CustomAgentInfo(
        name="GOV Integration Agent",
        description="Expert en intégration avec les systèmes gouvernementaux algériens",
        category="integration",
        tags=["algérie", "gouvernement", "CNAS", "CNRC", "Sonelgaz"]
    ),
    "chargily-payment": CustomAgentInfo(
        name="Chargily Payment Agent",
        description="Expert en intégration du paiement Chargily",
        category="payment",
        tags=["algérie", "paiement", "Chargily", "CIB", "EDAHABIA"]
    ),
}


def register_dz_agents(runner: BMADRunner) -> None:
    """
    Enregistre tous les agents custom IA Factory dans le runner.

    Args:
        runner: Instance du BMADRunner
    """
    for name, prompt in CUSTOM_AGENTS.items():
        runner.register_custom_agent(name, prompt)


def get_dz_agent_info(agent_name: str) -> CustomAgentInfo | None:
    """Récupère les infos d'un agent custom"""
    return CUSTOM_AGENTS_INFO.get(agent_name)


def list_dz_agents() -> list[CustomAgentInfo]:
    """Liste tous les agents custom disponibles"""
    return list(CUSTOM_AGENTS_INFO.values())


# ============ CONVENIENCE FUNCTIONS ============

async def check_dz_conformity(
    runner: BMADRunner,
    solution_description: str
) -> AgentResult:
    """
    Vérifie la conformité d'une solution pour l'Algérie.

    Args:
        runner: BMADRunner avec agents enregistrés
        solution_description: Description de la solution à vérifier

    Returns:
        Résultat de l'analyse de conformité
    """
    register_dz_agents(runner)
    return await runner.run_agent(
        "conformity-dz",
        f"Vérifie la conformité de cette solution pour l'Algérie:\n\n{solution_description}"
    )


async def localize_to_darija(
    runner: BMADRunner,
    content: str,
    context: str | None = None
) -> AgentResult:
    """
    Localise du contenu en Darija algérien.

    Args:
        runner: BMADRunner avec agents enregistrés
        content: Contenu à localiser
        context: Contexte optionnel

    Returns:
        Contenu localisé
    """
    register_dz_agents(runner)
    task = f"Localise ce contenu en Darija algérien:\n\n{content}"
    if context:
        task += f"\n\nContexte: {context}"

    return await runner.run_agent("darija-content", task)


async def design_gov_integration(
    runner: BMADRunner,
    system: str,
    requirements: str
) -> AgentResult:
    """
    Conçoit une intégration avec un système GOV algérien.

    Args:
        runner: BMADRunner avec agents enregistrés
        system: Système cible (CNAS, CNRC, Sonelgaz, etc.)
        requirements: Besoins d'intégration

    Returns:
        Spécifications d'intégration
    """
    register_dz_agents(runner)
    return await runner.run_agent(
        "gov-integration",
        f"Conçois l'intégration avec {system}:\n\n{requirements}"
    )
