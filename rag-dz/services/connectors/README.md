# DZ-Connectors

## 🇩🇿 Module d'ingestion automatique de données algériennes

Ce module permet à IAFactory Algeria de collecter, traiter et indexer automatiquement les données officielles algériennes pour alimenter le RAG.

## 📁 Structure

```
dz-connectors/
├── backend/
│   ├── main.py          # API FastAPI
│   ├── scrapers.py      # Scrapers pour chaque source
│   ├── services.py      # Chunker, Embeddings, Database
│   └── requirements.txt
├── n8n/
│   └── workflows.json   # Workflows n8n automatisés
└── README.md
```

## 🔌 Sources de données

| Source | ID | Fréquence | Type de données |
|--------|-----|-----------|-----------------|
| Journal Officiel (JORADP) | `DZ_JO` | Hebdomadaire | Lois, décrets, arrêtés |
| Direction Générale des Impôts | `DZ_DGI` | Hebdomadaire | Barèmes, circulaires fiscales |
| Office National des Statistiques | `DZ_ONS` | Mensuel | Rapports, indicateurs économiques |
| Banque d'Algérie | `DZ_BANK` | Hebdomadaire | Taux, circulaires bancaires |
| Douanes Algériennes | `DZ_DOUANE` | Hebdomadaire | Nomenclatures, tarifs |
| ANEM (Emploi) | `DZ_ANEM` | Hebdomadaire | Procédures, réglementations |
| ANDI (Investissement) | `DZ_ANDI` | Mensuel | Guides, avantages fiscaux |
| Actualités DZ | `DZ_NEWS` | Quotidien | APS, TSA, El Moudjahid |

## 🚀 Installation

### Prérequis

- Python 3.11+
- PostgreSQL avec extension pgvector
- Qdrant (base vectorielle)
- n8n (optionnel, pour automatisation)

### Installation locale

```bash
cd dz-connectors/backend
pip install -r requirements.txt

# Variables d'environnement
export DATABASE_URL="postgresql://user:pass@localhost:5432/iafactory"
export QDRANT_HOST="localhost"
export QDRANT_PORT="6333"
export GROQ_API_KEY="your-key"

# Lancer l'API
uvicorn main:app --host 0.0.0.0 --port 8195
```

### Avec Docker

```bash
docker build -t iaf-dz-connectors .
docker run -d \
  --name iaf-dz-connectors-prod \
  --network iaf-prod-network \
  -p 127.0.0.1:8195:8195 \
  -e DATABASE_URL="..." \
  -e QDRANT_HOST="..." \
  iaf-dz-connectors
```

## 📡 API Endpoints

### Ingestion

```bash
# Ingérer un document
POST /api/ingest
{
  "title": "Loi de Finances 2024",
  "text": "Article 1: ...",
  "source_url": "https://...",
  "source_name": "DZ_JO",
  "type": "law",
  "date": "2024-01-01"
}

# Ingestion en lot
POST /api/ingest/batch
{
  "documents": [...]
}
```

### Scraping

```bash
# Lancer le scraping d'une source
POST /api/scrape/DZ_JO

# Scraper toutes les sources
POST /api/scrape/all
```

### Statistiques

```bash
# Stats globales
GET /api/stats

# Liste des sources
GET /api/sources

# Recherche
GET /api/search?query=loi+de+finances&source=DZ_JO&limit=10
```

## ⚡ Automatisation n8n

Les workflows n8n sont configurés pour:

| Workflow | Fréquence | Horaire |
|----------|-----------|---------|
| JORADP | Hebdomadaire | Lundi 6h |
| DGI | Hebdomadaire | Mardi 7h |
| News | Quotidien | 8h |
| ONS | Mensuel | 1er du mois 9h |
| Banque d'Algérie | Hebdomadaire | Mercredi 10h |

### Importer les workflows

1. Aller dans n8n → Settings → Import Workflow
2. Importer `n8n/workflows.json`
3. Activer les workflows

## 📊 Format des documents

Chaque document ingéré est normalisé:

```json
{
  "title": "string",
  "text": "string (contenu extrait)",
  "source_url": "string",
  "source_name": "DZ_JO | DZ_DGI | DZ_ONS | ...",
  "type": "law | decree | tax | procedure | news | statistic | circular | report",
  "date": "YYYY-MM-DD",
  "country": "DZ" (ajouté automatiquement)
}
```

## 🔧 Pipeline de traitement

1. **Collecte** - Scraper récupère HTML/PDF
2. **Extraction** - pypdf pour PDF, BeautifulSoup pour HTML
3. **Nettoyage** - Suppression headers, numéros de page
4. **Chunking** - Découpage en morceaux de ~500 tokens
5. **Embedding** - Génération vecteurs via GROQ/fallback
6. **Stockage** - Qdrant (vecteurs) + PostgreSQL (métadonnées)

## 🛡️ Bonnes pratiques

- Respecter les délais entre requêtes (2-3 secondes)
- User-Agent réaliste pour éviter les blocages
- Retry automatique en cas d'erreur 500
- Log de toutes les opérations

## 📈 Monitoring

Dashboard disponible à `/data-dz/`:
- Nombre de documents par source
- Dernières ingestions
- Recherche rapide
- Lancement manuel des scrapers

## 🐛 Troubleshooting

### PDF protégé
Certains PDFs du JORADP sont protégés. Le scraper utilise pypdf avec fallback OCR.

### Timeout
Augmenter le timeout pour les gros PDFs:
```python
async with self.session.get(url, timeout=120) as response:
```

### Rate limiting
Ajouter un délai plus long:
```python
await self.delay(5)  # 5 secondes entre requêtes
```

## 📝 Licence

Propriétaire - IAFactory Algeria
