# 🏛️ LLM Council - Multi-AI Deliberation System

## Vue d'ensemble

LLM Council est un système innovant intégré dans IAFactory qui permet de consulter **plusieurs modèles d'IA simultanément** pour obtenir des réponses plus robustes, précises et fiables.

### Pourquoi un "Council" ?

Au lieu de se fier à un seul modèle d'IA (qui peut avoir des biais ou des limitations), le Council:
- ✅ Consulte 3 modèles différents en parallèle
- ✅ Compare leurs réponses et perspectives
- ✅ Synthétise la meilleure réponse possible
- ✅ Permet une validation croisée pour les décisions importantes

## 🏗️ Architecture Technique

### Stack Technologique

**Backend**
- Python 3.11+
- FastAPI (API REST)
- httpx (requêtes async)
- Pydantic (validation)

**Frontend**
- React 18 + TypeScript
- Tailwind CSS
- Lucide Icons
- React Router

**Providers LLM**
- **Claude Sonnet 4** (Anthropic) - Chairman & Member
- **Gemini 1.5 Pro** (Google) - Member
- **Llama 3 8B** (Meta via Ollama) - Member local

### Pipeline en 3 Étapes

```
┌─────────────────────────────────────────────────┐
│              STAGE 1: OPINIONS                  │
│                                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Claude  │  │ Gemini  │  │ Ollama  │        │
│  └────┬────┘  └────┬────┘  └────┬────┘        │
│       │            │            │              │
│       └────────────┴────────────┘              │
│              Opinions collectées                │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│         STAGE 2: REVIEW (optionnel)             │
│                                                 │
│  Chaque modèle évalue les autres sur:          │
│  - Précision factuelle (1-10)                   │
│  - Pertinence (1-10)                            │
│  - Clarté (1-10)                                │
│  - Complétude (1-10)                            │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│         STAGE 3: SYNTHESIS                      │
│                                                 │
│  Chairman (Claude) synthétise:                  │
│  ✓ Intègre les meilleures idées                 │
│  ✓ Résout les contradictions                    │
│  ✓ Fournit une réponse claire                   │
│  ✓ Mentionne les divergences importantes        │
└─────────────────────────────────────────────────┘
```

## 📁 Structure des Fichiers

```
rag-dz/
├── backend/rag-compat/app/
│   ├── modules/council/           # Module Council
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration
│   │   ├── providers.py           # LLM providers
│   │   └── orchestrator.py        # Orchestrateur principal
│   └── routers/
│       └── council.py             # API endpoints
│
├── frontend/archon-ui/src/
│   ├── features/council/          # Interface React
│   │   ├── CouncilInterface.tsx
│   │   └── ResponseTabs.tsx
│   └── pages/
│       └── CouncilPage.tsx
│
├── docs/
│   ├── COUNCIL_README.md          # Ce fichier
│   └── COUNCIL_QUICK_START.md     # Guide démarrage rapide
│
└── test-council.py                # Suite de tests
```

## 🚀 Installation

### Prérequis

- Docker & Docker Compose
- Python 3.11+ (pour les tests)
- Clés API: Anthropic, Google

### Étapes d'installation

1. **Configurer les variables d'environnement**

```bash
cp .env.example .env.local
```

Éditer `.env.local`:
```bash
# LLM Council Configuration
ANTHROPIC_API_KEY=sk-ant-xxxxx
GOOGLE_GENERATIVE_AI_API_KEY=AIzaSy-xxxxx
OLLAMA_BASE_URL=http://iafactory-ollama:11434

COUNCIL_ENABLE_REVIEW=false
COUNCIL_CHAIRMAN=claude
```

2. **Démarrer les services**

```bash
# Démarrer toute la stack
docker-compose up -d

# Ou uniquement Council + dépendances
docker-compose up -d iafactory-backend iafactory-ollama iafactory-hub
```

3. **Télécharger le modèle Ollama**

```bash
docker exec -it iaf-dz-ollama ollama pull llama3:8b
```

4. **Vérifier l'installation**

```bash
# Via le script de test
python test-council.py

# Ou via curl
curl http://localhost:8180/api/council/health
```

## 📖 Utilisation

### Interface Web

1. Accéder à http://localhost:8182
2. Cliquer sur "LLM Council" dans le menu
3. Poser une question
4. Choisir d'activer ou non la revue croisée
5. Consulter la réponse synthétisée et les opinions individuelles

### API REST

#### Interroger le Council

```bash
POST /api/council/query
Content-Type: application/json

{
  "query": "Comment sécuriser une API REST ?",
  "context": "Pour une application bancaire en Algérie",
  "enable_review": false,
  "council_members": ["claude", "gemini", "ollama"],
  "chairman": "claude"
}
```

Réponse:
```json
{
  "final_response": "Synthèse complète...",
  "opinions": {
    "claude": "Opinion de Claude...",
    "gemini": "Opinion de Gemini...",
    "ollama": "Opinion de Llama 3..."
  },
  "rankings": null,
  "metadata": {
    "execution_time": 18.5,
    "council_members": ["claude", "gemini", "ollama"],
    "chairman": "claude",
    "review_enabled": false
  }
}
```

#### Lister les providers

```bash
GET /api/council/providers
```

#### Tester la connectivité

```bash
POST /api/council/test
```

#### Configuration actuelle

```bash
GET /api/council/config
```

## 🎯 Cas d'Usage

### ✅ Situations Idéales

| Cas d'usage | Pourquoi Council | Mode recommandé |
|-------------|------------------|-----------------|
| **Décisions stratégiques** | Validation croisée nécessaire | Premium (avec review) |
| **Architecture technique** | Multiples perspectives utiles | Standard |
| **Analyses juridiques** | Précision critique | Premium |
| **Études de marché** | Synthèse de données complexes | Standard |
| **Audit de sécurité** | Identification exhaustive des risques | Premium |
| **Documentation technique** | Clarté et complétude requises | Standard |

### ❌ Situations Non Adaptées

- Questions simples et factuelles ("Quelle heure est-il ?")
- Génération créative (articles, code)
- Besoins temps réel (< 5 secondes)
- Traductions simples
- Calculs mathématiques

## ⚙️ Configuration Avancée

### Personnaliser le Council

**Changer les membres par défaut:**
```python
# backend/rag-compat/app/modules/council/config.py
DEFAULT_COUNCIL: List[str] = ["claude", "ollama"]  # Seulement 2 membres
```

**Changer le chairman:**
```bash
# .env.local
COUNCIL_CHAIRMAN=gemini
```

**Ajuster les timeouts:**
```python
# config.py
STAGE1_TIMEOUT: int = 60  # Au lieu de 30
STAGE2_TIMEOUT: int = 40  # Au lieu de 20
STAGE3_TIMEOUT: int = 30  # Au lieu de 15
```

### Ajouter un nouveau provider

1. **Créer la classe provider** dans `providers.py`:

```python
class NewProvider(LLMProvider):
    def __init__(self):
        self.api_key = os.getenv("NEW_PROVIDER_API_KEY")
        self.base_url = "https://api.newprovider.com"

    async def generate(self, prompt: str, system: str = None) -> str:
        # Implémentation...
        pass
```

2. **Ajouter à la config** dans `config.py`:

```python
PROVIDERS: Dict[str, Dict[str, Any]] = {
    # ... existing providers
    "newprovider": {
        "name": "New Provider",
        "model": "model-name",
        "role": "member",
        "cost_per_1k": 0.002,
        "enabled": True
    }
}
```

3. **Enregistrer dans la factory**:

```python
def get_provider(name: str) -> LLMProvider:
    providers = {
        # ... existing
        "newprovider": NewProvider
    }
    return providers[name]()
```

## 📊 Monitoring & Performance

### Métriques clés

- **Temps d'exécution moyen**: 15-30s (standard), 30-60s (premium)
- **Taux de succès**: > 95%
- **Coût par requête**: $0.015 (standard), $0.030 (premium)

### Logs

```bash
# Logs backend
docker logs -f iaf-dz-backend | grep Council

# Logs spécifiques
docker logs -f iaf-dz-backend | grep "council.orchestrator"
```

### Debugging

Activer le mode debug:
```python
# backend/rag-compat/app/main.py
logging.basicConfig(level=logging.DEBUG)
```

## 🔒 Sécurité

### Bonnes pratiques

1. **Ne jamais exposer les clés API**
   - Utiliser `.env.local` (git-ignored)
   - Rotation régulière des clés

2. **Rate limiting**
   - Déjà implémenté dans le backend
   - Configurable via `RATE_LIMIT_PER_MINUTE`

3. **Validation des inputs**
   - Longueur max des prompts: 10,000 caractères
   - Sanitization automatique

4. **Anonymisation (optionnel)**
   - Active par défaut dans la review
   - Évite les biais liés aux noms de modèles

## 💰 Coûts & Tarification

### Coûts par Provider (par 1K tokens)

| Provider | Input | Output | Moyenne par requête |
|----------|-------|--------|---------------------|
| Claude Sonnet 4 | $0.003 | $0.015 | ~$0.010 |
| Gemini 1.5 Pro | $0.00125 | $0.005 | ~$0.004 |
| Ollama (local) | $0.000 | $0.000 | $0.000 |

### Estimation par requête

**Mode Standard (sans review):**
- 3 modèles × ~500 tokens input = 1,500 tokens
- 3 modèles × ~1,000 tokens output = 3,000 tokens
- 1 synthèse × ~1,500 tokens = 1,500 tokens
- **Total estimé: $0.015 (1.5¢)**

**Mode Premium (avec review):**
- Standard + Review (6 évaluations supplémentaires)
- **Total estimé: $0.030 (3¢)**

### Tarification client suggérée (Algérie)

| Mode | Latence | Prix DZD | Prix EUR | Usage |
|------|---------|----------|----------|-------|
| Standard | 15-30s | 200 DZD | ~1.40 EUR | Questions complexes |
| Premium | 30-60s | 400 DZD | ~2.80 EUR | Décisions critiques |

## 🧪 Tests

### Suite de tests automatisée

```bash
python test-council.py
```

Tests inclus:
1. Health check du service
2. Liste des providers
3. Connectivité de chaque provider
4. Requête simple
5. Requête avec review (optionnel)
6. Vérification de la config

### Tests manuels

```bash
# Test endpoint par endpoint
curl http://localhost:8180/api/council/health
curl http://localhost:8180/api/council/providers
curl -X POST http://localhost:8180/api/council/test
```

## 🐛 Troubleshooting

Voir [COUNCIL_QUICK_START.md](./COUNCIL_QUICK_START.md#-dépannage)

## 📚 Références

- **Claude API**: https://docs.anthropic.com/claude/reference/
- **Gemini API**: https://ai.google.dev/docs
- **Ollama**: https://ollama.com/library/llama3

## 🎯 Roadmap

### Phase 1 (Actuelle - Décembre 2024)
- [x] Implémentation core
- [x] 3 providers (Claude, Gemini, Ollama)
- [x] Interface web basique
- [x] Tests automatisés

### Phase 2 (Janvier 2025)
- [ ] Cache intelligent (éviter doublons)
- [ ] Métriques Prometheus
- [ ] Dashboard analytics
- [ ] API webhooks pour notifications

### Phase 3 (Février 2025)
- [ ] Councils spécialisés (juridique, tech, médical)
- [ ] Support streaming (réponses progressives)
- [ ] Multi-langues (AR, FR, EN)
- [ ] Export PDF des délibérations

## 🤝 Contribution

Pour contribuer au développement du Council:

1. Créer une branche: `git checkout -b feature/council-xxx`
2. Coder + tester: `python test-council.py`
3. Commit: `git commit -m "feat(council): xxx"`
4. Push & PR

## 📄 Licence

Propriétaire - IAFactory Algeria © 2024

---

**Besoin d'aide ?**
- Documentation: [COUNCIL_QUICK_START.md](./COUNCIL_QUICK_START.md)
- Issues: Contacter l'équipe dev
- Démo: Préparation pour Algérie Télécom (6 décembre)
