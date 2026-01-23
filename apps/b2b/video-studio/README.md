# 🎬 IAFactory Video Studio Pro

## Vision

IAFactory Video Studio Pro est une **usine à contenu multimédia automatisée** capable de produire des podcasts, vidéos longues et shorts viraux avec voix synthétique, le tout orchestré par des agents IA spécialisés.

## 🎯 Objectifs Business

- **Marché cible** : Algérie (Darija/Arabe/Français) et Suisse (Français/Allemand/Italien)
- **Différenciation** : Contenu local authentique que les IA génériques ne peuvent pas produire
- **Modèle économique** : Système IAF-Tokens (paiement à l'usage)

---

## 📁 Structure du Projet

```
iafactory-video-studio-pro/
├── README.md                          # Ce fichier
├── docs/
│   ├── ARCHITECTURE.md                # Architecture technique détaillée
│   ├── API_REFERENCE.md               # Documentation API
│   ├── AGENTS_SPECS.md                # Spécifications des agents IA
│   ├── WORKFLOW.md                    # Flux de production détaillé
│   └── MONETIZATION.md                # Système de tarification IAF-Tokens
│
├── backend/
│   ├── main.py                        # Point d'entrée FastAPI
│   ├── config.py                      # Configuration centralisée
│   ├── requirements.txt               # Dépendances Python
│   │
│   ├── agents/                        # Agents IA spécialisés
│   │   ├── __init__.py
│   │   ├── base_agent.py              # Classe abstraite agent
│   │   ├── scriptwriter.py            # Agent Scénariste (Claude Opus 4)
│   │   ├── storyboarder.py            # Agent Storyboarder
│   │   ├── director.py                # Agent Réalisateur/Montage
│   │   ├── growth_hacker.py           # Agent Optimisation Virale
│   │   └── distributor.py             # Agent Publication
│   │
│   ├── video/
│   │   ├── __init__.py
│   │   ├── generator.py               # Génération vidéo (MiniMax/Luma/Kling)
│   │   ├── montage_orchestrator.py    # Orchestration FFmpeg
│   │   └── format_adapter.py          # Adaptation multi-plateformes
│   │
│   ├── audio/
│   │   ├── __init__.py
│   │   ├── tts.py                     # Text-to-Speech (ElevenLabs/Rime)
│   │   ├── music_generator.py         # Musique IA (Suno)
│   │   └── voice_cloner.py            # Clonage de voix
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── minimax_service.py         # API MiniMax/Hailuo
│   │   ├── elevenlabs_service.py      # API ElevenLabs
│   │   ├── fal_service.py             # API Fal.ai
│   │   ├── suno_service.py            # API Suno
│   │   └── n8n_service.py             # Intégration n8n
│   │
│   └── api/
│       ├── __init__.py
│       ├── routes/
│       │   ├── video.py               # Endpoints vidéo
│       │   ├── audio.py               # Endpoints audio
│       │   ├── scripts.py             # Endpoints scripts
│       │   └── publish.py             # Endpoints publication
│       └── schemas/
│           ├── video.py               # Schémas Pydantic vidéo
│           ├── audio.py               # Schémas Pydantic audio
│           └── script.py              # Schémas Pydantic scripts
│
├── frontend/
│   ├── package.json
│   ├── next.config.js
│   │
│   ├── components/
│   │   ├── VideoStudio/
│   │   │   ├── StudioDashboard.tsx    # Dashboard principal
│   │   │   ├── ScriptEditor.tsx       # Éditeur de scripts
│   │   │   ├── Timeline.tsx           # Timeline de montage
│   │   │   ├── PreviewPlayer.tsx      # Lecteur de prévisualisation
│   │   │   └── PublishPanel.tsx       # Panel de publication
│   │   ├── PodcastCreator/
│   │   │   ├── PodcastWizard.tsx      # Assistant création podcast
│   │   │   └── EpisodeManager.tsx     # Gestion épisodes
│   │   └── ShortsGenerator/
│   │       ├── ShortsWizard.tsx       # Assistant shorts viraux
│   │       └── ViralOptimizer.tsx     # Optimisation virale
│   │
│   ├── pages/
│   │   ├── video-studio/
│   │   │   ├── index.tsx              # Page principale studio
│   │   │   ├── podcast.tsx            # Création podcasts
│   │   │   ├── shorts.tsx             # Création shorts
│   │   │   └── algerie-connect.tsx    # Studio spécial Algérie
│   │   └── api/                       # API Routes Next.js
│   │
│   └── hooks/
│       ├── useVideoGeneration.ts      # Hook génération vidéo
│       ├── useAudioGeneration.ts      # Hook génération audio
│       └── useTokenBalance.ts         # Hook solde IAF-Tokens
│
├── infrastructure/
│   ├── docker-compose.yml             # Stack Docker complète
│   ├── Dockerfile.backend             # Image backend
│   ├── Dockerfile.frontend            # Image frontend
│   ├── nginx.conf                     # Proxy inverse
│   └── .env.example                   # Variables d'environnement
│
├── scripts/
│   ├── setup.sh                       # Installation automatique
│   ├── deploy.sh                      # Déploiement production
│   └── test_pipeline.py               # Tests du pipeline
│
└── prompts/
    ├── scriptwriter_system.md         # System prompt Scénariste
    ├── storyboarder_system.md         # System prompt Storyboarder
    ├── director_system.md             # System prompt Réalisateur
    ├── growth_hacker_system.md        # System prompt Growth
    └── algerie_connect_system.md      # System prompt Algérie Connect
```

---

## 🤖 Architecture des Agents IA

### 1. Agent Scénariste (`scriptwriter.py`)
- **Modèle** : Claude Opus 4 (créativité + complexité)
- **Mission** : Génération de scripts optimisés pour le viral
- **Fonctionnalités** :
  - Scripts podcasts (format long)
  - Scripts Reels/TikTok (format court)
  - Hooks viraux (3 premières secondes)
  - Segmentation temporelle automatique

### 2. Agent Storyboarder (`storyboarder.py`)
- **Modèle** : Claude Sonnet 4 + MiniMax
- **Mission** : Découpage visuel du script
- **Fonctionnalités** :
  - Génération de visuels par scène
  - Suggestions de B-roll
  - Thumbnails optimisées

### 3. Agent Réalisateur (`director.py`)
- **Modèle** : Orchestrateur Python/FFmpeg
- **Mission** : Montage automatisé
- **Fonctionnalités** :
  - Assemblage vidéo + voix + musique
  - Sous-titres multilingues (RTL pour Arabe)
  - Cuts dynamiques automatiques

### 4. Agent Growth Hacker (`growth_hacker.py`)
- **Modèle** : Grok 4.1 Fast (rapidité)
- **Mission** : Optimisation virale
- **Fonctionnalités** :
  - Analyse des tendances
  - A/B testing titres/thumbnails
  - Hashtags optimisés par plateforme

### 5. Agent Distributeur (`distributor.py`)
- **Intégration** : n8n (Port 5678)
- **Mission** : Publication automatisée
- **Fonctionnalités** :
  - Upload YouTube/TikTok/Instagram
  - Planification intelligente
  - Adaptation format (9:16, 16:9)

---

## 💰 Système de Monétisation (IAF-Tokens)

| Service                | Coût (IAF-Tokens) |
|------------------------|-------------------|
| Script Claude Opus 4   | 50 tokens/1000 mots |
| Vidéo MiniMax (30s)    | 200 tokens |
| Voix ElevenLabs (1 min)| 30 tokens |
| Musique Suno (30s)     | 50 tokens |
| Publication (1 plateforme) | 10 tokens |
| Montage complet Short  | 100 tokens |
| Podcast complet (15 min) | 500 tokens |

---

## 🚀 Instructions pour Claude Code

### Phase 1 : Backend Core (Priorité Haute)
```bash
# Commande pour Claude Code
claude "Crée le backend FastAPI avec les services de base pour la génération vidéo et audio. Commence par backend/main.py, config.py et les services MiniMax/ElevenLabs."
```

### Phase 2 : Agents IA
```bash
claude "Implémente les 5 agents IA dans backend/agents/ en commençant par le Scriptwriter. Utilise le pattern async/await et intègre le système de tokens."
```

### Phase 3 : Orchestration Montage
```bash
claude "Crée le montage_orchestrator.py qui combine FFmpeg avec les outputs des services vidéo/audio. Support RTL pour l'arabe et multi-formats."
```

### Phase 4 : Frontend React/Next.js
```bash
claude "Développe l'interface Video Studio dans frontend/components/VideoStudio/ avec le dashboard principal et les wizards de création."
```

### Phase 5 : Infrastructure Docker
```bash
claude "Configure la stack Docker complète dans infrastructure/ avec n8n, le backend, le frontend et nginx."
```

---

## 🔧 Configuration Requise

### APIs Externes (clés à configurer)
- **MiniMax/Hailuo AI** : Génération vidéo premium
- **Luma Dream Machine** : Alternative vidéo
- **ElevenLabs** : TTS haute qualité
- **Suno AI** : Génération musicale
- **Fal.ai** : Pipeline IA rapide

### Services Locaux
- **FFmpeg** : Montage vidéo
- **n8n** : Automatisation (Port 5678)
- **PostgreSQL** : Base de données
- **Redis** : Cache et files d'attente

---

## 📋 Checklist de Développement

- [ ] Backend FastAPI initialisé
- [ ] Service MiniMax connecté
- [ ] Service ElevenLabs connecté
- [ ] Agent Scriptwriter fonctionnel
- [ ] Agent Storyboarder fonctionnel
- [ ] Agent Director (montage FFmpeg)
- [ ] Agent Growth Hacker
- [ ] Agent Distributor (n8n)
- [ ] Frontend Dashboard
- [ ] Wizard Podcast
- [ ] Wizard Shorts
- [ ] Docker Compose complet
- [ ] Tests E2E pipeline
- [ ] Documentation API
- [ ] Système IAF-Tokens intégré

---

## 🌍 Spécificités Locales

### Algérie Connect
- Support Darija (dialecte algérien)
- Références culturelles locales
- Experts virtuels algériens
- Thèmes : Tech, Économie, Culture DZ

### Suisse Connect
- Multilinguisme (FR/DE/IT)
- Conformité réglementaire
- Thèmes : Finance, Innovation, Business

---

*Dernière mise à jour : Décembre 2024*
*Version : 1.0.0-alpha*
