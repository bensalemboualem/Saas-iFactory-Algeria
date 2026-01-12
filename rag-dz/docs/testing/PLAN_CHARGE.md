## Plan de tests de charge (Phase 5)

### 1. Objectifs
- Valider que l’orchestrateur BMAD tient 50 RPS et pic 150 RPS sans erreur.
- Mesurer la latence P95 (<1,2 s) et l’erreur rate (<2 %).
- Vérifier la résilience lorsqu’un orchestrator_state reste bloqué (utilisation des nouveaux endpoints `pending-workflows` + `recover`).

### 2. Scénarios
| Nom | Fichier k6 | Charge | Pré-requis |
| --- | --- | --- | --- |
| `orchestrator-smoke` | `tests/load/k6/orchestrator-smoke.js` | 10 VUs / 1 min | Backend + DB + BMAD simulés |
| `orchestrator-burst` | `tests/load/k6/orchestrator-burst.js` | 0→50 VUs (stages 5 min) | Monitoring actif |
| `orchestrator-regen` | `tests/load/k6/orchestrator-regen.js` | 25 VUs / 10 min + supervision | n8n superviseur actif |

### 3. Exécution
```bash
# Lancer Prometheus/Grafana (profil monitoring Docker)
make start-monitoring

# Exporter les variables (API locale par défaut)
export K6_BASE_URL="http://localhost:8180"
export K6_API_KEY="change-me-in-production"

# Lancer le smoke test
./scripts/load-test.sh orchestrator-smoke

# Ou version PowerShell
pwsh scripts/load-test.ps1 orchestrator-smoke
```

### 4. Collecte des métriques
- `Prometheus` (port 8187) collecte automatiquement `/metrics` du backend (`ENABLE_METRICS=true` déjà activé).
- `Grafana` (port 8188) → dashboard `infrastructure/monitoring/grafana/dashboards/dashboard.yml`.
- Exporter les résultats k6 (`--summary-trend-stats "avg,p(90),p(95),p(99)"`) et joindre à `docs/testing/RESULTATS_CHARGE.md`.

### 5. Critères de passage
- P95 < 1,2 s sur `/api/orchestrator/analyze-readiness`.
- Taux d’erreur HTTP < 2 %.
- Pas de backlog > 5 entrées dans `GET /api/orchestrator/pending-workflows` sur la période.
- Superviseur n8n doit consommer toute orchestration “failed” en < 2 minutes.

### 6. Prochaines étapes
1. Ajouter scénarios burst/regen (nouveaux fichiers k6).
2. Brancher un job GitHub Actions optionnel (`workflow_dispatch`) pour lancer les tests de charge en pré-prod.
3. Exporter les dashboards Grafana (JSON) et les inclure dans `infrastructure/monitoring/grafana/dashboards/`.

