# PRP-006: IA Factory Algérie Adaptation

> **Priorité**: P0  
> **Effort**: 6-8 heures  
> **Dépendances**: PRP-005

---

## Objectif

Adapter Nexus pour le marché algérien: Chargily, Darija, APIs GOV.

---

## Tâches

### T1: Chargily Integration (2h)

Créer `orchestrators/shared/chargily.py`:

```python
import httpx
from pydantic import BaseModel

class ChargilyPayment(BaseModel):
    amount: int  # En centimes DZD
    currency: str = "DZD"
    client_name: str
    client_email: str
    description: str
    webhook_url: str

class ChargilyService:
    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = "https://pay.chargily.net/api/v2"
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {api_key}"}
        )
    
    async def create_checkout(self, payment: ChargilyPayment) -> dict:
        response = await self.client.post("/checkouts", json=payment.model_dump())
        return response.json()
    
    async def verify_webhook(self, signature: str, payload: bytes) -> bool:
        import hmac
        import hashlib
        expected = hmac.new(
            self.secret_key.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected)
    
    async def get_payment(self, payment_id: str) -> dict:
        response = await self.client.get(f"/payments/{payment_id}")
        return response.json()
```

**Validation**: Checkout créé, webhook vérifié.

---

### T2: Darija Support (1.5h)

Créer support multi-langue avec Darija:

```python
# i18n/darija/common.json
{
    "welcome": "Marhba bik",
    "login": "Dkhol",
    "logout": "Khrej",
    "dashboard": "Tableau de bord",
    "invoices": "Factures",
    "payment": "Khlass",
    "error": "Kayn mochkil",
    "success": "Temmam",
    "loading": "Stenna..."
}

# Service de traduction
class DarijaService:
    def __init__(self, translations_path: str):
        self.translations = self._load_translations(translations_path)
    
    def translate(self, key: str, lang: str = "darija") -> str:
        return self.translations.get(lang, {}).get(key, key)
    
    async def generate_darija_content(self, text_fr: str) -> str:
        # Use LLM to translate to Darija
        # With context about Algerian dialect
        pass
```

**Validation**: Traductions Darija fonctionnelles.

---

### T3: GOV Agents Completion (2h)

Compléter les parsers des agents GOV existants:

```python
# agents/gov/cnas.py - Compléter les parsers

class CNASParser:
    async def parse_attestation(self, html: str) -> dict:
        # Parser spécifique pour les attestations CNAS
        pass
    
    async def parse_historique(self, html: str) -> list[dict]:
        # Parser pour l'historique des cotisations
        pass
    
    async def parse_carte_chifa(self, html: str) -> dict:
        # Parser pour les infos carte Chifa
        pass

# agents/gov/sonelgaz.py - Compléter les parsers

class SonelgazParser:
    async def parse_facture(self, html: str) -> dict:
        # Parser spécifique pour les factures
        pass
    
    async def parse_consommation(self, html: str) -> list[dict]:
        # Parser pour l'historique de consommation
        pass
```

**Validation**: Parsers extraient les données correctement.

---

### T4: Knowledge Base DZ (1h)

Pré-indexer les réglementations algériennes:

```python
DZ_KNOWLEDGE_SOURCES = [
    {"url": "https://www.mfdgi.gov.dz", "type": "fiscal"},
    {"url": "https://www.cnas.dz", "type": "social"},
    {"url": "https://www.cnrc.dz", "type": "commerce"},
    {"doc": "PCN_Algerie.pdf", "type": "accounting"},
    {"doc": "Code_Commerce_DZ.pdf", "type": "legal"},
    {"doc": "Code_Travail_DZ.pdf", "type": "labor"},
]

async def index_dz_knowledge(archon: ArchonBridge):
    for source in DZ_KNOWLEDGE_SOURCES:
        if "url" in source:
            await archon.crawl_url(source["url"], metadata={"type": source["type"]})
        else:
            content = Path(f"docs/dz/{source['doc']}").read_bytes()
            await archon.ingest_document(content, metadata={"type": source["type"]})
```

**Validation**: KB contient les réglementations DZ.

---

### T5: Credit System Integration (1h)

Intégrer le système de crédits existant:

```python
class CreditSystem:
    # Rates par type d'opération
    RATES = {
        "chat_message": 1,
        "code_generation": 5,
        "image_generation": 20,
        "video_generation": 100,
        "gov_agent_call": 3,
    }
    
    async def check_balance(self, user_id: str) -> int:
        # Via Supabase
        pass
    
    async def deduct(self, user_id: str, operation: str, amount: int = None) -> bool:
        amount = amount or self.RATES.get(operation, 1)
        # Déduire et logger
        pass
    
    async def add_credits(self, user_id: str, amount: int, source: str):
        # Chargily webhook → add credits
        pass
```

**Validation**: Crédits déduits correctement.

---

### T6: Conformity Checks (30min)

Implémenter les checks de conformité:

```python
class ConformityChecker:
    RULES = {
        "chargily_only": lambda code: "stripe" not in code.lower(),
        "rls_enabled": lambda code: "ENABLE ROW LEVEL SECURITY" in code,
        "tenant_via_jwt": lambda code: "X-Tenant-ID" not in code,
        "i18n_required": lambda code: any(lang in code for lang in ["fr", "ar", "darija"]),
    }
    
    def check(self, code: str) -> list[str]:
        violations = []
        for rule_name, check in self.RULES.items():
            if not check(code):
                violations.append(rule_name)
        return violations
```

**Validation**: Violations détectées correctement.

---

### T7: Tests End-to-End (30min)

Tests complets du flux IA Factory.

**Validation**: E2E tests passent.

---

## Critères de Complétion

- [ ] T1: Chargily fonctionnel
- [ ] T2: Darija support
- [ ] T3: GOV parsers complets
- [ ] T4: KB DZ indexée
- [ ] T5: Credit system
- [ ] T6: Conformity checks
- [ ] T7: E2E tests

---

## Projet Complété! 🎉

Après PRP-006, le projet Nexus AI Platform pour IA Factory Algérie est opérationnel.
