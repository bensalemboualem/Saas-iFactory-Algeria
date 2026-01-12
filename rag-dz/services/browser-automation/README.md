# Browser Automation - IA Factory Algeria

Module d'automatisation navigateur pour services algériens.

## Stack

| Composant | Description | Coût |
|-----------|-------------|------|
| Browser-Use | Automatisation navigateur IA | Gratuit |
| Ollama | LLM local | Gratuit |
| Qwen2.5:7b | Modèle IA | Gratuit |
| FastAPI | API REST | Gratuit |

**Coût total: $0/mois** (100% local)

## Services Supportés

### Sonelgaz (Électricité/Gaz)
- `get_factures` - Récupérer les factures
- `get_consommation` - Historique consommation
- `payer_facture` - Initier paiement

### CNAS (Sécurité Sociale)
- `get_attestation` - Attestation d'affiliation
- `get_historique` - Historique cotisations
- `verifier_droits` - Droits ouverts
- `get_carte_chifa` - Infos carte Chifa

## Démarrage Rapide

### 1. Avec Docker (Recommandé)

```bash
# Démarrer Ollama + Service
docker-compose up -d

# Télécharger le modèle Qwen2.5
docker exec -it iaf-ollama ollama pull qwen2.5:7b

# Vérifier
curl http://localhost:8100/health
```

### 2. Sans Docker (Local)

```bash
# Installer Ollama
# Windows: https://ollama.ai/download
# Linux: curl -fsSL https://ollama.ai/install.sh | sh

# Télécharger le modèle
ollama pull qwen2.5:7b

# Installer dépendances
pip install -r requirements.txt
playwright install chromium

# Lancer
python main.py
```

## API Endpoints

### Health Check
```bash
GET http://localhost:8100/health
```

### Liste Services
```bash
GET http://localhost:8100/services
```

### Sonelgaz - Factures
```bash
POST http://localhost:8100/sonelgaz
Content-Type: application/json

{
  "reference_client": "123456789",
  "action": "get_factures"
}
```

### CNAS - Attestation
```bash
POST http://localhost:8100/cnas
Content-Type: application/json

{
  "numero_securite_sociale": "1234567890123",
  "action": "get_attestation"
}
```

### Statut Tâche
```bash
GET http://localhost:8100/tasks/{task_id}
```

## Configuration

Copier `.env.example` vers `.env` et ajuster:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
BROWSER_HEADLESS=true
```

## Modèles Ollama Recommandés

| Modèle | RAM | Vitesse | Qualité |
|--------|-----|---------|---------|
| qwen2.5:7b | 8GB | Rapide | Bonne |
| qwen2.5:14b | 16GB | Moyen | Très bonne |
| llama3.1:8b | 8GB | Rapide | Bonne |

## Architecture

```
browser-automation/
├── main.py              # API FastAPI
├── config.py            # Configuration
├── agents/
│   ├── base.py          # Agent de base
│   ├── sonelgaz.py      # Agent Sonelgaz
│   └── cnas.py          # Agent CNAS
├── data/                # Données extraites
├── screenshots/         # Captures d'écran
└── docker-compose.yml   # Docker config
```

## Sécurité

⚠️ **Important**:
- Ne jamais stocker de mots de passe en clair
- Les données extraites sont stockées localement
- Utiliser HTTPS en production
- Les captures d'écran peuvent contenir des données sensibles

## Ajout de Nouveaux Services

1. Créer `agents/nouveau_service.py`
2. Hériter de `BaseAutomationAgent`
3. Implémenter les méthodes spécifiques
4. Ajouter les routes dans `main.py`

## Coûts

| Ressource | Coût |
|-----------|------|
| Ollama | $0 |
| Browser-Use | $0 |
| Serveur (si VPS) | ~$5-15/mois |
| **Total** | **$0-15/mois** |
