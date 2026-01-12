## Orchestration n8n - Phase 4

### Workflows actifs
- `workflow_email_auto.json`
- `workflow_nouveau_rdv.json`
- `workflow_rappel_rdv.json`
- `workflow_superviseur_orchestrateur.json` *(nouveau superviseur automatique)*

### Secrets requis
| Secret | Description | Où le définir |
| --- | --- | --- |
| `API_KEY` | Clef API backend pour `/api/orchestrator/*` | `.env.local` + variables n8n |
| `BACKEND_URL` | URL interne FastAPI (docker: `http://iafactory-backend:8180`) | Variables globales n8n |
| `IMAP_CONFIG`, `SMTP_*` | Boîte email et envoi auto | Credentials n8n |
| `SLACK_CHANNEL`, `slack-credentials` | Notifications supervision | Credentials n8n |
| `TWILIO_*` | SMS rappels RDV | Credentials n8n |

### Plan de reprise
1. Le superviseur exécute `GET /api/orchestrator/pending-workflows` toutes les 5 min.
2. Les états `failed` ou âgés de >15 min sont automatiquement relancés via `POST /api/orchestrator/pending-workflows/{id}/recover`.
3. Les orchestrations non prêtes + signaux manquants sont escaladées sur Slack (`#ops-ragdz` par défaut).
4. En cas d’incident complet, importer à nouveau les workflows via **Settings → Workflow Import** ou monter le dossier `infrastructure/n8n/workflows` en lecture seule (déjà fait par Docker Compose).

### Commandes utiles
```bash
# Démarrer n8n + workflows (profil par défaut)
docker compose up -d iafactory-n8n

# Vérifier la santé de l’API orchestrateur
curl -H "X-API-Key: $API_KEY" http://localhost:8180/api/orchestrator/health
```

