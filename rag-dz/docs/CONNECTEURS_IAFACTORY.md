# 🔌 Connecteurs IA Factory

> **Connexion simple et sécurisée à vos données avec Studio Créatif & Archon Hub**

IA Factory offre une méthode très simple pour connecter vos applications au Studio Créatif, aux agents BMAD et à tous les services de la plateforme.

---

## 🚀 Démarrage Rapide

### Accéder aux Connecteurs

1. **Via Archon Hub** (recommandé)
   ```
   http://localhost:8182/settings
   → Onglet "Integrations"
   → Bouton "Add Connector"
   ```

2. **Via Backend API**
   ```
   http://localhost:8180/docs
   → Section "/api/v1/connectors"
   ```

3. **Via Studio Créatif**
   ```
   http://localhost:8184/studio
   → Menu "More"
   → "MCP Servers"
   → "Configure Connectors"
   ```

---

## 📊 Connecteurs First-Party

### Base de Données

#### 🐘 PostgreSQL (avec PGVector)
**Configuration automatique** - Déjà connecté dans Docker

```bash
# Credentials (dans .env.local)
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=iafactory
POSTGRES_USER=postgres
POSTGRES_PASSWORD=votre-mot-de-passe-securise
```

**Capacités:**
- ✅ Requêtes SQL directes
- ✅ Recherche vectorielle (embeddings)
- ✅ Full-text search
- ✅ Analytics temps réel

**Utilisation dans prompts:**
```
"Analyser les 100 dernières conversations utilisateurs dans PostgreSQL
et générer un rapport des questions les plus fréquentes"
```

---

#### 💎 Qdrant Vector Database
**Pour recherche sémantique avancée**

```bash
# Configuration
QDRANT_URL=http://qdrant:6333
QDRANT_API_KEY=optionnel
```

**Capacités:**
- ✅ Recherche vectorielle ultra-rapide
- ✅ Filtrage hybride (vecteurs + metadata)
- ✅ Collections multiples
- ✅ Scalabilité horizontale

**Utilisation dans prompts:**
```
"Rechercher dans Qdrant les documents similaires à 'intelligence artificielle algérienne'
et résumer les 5 meilleurs résultats"
```

---

#### 🗄️ Redis Cache
**Cache haute performance**

```bash
# Configuration
REDIS_URL=redis://redis:6379
```

**Capacités:**
- ✅ Cache de réponses LLM
- ✅ Session storage
- ✅ Rate limiting
- ✅ Pub/Sub messaging

---

### Communication & Collaboration

#### 💬 Slack
**Intégration complète avec votre workspace**

**Setup:**
1. Aller sur https://api.slack.com/apps
2. Créer une nouvelle app
3. Activer les scopes nécessaires:
   - `chat:write` - Envoyer messages
   - `channels:read` - Lire channels
   - `users:read` - Lire utilisateurs
4. Installer l'app dans votre workspace
5. Copier le Bot Token

```bash
# .env.local
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxxx
SLACK_SIGNING_SECRET=xxxxxxxxxxxxx
```

**Capacités:**
- ✅ Envoyer messages automatiques
- ✅ Créer/gérer channels
- ✅ Inviter utilisateurs
- ✅ Upload fichiers
- ✅ Réagir aux mentions

**Utilisation dans prompts:**
```
"Envoyer un message sur #general Slack pour annoncer le lancement
de notre nouvelle fonctionnalité IA"
```

---

#### 📝 Notion
**Gestion de documentation et bases de données**

**Setup:**
1. Aller sur https://www.notion.so/my-integrations
2. Créer une nouvelle intégration
3. Copier l'API key
4. Partager vos pages Notion avec l'intégration

```bash
# .env.local
NOTION_API_KEY=secret_xxxxxxxxxxxxx
```

**Capacités:**
- ✅ Lire/écrire pages
- ✅ Query databases
- ✅ Créer pages automatiquement
- ✅ Update properties

**Utilisation dans prompts:**
```
"Créer une nouvelle page Notion dans la database 'Projets'
avec le titre 'IA Factory Launch' et remplir tous les champs"
```

---

#### 📁 Google Drive
**Stockage et partage de fichiers**

**Setup:**
1. Aller sur https://console.cloud.google.com
2. Créer un Service Account
3. Activer Google Drive API
4. Télécharger les credentials JSON

```bash
# .env.local
GOOGLE_DRIVE_CREDS='{"type":"service_account",...}'
```

**Capacités:**
- ✅ Upload/download fichiers
- ✅ Créer folders
- ✅ Partager fichiers
- ✅ Search dans Drive

**Utilisation dans prompts:**
```
"Uploader le rapport PDF généré sur Google Drive dans le folder
'IA Factory Reports' et partager avec l'équipe"
```

---

### Productivité

#### ✅ Google Tasks
**Gestion de tâches et to-do lists**

**Setup:**
1. Aller sur https://console.cloud.google.com
2. Activer Google Tasks API
3. Configurer OAuth 2.0

```bash
# .env.local
GOOGLE_TASKS_CREDS='{"type":"service_account",...}'
```

**Capacités:**
- ✅ Créer tâches
- ✅ Lister tâches
- ✅ Marquer comme complété
- ✅ Organiser en listes

**Utilisation dans prompts:**
```
"Créer une nouvelle tâche Google Tasks:
'Finaliser présentation IA Factory pour le 30 janvier'"
```

---

#### 📅 Google Calendar
**Gestion d'événements et planification**

**Setup:**
1. Aller sur https://console.cloud.google.com
2. Activer Google Calendar API
3. Configurer Service Account

```bash
# .env.local
GOOGLE_CALENDAR_CREDS='{"type":"service_account",...}'
```

**Capacités:**
- ✅ Créer événements
- ✅ Lire calendrier
- ✅ Update événements
- ✅ Inviter participants

**Utilisation dans prompts:**
```
"Créer un événement Google Calendar pour demain à 14h:
'Réunion IA Factory - Revue Sprint' avec toute l'équipe"
```

---

### Développement

#### 🐙 GitHub
**Gestion de code et collaboration**

**Setup:**
1. Aller sur https://github.com/settings/tokens
2. Générer un Personal Access Token
3. Sélectionner scopes: `repo`, `workflow`, `read:org`

```bash
# .env.local
GITHUB_TOKEN=ghp_xxxxxxxxxxxxx
```

**Capacités via MCP:**
- ✅ Lire repos/fichiers
- ✅ Créer issues/PRs
- ✅ Commit code
- ✅ Gérer branches
- ✅ Run workflows

**Utilisation dans prompts:**
```
"Créer un nouveau repo GitHub 'iafactory-mobile'
avec README, .gitignore Python et LICENSE MIT"
```

---

#### 🦊 GitLab
**Alternative à GitHub**

```bash
# .env.local
GITLAB_TOKEN=glpat-xxxxxxxxxxxxx
GITLAB_URL=https://gitlab.com
```

**Capacités:**
- ✅ Gestion repos
- ✅ CI/CD pipelines
- ✅ Issues/Merge Requests
- ✅ Container Registry

---

### Messaging & SMS

#### 📱 Twilio (SMS/WhatsApp)
**Communication par SMS et WhatsApp**

**Setup:**
1. Créer compte sur https://www.twilio.com
2. Acheter un numéro (+213 pour Algérie disponible)
3. Configurer WhatsApp Business

```bash
# .env.local
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+213xxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+213xxxxxxxxx
```

**Capacités:**
- ✅ Envoyer SMS
- ✅ WhatsApp messages
- ✅ Recevoir webhooks
- ✅ Voice calls
- ✅ Vérification numéros

**Utilisation dans prompts:**
```
"Envoyer un SMS via Twilio au +213 XXX XXX XXX:
'Votre code de vérification IA Factory est: 123456'"
```

---

### Web Scraping & Automation

#### 🎭 Playwright
**Automation web et scraping**

**Configuration automatique** - Déjà disponible via MCP

**Capacités:**
- ✅ Screenshot pages web
- ✅ Navigation automatique
- ✅ Remplir formulaires
- ✅ Extraire données
- ✅ Tests E2E

**Utilisation dans prompts:**
```
"Utiliser Playwright pour prendre un screenshot de https://iafactory.dz
en mode desktop et mobile"
```

---

#### 🦁 Brave Search
**Recherche web respectueuse de la vie privée**

**Setup:**
1. Créer compte sur https://brave.com/search/api/
2. Plan gratuit: 500 requêtes/mois

```bash
# .env.local
BRAVE_API_KEY=BSA_xxxxxxxxxxxxx
```

**Capacités:**
- ✅ Recherche web
- ✅ Résultats structurés
- ✅ News search
- ✅ Image search

**Utilisation dans prompts:**
```
"Rechercher sur Brave les dernières actualités sur 'intelligence artificielle Algérie'
et résumer les 5 articles les plus récents"
```

---

#### 📺 YouTube Transcript
**Extraction de transcriptions vidéos**

**Configuration automatique** - Pas d'API key requise

**Capacités:**
- ✅ Télécharger transcripts
- ✅ Traduction automatique
- ✅ Timestamps
- ✅ Multilingue

**Utilisation dans prompts:**
```
"Récupérer la transcription de la vidéo YouTube [URL]
et générer un résumé structuré avec timestamps"
```

---

## 🔐 Sécurité & Authentification

### Gestion des Credentials

**Stockage sécurisé:**
- ✅ **PostgreSQL chiffré** - Toutes les API keys sont chiffrées AES-256
- ✅ **Variables d'environnement** - Pour secrets sensibles
- ✅ **Vault optionnel** - HashiCorp Vault supporté

**Accès:**
```bash
# Via Archon Hub
http://localhost:8182/settings
→ "Provider Credentials"
→ "Add New Credential"
```

**Format:**
```json
{
  "provider": "github",
  "credential_type": "token",
  "encrypted_value": "ghp_xxxxxxxxxxxxx",
  "metadata": {
    "scopes": ["repo", "workflow"],
    "created_at": "2025-01-18"
  }
}
```

---

### OAuth 2.0 Flow

Pour services Google (Drive, Calendar, Tasks):

1. **Backend génère URL d'autorisation**
   ```python
   GET /api/v1/auth/google/authorize
   ```

2. **User consent sur Google**

3. **Callback avec code**
   ```python
   GET /api/v1/auth/google/callback?code=xxx
   ```

4. **Backend stocke tokens (refresh + access)**

5. **Auto-refresh avant expiration**

---

## 🎯 Utilisation dans Studio Créatif

### Détection Automatique

Le Studio détecte automatiquement quel connecteur utiliser:

```
Prompt: "Envoyer un message Slack"
→ Détection: Communication
→ Connecteur: Slack
→ Action: chat.postMessage
```

```
Prompt: "Créer une issue GitHub"
→ Détection: Development
→ Connecteur: GitHub MCP
→ Action: create_issue
```

---

### Configuration MCP Servers

**Via Studio UI:**

1. Cliquer sur bouton "MCP" dans toolbar
2. Sélectionner jusqu'à 5 serveurs (limite Abacus.AI)
3. Filtrer par catégorie:
   - 🔧 Development (GitHub, GitLab)
   - 📄 Content (YouTube, Playwright, Notion)
   - 💾 Data (PostgreSQL, SQLite)
   - 🤖 Automation (Google Tasks/Calendar)
   - 💬 Communication (Slack, Google Drive)

4. Cliquer "Apply Configuration"
5. Génération automatique du JSON

**Format généré:**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxxx"
      }
    },
    "postgresql": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@localhost/db"
      }
    }
  }
}
```

---

## 📚 Exemples d'Utilisation

### Workflow Multi-Connecteurs

**Scénario**: Création de rapport automatique

```
Prompt:
"1. Analyser les données de ventes dans PostgreSQL (table 'orders')
 2. Créer un graphique avec les tendances
 3. Générer un rapport PDF
 4. Uploader sur Google Drive dans folder 'Reports'
 5. Envoyer notification Slack sur #sales
 6. Créer une tâche Google Tasks pour review"
```

**Connecteurs utilisés:**
- PostgreSQL (data)
- Code Generation (graphique)
- Doc-Gen (PDF)
- Google Drive (upload)
- Slack (notification)
- Google Tasks (tâche)

---

### Automatisation E-commerce

```
Prompt:
"Quand nouvelle commande dans PostgreSQL (webhook):
 1. Envoyer SMS Twilio au client
 2. Créer task Google Tasks pour préparation
 3. Log dans Notion database 'Orders'
 4. Notification Slack #operations"
```

---

### CI/CD Automatique

```
Prompt:
"1. Lire le code du repo GitHub 'iafactory/backend'
 2. Générer tests unitaires manquants
 3. Créer une nouvelle branch 'tests/auto-generated'
 4. Commit les tests
 5. Créer Pull Request
 6. Notifier sur Slack"
```

---

## 🔄 API Reference

### Créer un Connecteur

**Endpoint:**
```http
POST /api/v1/connectors
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "My GitHub",
  "type": "github",
  "credentials": {
    "token": "ghp_xxxxxxxxxxxxx"
  },
  "metadata": {
    "organization": "iafactory",
    "description": "Main GitHub org"
  }
}
```

**Response:**
```json
{
  "id": "conn_123",
  "name": "My GitHub",
  "type": "github",
  "status": "active",
  "created_at": "2025-01-18T10:00:00Z"
}
```

---

### Lister Connecteurs

```http
GET /api/v1/connectors
Authorization: Bearer <token>
```

**Response:**
```json
{
  "connectors": [
    {
      "id": "conn_123",
      "name": "My GitHub",
      "type": "github",
      "status": "active"
    },
    {
      "id": "conn_456",
      "name": "Production DB",
      "type": "postgresql",
      "status": "active"
    }
  ]
}
```

---

### Tester Connexion

```http
POST /api/v1/connectors/{id}/test
Authorization: Bearer <token>
```

**Response:**
```json
{
  "status": "success",
  "latency_ms": 142,
  "details": {
    "github_user": "iafactory",
    "rate_limit_remaining": 4999
  }
}
```

---

### Supprimer Connecteur

```http
DELETE /api/v1/connectors/{id}
Authorization: Bearer <token>
```

---

## 🛡️ Bonnes Pratiques

### 1. Credentials Management

❌ **À ÉVITER:**
```bash
# Hardcoder les credentials
GITHUB_TOKEN=ghp_123456789
```

✅ **RECOMMANDÉ:**
```bash
# Utiliser secrets management
docker secret create github_token ghp_123456789

# Ou référencer depuis vault
GITHUB_TOKEN=${VAULT_GITHUB_TOKEN}
```

---

### 2. Rotation des Clés

```bash
# Planifier rotation tous les 90 jours
*/0 0 1 */3 * /scripts/rotate-api-keys.sh
```

---

### 3. Least Privilege

Pour GitHub, limiter les scopes:
```bash
# Minimum nécessaire
GITHUB_TOKEN_SCOPES=repo,read:org

# Au lieu de
GITHUB_TOKEN_SCOPES=admin:everything
```

---

### 4. Monitoring

```python
# Logger tous les accès
logger.info(f"Connector {connector_id} accessed by {user_id} at {timestamp}")

# Alerter sur comportement suspect
if request_count > threshold:
    alert_security_team()
```

---

### 5. Rate Limiting

```python
# Respecter les limites des APIs externes
@rate_limit(max_calls=5000, period=3600)  # GitHub: 5000/hour
def github_api_call():
    pass
```

---

## 🐛 Troubleshooting

### Connecteur ne fonctionne pas

**1. Vérifier credentials:**
```bash
docker exec -it iaf-dz-backend python -c "
from app.services.user_key_service import UserKeyService
keys = UserKeyService.get_user_keys(user_id=1)
print(keys)
"
```

**2. Tester manuellement:**
```bash
# GitHub
curl -H "Authorization: token ghp_xxxxxxxxxxxxx" \
  https://api.github.com/user

# Slack
curl -H "Authorization: Bearer xoxb-xxxxxxxxxxxxx" \
  https://slack.com/api/auth.test
```

**3. Vérifier logs:**
```bash
docker logs iaf-dz-backend --tail 100 | grep connector
```

---

### Erreur "Quota exceeded"

**GitHub:**
- Limite: 5000 req/hour
- Solution: Attendre reset ou utiliser multiple tokens

**Brave Search:**
- Limite: 500 req/mois (free tier)
- Solution: Upgrader au plan payant

**Google APIs:**
- Limite: Variable selon API
- Solution: Activer billing et augmenter quotas

---

### Erreur OAuth

**Google Services:**

1. Vérifier redirect URI:
   ```
   http://localhost:8180/api/v1/auth/google/callback
   ```

2. Vérifier scopes:
   ```
   https://www.googleapis.com/auth/drive
   https://www.googleapis.com/auth/calendar
   ```

3. Refresh token expiré:
   ```bash
   # Relancer OAuth flow
   open http://localhost:8182/settings?reconnect=google
   ```

---

## 📊 Dashboard Connecteurs

**Via Archon Hub:**

```
http://localhost:8182/connectors
```

**Métriques affichées:**
- ✅ Nombre de connecteurs actifs
- ✅ Requêtes last 24h
- ✅ Taux d'erreur
- ✅ Latency moyenne
- ✅ Quotas restants

---

## 🚀 Ajout d'un Nouveau Connecteur

### Backend (Python)

**1. Créer le service:**
```python
# backend/rag-compat/app/services/my_connector_service.py

class MyConnectorService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = MyConnectorClient(api_key)

    async def do_action(self, params: dict):
        result = await self.client.action(params)
        return result
```

**2. Créer le router:**
```python
# backend/rag-compat/app/routers/my_connector.py

from fastapi import APIRouter, Depends
from app.services.my_connector_service import MyConnectorService

router = APIRouter(prefix="/my-connector", tags=["connectors"])

@router.post("/action")
async def perform_action(
    params: dict,
    service: MyConnectorService = Depends()
):
    return await service.do_action(params)
```

**3. Enregistrer dans main.py:**
```python
from app.routers import my_connector

app.include_router(my_connector.router, prefix="/api/v1")
```

---

### Frontend (MCP Server)

**1. Ajouter à MCPConfig.ts:**
```typescript
export const MCP_SERVERS: MCPServer[] = [
  // ... autres serveurs
  {
    id: 'my-connector',
    name: 'My Connector',
    icon: '🔌',
    category: 'automation',
    description: 'Description du connecteur',
    protocol: 'stdio',
    command: 'npx',
    args: ['-y', '@mcp/server-my-connector'],
    requires_auth: true,
    env_vars: {
      MY_CONNECTOR_API_KEY: 'required'
    }
  }
];
```

**2. Tester:**
```bash
cd bolt-diy
npm run dev

# Ouvrir http://localhost:8184/studio
# Cliquer MCP → Sélectionner "My Connector"
```

---

## 📈 Statistiques & Analytics

**Requêtes par connecteur (last 30 days):**

| Connecteur | Requêtes | Succès | Erreurs | Latency Avg |
|------------|----------|--------|---------|-------------|
| PostgreSQL | 12,543   | 99.8%  | 0.2%    | 45ms        |
| GitHub     | 1,234    | 98.5%  | 1.5%    | 320ms       |
| Slack      | 856      | 99.9%  | 0.1%    | 180ms       |
| Google Drive | 432    | 97.2%  | 2.8%    | 520ms       |
| Twilio     | 234      | 99.1%  | 0.9%    | 240ms       |

**Query dans PostgreSQL:**
```sql
SELECT
    connector_type,
    COUNT(*) as total_requests,
    AVG(latency_ms) as avg_latency,
    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as success_rate
FROM connector_logs
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY connector_type
ORDER BY total_requests DESC;
```

---

## 🎓 Ressources Additionnelles

### Documentation Externe

- **GitHub MCP**: https://github.com/modelcontextprotocol/servers
- **Slack API**: https://api.slack.com/docs
- **Twilio Docs**: https://www.twilio.com/docs
- **Google APIs**: https://console.cloud.google.com/apis
- **Notion API**: https://developers.notion.com

### Vidéos Tutoriels

- → [Configuration PostgreSQL PGVector](./GUIDE_INSTALLATION_VPS.md)
- → [Setup Twilio WhatsApp](./DEPLOIEMENT_HETZNER.md)
- → [GitHub MCP Integration](./ETAT_ACTUEL_BMAD_WORKFLOW.md)
- → [OAuth Google Services](./CONFIGURATION_GROQ_IMMEDIAT.md)

---

## ✅ Checklist de Configuration

### Setup Initial

- [ ] Configurer `.env.local` avec credentials
- [ ] Démarrer services: `docker-compose up -d`
- [ ] Vérifier PostgreSQL: `docker logs iaf-dz-postgres`
- [ ] Vérifier Backend: `curl http://localhost:8180/health`
- [ ] Accéder à Archon Hub: http://localhost:8182

### Connecteurs Recommandés (Minimum)

- [ ] PostgreSQL (database) - Déjà configuré
- [ ] GitHub (development) - Token gratuit
- [ ] Slack (communication) - Optionnel
- [ ] Brave Search (web search) - 500 req/mois gratuit

### Connecteurs Optionnels

- [ ] Twilio (SMS/WhatsApp) - Payant
- [ ] Google Drive (storage) - Gratuit avec Gmail
- [ ] Google Calendar (productivity) - Gratuit
- [ ] Notion (documentation) - Freemium
- [ ] GitLab (alternative GitHub) - Gratuit

---

## 🆘 Support

**Questions?**
- 📧 Email: support@iafactory.dz
- 💬 Slack: [IA Factory Community](http://localhost:8185/slack)
- 📚 Docs: http://localhost:8183

**Issues GitHub:**
- Bugs: https://github.com/iafactory/rag-dz/issues
- Feature requests: https://github.com/iafactory/rag-dz/discussions

---

## 🔗 Liens Rapides

- **Hub Documentation**: [INDEX_IAFACTORY.md](./INDEX_IAFACTORY.md)
- **Studio Créatif Guide**: [STUDIO_CREATIF_GUIDE.md](./STUDIO_CREATIF_GUIDE.md)
- **Prompting Tips**: [PROMPTING_TIPS_STUDIO.md](./PROMPTING_TIPS_STUDIO.md)
- **Architecture**: [ARCHITECTURE_INTEGREE.md](./ARCHITECTURE_INTEGREE.md)
- **API Reference**: http://localhost:8180/docs

---

**Version**: 1.0.0
**Dernière mise à jour**: 2025-01-18

🇩🇿 **IA Factory Algeria - Connectez vos données, libérez votre potentiel**

---

Copyright © 2025 IA Factory Algeria. Tous droits réservés.
