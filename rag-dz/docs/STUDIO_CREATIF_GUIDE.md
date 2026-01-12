# 🎨 Guide Complet - Studio Créatif IA Factory

## Vue d'ensemble

Le **Studio Créatif** est une plateforme complète de création multimédia avec IA, inspirée d'Abacus.AI, qui combine:

- ✅ **Toolbar Multi-outils** - 5 outils principaux + 12 outils avancés via le menu "More"
- ✅ **MCP Servers** - Intégration avec 12+ services externes via Model Context Protocol
- ✅ **Détection Automatique NLP** - Analyse intelligente du prompt pour sélectionner l'outil approprié
- ✅ **Génération Multi-Format** - Vidéos, images, code, présentations, audio, recherches
- ✅ **Workflow n8n** - Diffusion automatique sur réseaux sociaux et export multi-format
- ✅ **Intégration BMAD** - Agents IA pour optimisation des prompts

---

## 🚀 Accès au Studio

```
URL: http://localhost:8184/studio
```

---

## 🎯 Toolbar Principale (5 boutons)

| Bouton | Icon | Description | Modèles AI |
|--------|------|-------------|------------|
| **Image** | 🖼️ | Génération et édition d'images | GPT Image, FLUX Pro, FLUX Kontext, Nano Banana Pro, Seedream, Recraft, Ideogram, DALL-E 3 |
| **Code** | 💻 | Assistance au codage | - |
| **Playground** | 🎮 | Espace interactif pour tests | - |
| **Powerpoint** | 📊 | Génération de présentations | - |
| **Deep Research** | 🔬 | Recherche approfondie | - |

---

## ⋮ Menu "More" (12 options avancées)

### 🎬 Média

| Outil | Description | Modèles |
|-------|-------------|---------|
| **Video-Gen** | Génération de vidéos | Sora 2, Seedance Pro/Lite, Veo 3, Kling AI, Luma Dream Machine, Hailuo, Runway Gen-3 |
| **Lip Sync** | Synchronisation labiale | Hedra, OmniHuman |
| **Text-to-Speech** | Conversion texte → audio | ElevenLabs, OpenAI TTS |
| **Speech-to-Text** | Transcription audio | Whisper, Scribe |
| **Speech-to-Speech** | Conversion vocale | - |
| **Video Analysis** | Analyse de contenu vidéo | - |

### 📄 Documents

| Outil | Description |
|-------|-------------|
| **Doc-Gen** | Création de documents |
| **Editor** | Éditeur de texte enrichi |

### 🛠️ Utilitaires

| Outil | Description |
|-------|-------------|
| **Humanize** | Conversion texte IA → humain (3 tons: Professionnel, Humoristique, Caring) |
| **Scrape URL** | Extraction d'informations web |
| **Screenshot** | Capture d'écran |
| **Task** | Automatisation de tâches |

---

## 🔌 MCP Servers (Model Context Protocol)

### Configuration

1. Cliquez sur le bouton **🔌 MCP** dans la toolbar
2. Sélectionnez jusqu'à **5 serveurs** (limitation Abacus.AI)
3. Configurez les credentials si nécessaire
4. Cliquez sur **Appliquer**

### Serveurs Disponibles

#### 💻 Développement

| Serveur | Description | Auth |
|---------|-------------|------|
| **GitHub** 🐙 | Repositories, issues, PRs | ✓ (Token) |
| **GitLab** 🦊 | Repos, pipelines | ✓ (Token) |

#### 📝 Contenu & Web

| Serveur | Description | Auth |
|---------|-------------|------|
| **Playwright** 🎭 | Automation web, scraping | ✗ |
| **Brave Search** 🦁 | Recherche web | ✓ (API Key) |
| **YouTube Transcript** 📺 | Transcriptions vidéos | ✗ |
| **Notion** 📝 | Pages et databases | ✓ (API Key) |
| **Google Drive** 📁 | Fichiers | ✓ (OAuth) |

#### 💾 Données

| Serveur | Description | Auth |
|---------|-------------|------|
| **PostgreSQL** 🐘 | Base de données | ✓ (Connection String) |
| **SQLite** 💾 | Base de données locale | ✗ |

#### ⚙️ Automation

| Serveur | Description | Auth |
|---------|-------------|------|
| **Google Tasks** ✅ | To-do lists | ✓ (OAuth) |
| **Google Calendar** 📅 | Événements | ✓ (OAuth) |
| **Slack** 💬 | Messagerie | ✓ (Bot Token) |

### Exemple de Configuration JSON

```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxx"
    }
  },
  "playwright": {
    "command": "npx",
    "args": ["-y", "@executeautomation/playwright-mcp-server"]
  },
  "brave-search": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-brave-search"],
    "env": {
      "BRAVE_API_KEY": "BSA_xxxxxxxxxxxx"
    }
  }
}
```

---

## 🎨 Workflow de Création

### 1. Détection Automatique

Le système analyse automatiquement votre prompt et sélectionne l'outil approprié:

```
"Créer une vidéo sur le Sahara"  →  Video-Gen (Sora 2)
"Générer une image futuriste"    →  Image (FLUX Pro)
"Écrire du code Python"          →  Code
"Rechercher sur l'IA"             →  Deep Research
"Créer une présentation"          →  Powerpoint
"Convertir en audio"              →  Text-to-Speech
```

### 2. Optimisation BMAD

Si le backend BMAD est disponible:
- Agent **creative_architect** optimise le prompt
- Détection du type de contenu
- Recommandation du meilleur modèle

Mode démo (si backend indisponible):
- Détection locale par mots-clés
- Génération avec services externes

### 3. Génération

Selon le type:
- **Vidéo**: Utilise Sora 2, Seedance, etc.
- **Image**: Pollinations.ai + FLUX
- **Code**: Génération de snippets
- **Présentation**: Templates PowerPoint
- **Audio**: Services TTS
- **Research**: Rapport structuré

### 4. Publication n8n

#### Pour Vidéos:
- YouTube Shorts
- TikTok
- Instagram Reels
- LinkedIn Post
- X (Twitter)

#### Pour Présentations:
- Export PDF
- Export HTML
- Export CSV
- Export PHP

#### Pour Images:
- Instagram Post
- Facebook
- LinkedIn
- X (Twitter)

---

## 📊 Exemples d'Utilisation

### Exemple 1: Génération Vidéo Complète

```
1. Tapez: "Une vidéo sur le coucher de soleil dans le Sahara algérien"
2. Le système détecte → Video-Gen
3. BMAD optimise le prompt
4. Génération avec Sora 2
5. Sélectionnez les canaux: YouTube + TikTok + Instagram
6. Cliquez sur "Publier sur les Réseaux Sociaux"
7. Webhook n8n déclenché automatiquement
```

### Exemple 2: Image Professionnelle

```
1. Tapez: "Logo moderne pour une startup tech"
2. Détection → Image
3. Choix du modèle: FLUX Pro
4. Génération via Pollinations.ai
5. Diffusion sur Instagram + LinkedIn
```

### Exemple 3: Code avec GitHub MCP

```
1. Activez le serveur MCP GitHub
2. Tapez: "Créer une fonction Python pour analyser des logs"
3. Le code est généré
4. Utilisez les tools GitHub MCP:
   - create_repository
   - create_file
   - create_pull_request
```

### Exemple 4: Recherche avec Playwright

```
1. Activez Playwright MCP
2. Tapez: "Extraire les titres de https://example.com"
3. Playwright navigue et extrait
4. Résultats formatés en rapport
```

---

## 🔧 Configuration Backend

### Variables d'Environnement (.env.local)

```bash
# ═══════════════════════════════════════════════════════════════
# STUDIO CRÉATIF - CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# LLM Providers (pour BMAD)
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

# MCP Servers
GITHUB_TOKEN=ghp_xxxxxxxxxxxxx
BRAVE_API_KEY=BSA_xxxxxxxxxxxxx
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxxx
NOTION_API_KEY=secret_xxxxxxxxxxxxx

# n8n Webhook
N8N_WEBHOOK_URL=http://localhost:8185
```

---

## 🎯 Limitations

### MCP Servers (d'après Abacus.AI)
- ✅ Maximum 5 serveurs actifs
- ✅ Maximum 50 outils par serveur
- ❌ Pas d'accès au système de fichiers local (environnement isolé)
- ✅ Serveurs stdio (npm/PyPI) et SSE (remote) supportés

### Génération
- Vidéo: Selon les limites des providers (Sora 2, etc.)
- Image: Pollinations.ai gratuit
- Audio: Limites ElevenLabs/OpenAI TTS

---

## 🐛 Troubleshooting

### MCP Server ne se connecte pas
1. Vérifiez la config JSON (format correct)
2. Vérifiez que le serveur est démarré
3. Vérifiez les credentials

### Backend BMAD indisponible
→ Le mode démo local fonctionne automatiquement

### Erreur de génération
→ Vérifiez les logs Docker:
```bash
docker logs iaf-dz-studio --tail 50 --follow
```

---

## 📚 Ressources

- **MCP Registry**: https://github.com/modelcontextprotocol/servers
- **MCP Directory**: https://mcp.so
- **Abacus.AI Docs**: https://docs.abacus.ai
- **n8n Workflows**: http://localhost:8185

---

## 🚀 Prochaines Étapes

1. Configurer vos API keys dans `.env.local`
2. Activer les serveurs MCP nécessaires
3. Tester le workflow complet
4. Configurer n8n pour la publication automatique
5. Personnaliser les templates de génération

---

**Version**: 1.0.0
**Dernière mise à jour**: 2025-01-18
**Support**: IA Factory Algeria
