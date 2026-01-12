# 📊 Data DZ Dashboard - RAG Algérie Monitoring

**Module 7** - Tableau de bord de monitoring et pilotage du RAG Algérie.

## 🎯 Fonctionnalités

- **Visualisation des documents indexés** : sources, volumes, dates
- **Suivi des connecteurs DZ** : succès / erreurs / warnings
- **Fraîcheur des données** : dernières lois, notes DGI, etc.
- **Diagnostics** : détection rapide des problèmes d'ingestion
- **Vue marketing** : stats publiques sur la couverture du RAG

## 🔗 URLs

| Service | URL |
|---------|-----|
| Dashboard UI | https://www.iafactoryalgeria.com/data-dashboard/ |
| API Summary | https://www.iafactoryalgeria.com/api/dz-data/summary |
| API Health | https://www.iafactoryalgeria.com/api/dz-data/health |
| Public Stats | https://www.iafactoryalgeria.com/api/public/dz-data/stats |

## 📊 Sources de données DZ

| Source | Description | Types de documents |
|--------|-------------|-------------------|
| DZ_JO | Journal Officiel | Lois, décrets, circulaires |
| DZ_DGI | Direction Générale des Impôts | Notes fiscales, instructions |
| DZ_ONS | Office National des Statistiques | Statistiques, rapports |
| DZ_DOUANE | Douanes Algériennes | Tarifs, procédures |
| DZ_NEWS | Actualités Économiques | News business |
| DZ_CNRC | Registre du Commerce | Procédures création |
| DZ_CNAS | Sécurité Sociale | Cotisations, prestations |
| DZ_BOAMP | Marchés Publics | Appels d'offres |

## 📚 Endpoints API

### GET /api/dz-data/summary

Résumé global des données indexées.

```bash
curl https://www.iafactoryalgeria.com/api/dz-data/summary
```

Réponse:
```json
{
  "total_documents": 44,
  "total_chunks": 1491,
  "sources_count": 8,
  "by_source": [
    {
      "source_name": "DZ_JO",
      "document_count": 10,
      "chunk_count": 666,
      "last_document_date": "2025-11-17",
      "last_ingested_at": "2025-11-25T22:11:41"
    }
  ],
  "by_type": [
    {"type": "procedure", "document_count": 13},
    {"type": "law", "document_count": 6}
  ],
  "last_runs": [...]
}
```

### GET /api/dz-data/source/{source_name}

Détails d'une source spécifique.

```bash
curl "https://www.iafactoryalgeria.com/api/dz-data/source/DZ_JO?limit=10"
```

Query params:
- `limit` (int, défaut: 50)
- `offset` (int, défaut: 0)
- `doc_type` (string, optionnel)
- `date_from` (ISO date, optionnel)
- `date_to` (ISO date, optionnel)

### GET /api/dz-data/runs

Historique des runs d'ingestion.

```bash
curl "https://www.iafactoryalgeria.com/api/dz-data/runs?limit=20&source_name=DZ_DGI"
```

Query params:
- `source_name` (string, optionnel)
- `status` (success|partial|error, optionnel)
- `limit` (int, défaut: 20)

### GET /api/dz-data/health

Statut de santé des sources.

```bash
curl https://www.iafactoryalgeria.com/api/dz-data/health
```

Réponse:
```json
{
  "overall_status": "healthy",
  "sources": [
    {
      "source_name": "DZ_JO",
      "status": "ok",
      "last_run_at": "2025-11-28T21:11:41",
      "last_run_status": "success",
      "freshness_days": 11,
      "document_count": 10
    }
  ],
  "last_check": "2025-11-28T22:11:57"
}
```

Statuts possibles:
- `ok` : Source à jour, dernier run réussi
- `warning` : Données pas fraîches (>30 jours) ou run partiel
- `error` : Dernier run en erreur

### GET /api/public/dz-data/stats

Stats publiques pour affichage marketing.

```bash
curl https://www.iafactoryalgeria.com/api/public/dz-data/stats
```

## 🔌 Intégration avec les Connecteurs DZ

Les workflows d'ingestion doivent appeler ces endpoints pour enregistrer leurs actions:

### Enregistrer un document indexé

```bash
curl -X POST "https://www.iafactoryalgeria.com/api/dz-data/ingest/document" \
  -H "Content-Type: application/json" \
  -d '{
    "doc_id": "DZ_JO_2024_001",
    "title": "Loi de Finances 2025",
    "source_name": "DZ_JO",
    "doc_type": "law",
    "nb_chunks": 45,
    "source_url": "https://joradp.dz/...",
    "date_document": "2024-12-15"
  }'
```

### Enregistrer un run d'ingestion

```bash
curl -X POST "https://www.iafactoryalgeria.com/api/dz-data/ingest/run" \
  -H "Content-Type: application/json" \
  -d '{
    "source_name": "DZ_JO",
    "run_id": "n8n_run_20251128_001",
    "status": "success",
    "nb_documents": 12,
    "nb_chunks": 450,
    "start_time": "2025-11-28T10:00:00",
    "end_time": "2025-11-28T10:15:32"
  }'
```

## 📦 Modèle de données

### Table `documents_indexed`

| Champ | Type | Description |
|-------|------|-------------|
| id | UUID | Identifiant unique |
| doc_id | string | ID logique du document |
| title | string | Titre du document |
| source_name | string | DZ_JO, DZ_DGI, etc. |
| type | enum | law, tax, procedure, news... |
| source_url | string | URL source originale |
| date_document | date | Date du document |
| date_ingested | datetime | Date d'indexation |
| nb_chunks | int | Nombre de chunks créés |
| status | enum | ok, error, partial |

### Table `ingestion_logs`

| Champ | Type | Description |
|-------|------|-------------|
| id | UUID | Identifiant unique |
| source_name | string | Source concernée |
| run_id | string | ID du run n8n/batch |
| start_time | datetime | Début du run |
| end_time | datetime | Fin du run |
| status | enum | success, partial, error |
| nb_documents | int | Documents traités |
| nb_chunks | int | Chunks créés |
| error_message | string | Message d'erreur si applicable |

## 🐳 Containers Docker

| Container | Port | Description |
|-----------|------|-------------|
| iaf-data-dashboard-prod | 8205 | Backend API FastAPI |
| iaf-data-dashboard-ui-prod | 8206 | Frontend Dashboard |

## 🎨 Interface utilisateur

### Dashboard principal
- **Cartes statistiques** : Total documents, chunks, sources, dernier run
- **Graphiques** : Documents par source (bar), répartition par type (doughnut)
- **Sources DZ** : Grille avec statut santé, fraîcheur, compteurs

### Panneau de détail source
- Tableau des documents avec titre, type, date, chunks, statut
- Lien vers le document source original
- Pagination et filtres

### Historique des runs
- Tableau des derniers runs d'ingestion
- Filtres par source et statut
- Durée, documents traités, erreurs éventuelles

### Exports CSV
- Export des sources
- Export des runs d'ingestion

## 🔐 Sécurité (recommandations production)

- Protéger `/api/dz-data/...` par authentification JWT
- Exposer uniquement `/api/public/dz-data/stats` publiquement
- Rate limiting sur les endpoints d'ingestion
- Indexer les colonnes `source_name`, `date_document`, `date_ingested`

---

## 📞 Support

- **Dashboard:** https://www.iafactoryalgeria.com/data-dashboard/
- **Hub:** https://www.iafactoryalgeria.com/hub/
- **Email:** support@iafactoryalgeria.com

---

© 2025 iaFactory Algeria - Tous droits réservés
