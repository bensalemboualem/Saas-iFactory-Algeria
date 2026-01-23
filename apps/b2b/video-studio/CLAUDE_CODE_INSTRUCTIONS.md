# 🎯 INSTRUCTIONS CLAUDE CODE - IAFactory Video Studio Pro

## Objectif du Projet

Développer une **usine à contenu multimédia automatisée** capable de :
- Générer des scripts viraux avec Claude Opus 4
- Créer des vidéos avec MiniMax/Luma/Fal.ai
- Synthétiser des voix avec ElevenLabs
- Assembler automatiquement avec FFmpeg
- Publier sur YouTube/TikTok/Instagram via n8n

## Architecture Technique

```
Frontend (Next.js 14) ←→ Backend (FastAPI) ←→ Services IA (Claude, MiniMax, ElevenLabs)
                              ↓
                      Celery Workers (Redis)
                              ↓
                      Storage (MinIO/S3)
```

---

## 📋 PHASES DE DÉVELOPPEMENT

### PHASE 1 : Backend Core (Priorité : HAUTE)

```bash
# Ordre de développement :
1. backend/config.py ✅ (déjà créé)
2. backend/main.py ✅ (déjà créé)
3. backend/agents/__init__.py ✅ (déjà créé)
4. backend/agents/scriptwriter.py ✅ (déjà créé)
5. backend/services/elevenlabs_service.py ✅ (déjà créé)
```

**À créer maintenant :**

```python
# backend/services/minimax_service.py
# Service pour la génération vidéo MiniMax/Hailuo
# - text_to_video(prompt, duration)
# - image_to_video(image_path, motion_prompt)
# - get_generation_status(job_id)

# backend/services/fal_service.py
# Service pour Fal.ai (images et vidéo rapide)
# - generate_image(prompt, style)
# - text_to_video(prompt)
# - image_to_video(image_path)

# backend/video/montage_orchestrator.py
# Orchestration FFmpeg pour le montage
# - assemble_video(clips, audio, music)
# - add_subtitles(video, srt_path, language)
# - convert_format(video, target_format)
# - extract_segment(video, start, end)
```

### PHASE 2 : Agents IA Complets

```python
# backend/agents/storyboarder.py
# Découpage visuel du script
# - decompose_script(script) -> List[Scene]
# - generate_visual_prompts(scene) -> str
# - create_thumbnail(script) -> Image

# backend/agents/director.py
# Orchestration du montage
# - assemble_project(assets) -> Video
# - apply_transitions(clips) -> Video
# - render_multiformat(video) -> Dict[str, Video]

# backend/agents/growth_hacker.py
# Optimisation virale
# - analyze_viral_potential(script) -> Score
# - generate_title_variations(topic) -> List[str]
# - optimize_hashtags(content, platform) -> List[str]

# backend/agents/distributor.py
# Publication automatisée
# - publish_youtube(video, metadata)
# - publish_tiktok(video, metadata)
# - publish_instagram(video, metadata)
# - schedule_post(video, platforms, datetime)
```

### PHASE 3 : API Routes

```python
# backend/api/routes/scripts.py
POST /api/v1/scripts/generate
GET  /api/v1/scripts/{id}
PUT  /api/v1/scripts/{id}
POST /api/v1/scripts/{id}/approve
POST /api/v1/scripts/{id}/extract-shorts

# backend/api/routes/video.py
POST /api/v1/video/generate
GET  /api/v1/video/{id}/status
GET  /api/v1/video/{id}/preview
POST /api/v1/video/{id}/render
POST /api/v1/video/{id}/export

# backend/api/routes/audio.py
POST /api/v1/audio/tts
POST /api/v1/audio/music
POST /api/v1/audio/clone-voice
GET  /api/v1/audio/voices

# backend/api/routes/publish.py
POST /api/v1/publish/youtube
POST /api/v1/publish/tiktok
POST /api/v1/publish/instagram
POST /api/v1/publish/schedule
GET  /api/v1/publish/status/{id}

# backend/api/routes/tokens.py
GET  /api/v1/tokens/balance
POST /api/v1/tokens/estimate
GET  /api/v1/tokens/history
POST /api/v1/tokens/purchase
```

### PHASE 4 : Frontend React/Next.js

```typescript
// frontend/components/VideoStudio/StudioDashboard.tsx
// Dashboard principal avec :
// - Liste des projets
// - Boutons de création (Podcast, Short, Vidéo)
// - Statistiques de tokens

// frontend/components/VideoStudio/ScriptEditor.tsx
// Éditeur de scripts avec :
// - Édition en temps réel
// - Prévisualisation du timing
// - Génération IA

// frontend/components/VideoStudio/Timeline.tsx
// Timeline de montage avec :
// - Pistes audio/vidéo
// - Drag & drop
// - Aperçu

// frontend/components/PodcastCreator/PodcastWizard.tsx
// Assistant création podcast :
// Step 1: Sujet et paramètres
// Step 2: Génération script
// Step 3: Review et édition
// Step 4: Génération assets
// Step 5: Montage et preview
// Step 6: Publication

// frontend/components/ShortsGenerator/ShortsWizard.tsx
// Assistant création Shorts :
// Step 1: Hook ou sujet
// Step 2: Script court
// Step 3: Visuel
// Step 4: Voix
// Step 5: Export multi-plateformes
```

### PHASE 5 : Infrastructure

```yaml
# infrastructure/docker-compose.yml ✅ (déjà créé)
# Vérifier que tous les services sont configurés

# infrastructure/Dockerfile.backend
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y ffmpeg
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# infrastructure/Dockerfile.frontend
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

---

## 🔧 CONVENTIONS DE CODE

### Python (Backend)
```python
# Utiliser async/await partout
async def my_function():
    pass

# Typage strict avec Pydantic
class MyModel(BaseModel):
    field: str
    optional_field: Optional[int] = None

# Logging structuré
logger.info(f"[{self.name}] Action: {details}")

# Gestion d'erreurs
try:
    result = await operation()
except SpecificError as e:
    logger.error(f"Error: {e}")
    raise HTTPException(status_code=400, detail=str(e))
```

### TypeScript (Frontend)
```typescript
// Components fonctionnels avec hooks
const MyComponent: React.FC<Props> = ({ prop1, prop2 }) => {
    const [state, setState] = useState<StateType>(initialState);
    
    return <div>{/* ... */}</div>;
};

// Tailwind CSS pour le styling
<div className="flex flex-col gap-4 p-6 bg-gray-900 rounded-xl">
```

---

## 📁 STRUCTURE DES FICHIERS À CRÉER

```
backend/
├── services/
│   ├── __init__.py
│   ├── minimax_service.py      # À créer
│   ├── fal_service.py          # À créer
│   ├── suno_service.py         # À créer
│   └── n8n_service.py          # À créer
├── video/
│   ├── __init__.py
│   ├── generator.py            # À créer
│   ├── montage_orchestrator.py # À créer
│   └── format_adapter.py       # À créer
├── audio/
│   ├── __init__.py
│   ├── tts.py                  # À créer
│   ├── music_generator.py      # À créer
│   └── voice_cloner.py         # À créer
├── agents/
│   ├── storyboarder.py         # À créer
│   ├── director.py             # À créer
│   ├── growth_hacker.py        # À créer
│   └── distributor.py          # À créer
└── api/
    ├── routes/
    │   ├── scripts.py          # À créer
    │   ├── video.py            # À créer
    │   ├── audio.py            # À créer
    │   ├── publish.py          # À créer
    │   └── tokens.py           # À créer
    └── schemas/
        ├── script.py           # À créer
        ├── video.py            # À créer
        └── audio.py            # À créer

frontend/
├── components/
│   ├── VideoStudio/
│   │   ├── StudioDashboard.tsx
│   │   ├── ScriptEditor.tsx
│   │   ├── Timeline.tsx
│   │   ├── PreviewPlayer.tsx
│   │   └── PublishPanel.tsx
│   ├── PodcastCreator/
│   │   ├── PodcastWizard.tsx
│   │   └── EpisodeManager.tsx
│   └── ShortsGenerator/
│       ├── ShortsWizard.tsx
│       └── ViralOptimizer.tsx
├── pages/
│   └── video-studio/
│       ├── index.tsx
│       ├── podcast.tsx
│       ├── shorts.tsx
│       └── algerie-connect.tsx
└── hooks/
    ├── useVideoGeneration.ts
    ├── useAudioGeneration.ts
    └── useTokenBalance.ts
```

---

## 🚀 COMMANDES CLAUDE CODE

### Pour démarrer le développement :
```
cd /path/to/iafactory-video-studio-pro

# Phase 1 : Compléter les services backend
"Claude, crée le service MiniMax dans backend/services/minimax_service.py avec les méthodes text_to_video et image_to_video. Utilise l'API MiniMax/Hailuo."

# Phase 2 : Créer les agents manquants
"Claude, crée l'agent Storyboarder dans backend/agents/storyboarder.py qui découpe un script en scènes et génère des prompts visuels pour chaque scène."

# Phase 3 : API Routes
"Claude, crée les routes FastAPI pour les scripts dans backend/api/routes/scripts.py avec les endpoints CRUD et la génération."

# Phase 4 : Frontend
"Claude, crée le composant StudioDashboard.tsx avec Next.js et Tailwind. Il doit afficher la liste des projets et les boutons de création."

# Phase 5 : Tests
"Claude, écris les tests unitaires pour l'agent Scriptwriter dans tests/test_scriptwriter.py"
```

---

## ✅ CHECKLIST FINALE

- [ ] Backend FastAPI fonctionnel
- [ ] Service MiniMax connecté et testé
- [ ] Service ElevenLabs connecté et testé
- [ ] Service Fal.ai connecté et testé
- [ ] Agent Scriptwriter testé
- [ ] Agent Storyboarder testé
- [ ] Agent Director (montage FFmpeg) testé
- [ ] Agent Growth Hacker testé
- [ ] Agent Distributor (n8n) testé
- [ ] Frontend Dashboard fonctionnel
- [ ] Wizard Podcast complet
- [ ] Wizard Shorts complet
- [ ] Docker Compose démarré
- [ ] Tests E2E passés
- [ ] Documentation API générée
- [ ] Système IAF-Tokens intégré
- [ ] Publication YouTube testée
- [ ] Publication TikTok testée
- [ ] Publication Instagram testée

---

## 💡 NOTES IMPORTANTES

1. **Priorité aux marchés locaux** : Toujours tester avec du contenu en Darija et références algériennes.

2. **Gestion des coûts** : Chaque opération doit déduire des IAF-Tokens. Implémenter le tracking dès le début.

3. **Qualité vidéo** : Privilégier MiniMax pour la qualité, Fal.ai pour la rapidité.

4. **Support RTL** : Les sous-titres arabes doivent être correctement alignés à droite.

5. **Montage automatique** : FFmpeg doit gérer la synchronisation audio/vidéo avec précision.

6. **Viralité** : Toujours identifier et extraire les moments viraux pour les Shorts.

---

*Dernière mise à jour : Décembre 2024*
*Projet : IAFactory Video Studio Pro v1.0*
