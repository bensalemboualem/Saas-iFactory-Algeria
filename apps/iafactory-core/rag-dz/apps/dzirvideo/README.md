# Dzir IA Video v2.1

> **Plateforme Unifiée Multi-Générateurs IA** - 40+ outils d'IA pour créer des vidéos automatiquement

## 🎯 Vue d'Ensemble

**Dzir IA Video** transforme n'importe quel texte en vidéo professionnelle YouTube Shorts en une seule commande, avec le choix entre **40 générateurs d'IA** (gratuits et premium).

### Qu'est-ce qui rend Dzir IA Video unique ?

- **40+ Générateurs IA** : Le plus grand catalogue unifié (WAN 2.1, Kling, Runway, Sora, etc.)
- **100% Gratuit possible** : Utilisez uniquement des générateurs gratuits (WAN 2.1, Qwen, DIGEN)
- **Smart Router** : Sélection automatique du meilleur générateur selon qualité/prix
- **Pipeline Complet** : Script → TTS → IA Vidéo → Sous-titres → Upload YouTube
- **Multi-langues** : Français, Arabe, Anglais

## 🚀 Quick Start (5 minutes)

### 1. Installer

```bash
git clone https://github.com/IAFactory/dzirvideo.git
cd dzirvideo
cp .env.example .env
```

### 2. Configurer (Clé gratuite Alibaba)

Obtenez une clé API gratuite : https://dashscope.console.aliyun.com/

```bash
# .env
ALIBABA_DASHSCOPE_API_KEY=sk-your-key-here  # 100 vidéos/jour GRATUIT
YOUTUBE_CLIENT_ID=your-youtube-oauth-id
YOUTUBE_CLIENT_SECRET=your-youtube-secret
YOUTUBE_REFRESH_TOKEN=your-refresh-token
```

### 3. Lancer

```bash
# Avec Docker
docker compose up -d

# Ou en local
pip install -r requirements.txt
uvicorn src.api:app --port 8200
```

### 4. Générer votre première vidéo

```bash
curl -X POST http://localhost:8200/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Les 5 plus beaux endroits d'\''Algérie",
    "duration_seconds": 30,
    "category": "text-to-video"
  }'
```

✅ Votre vidéo est générée et uploadée sur YouTube en 2-3 minutes !

## 📦 Fonctionnalités

### 🎬 Générateurs Vidéo (17 outils)

#### Gratuits (0€)
- **WAN 2.1** (Alibaba) - 100 vidéos/jour, Quality 85/100
- **DIGEN Sora** - Illimité, Quality 75/100
- **CogVideo** (Zhipu AI) - Self-hosted, Quality 82/100
- **Open-Sora** - Self-hosted, Quality 78/100

#### Freemium
- **Kling AI** (Kuaishou) - 66 crédits/jour ≈ 10 vidéos, Quality 90/100
- **Pika Labs** - 250 crédits gratuits, Quality 88/100
- **Luma Dream** - $9.99/mo illimité, Quality 90/100
- **Hailuo AI** (MiniMax) - 20 vidéos/jour, Quality 84/100

#### Premium
- **Runway Gen-4** - $0.05/sec, Quality 95/100 ⭐ Meilleur
- **Veo 2** (Google) - $0.50/sec, Quality 93/100
- **Sora** (OpenAI) - $0.30/sec, Quality 92/100
- **Hunyuan Video** (Tencent) - $0.01/sec, Quality 82/100

### 🖼️ Générateurs Image (9 outils)

- **Qwen-VL** (Alibaba) - 100 images/jour GRATUIT, Quality 80/100
- **FLUX.1** (Black Forest Labs) - $0.01/image, Quality 90/100
- **DALL-E 3** (OpenAI) - $0.04/image, Quality 92/100
- **Midjourney** - $10/mo, Quality 95/100
- **Stable Diffusion 3.5** - $0.02/image, Quality 90/100
- **Ideogram** - $0.025/image, Quality 88/100
- **Leonardo AI** - 150 crédits/jour gratuits, Quality 85/100
- **Adobe Firefly** - $4.99/mo, Quality 87/100
- **Playground v2** - 50 images/jour gratuits, Quality 86/100

### 🎭 Avatars Parlants (5 outils)

- **HeyGen** - $24/mo, Quality 92/100
- **Synthesia** - $22/mo, Quality 90/100
- **D-ID** - $5.99/mo, Quality 85/100
- **Tavus** - $99/mo, Quality 88/100
- **KreadoAI** - $10/mo, Quality 80/100

### 📱 Reels/Short-form (7 outils)

- **Canva AI** - Freemium, Quality 83/100
- **VEED.IO** - Freemium, Quality 85/100
- **InVideo AI** - Freemium, Quality 82/100
- **OpusClip** - $9.50/mo, Quality 88/100
- **Short AI** - $19/mo, Quality 84/100

## 🔧 Architecture

```
┌─────────────────────────────────────────────────┐
│  Frontend (index-ultimate.html)                │
│  - Mode Auto / Manuel / Comparaison            │
│  - Sélecteur 40 générateurs                    │
│  - Estimation coût temps réel                  │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│  FastAPI Backend (src/api.py)                  │
│  - 9 endpoints REST                            │
│  - Smart Router (sélection auto)               │
│  - Cost Tracker                                │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│  Generator Registry (40 générateurs)           │
│  ├─ Text-to-Video (17)                         │
│  ├─ Text-to-Image (9)                          │
│  ├─ Avatar Video (5)                           │
│  ├─ Reels (7)                                  │
│  └─ Image-to-Video (2)                         │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│  Pipeline v2 (pipeline_v2.py)                  │
│  1. Script Optimizer (Qwen 2.1)                │
│  2. TTS Generation (Coqui)                     │
│  3. Scene Splitting (AI)                       │
│  4. AI Clips Generation (parallèle)            │
│  5. Subtitle Generation (SRT)                  │
│  6. FFmpeg Assembly                            │
│  7. YouTube Upload                             │
└─────────────────────────────────────────────────┘
```

## 📖 Utilisation

### Mode 1 : Auto-Sélection (Recommandé)

Le Smart Router choisit automatiquement le meilleur générateur :

```python
from src.pipeline_v2 import create_youtube_short

result = await create_youtube_short(
    script="Les 10 merveilles d'Algérie",
    title="Découvrez l'Algérie",
    budget=0.0  # Gratuit uniquement → WAN 2.1
)
```

### Mode 2 : Sélection Manuelle

Choisissez un générateur spécifique :

```python
result = await create_youtube_short(
    script="Top 5 des startups algériennes",
    title="Startups DZ",
    generator="runway_gen4",  # Force Runway Gen-4
    budget=5.0  # Max $5
)
```

### Mode 3 : Comparaison (A/B Testing)

Comparez 4 générateurs côte à côte :

```python
from src.pipeline_v2 import compare_generators

results = await compare_generators(
    script="Innovation en Algérie",
    generators=["wan_2_1", "kling_ai", "runway_gen4", "veo_2"]
)

# results = {
#   "wan_2_1": {"quality_score": 85, "cost": 0.0, "time": 90},
#   "kling_ai": {"quality_score": 90, "cost": 0.0, "time": 120},
#   ...
# }
```

### API REST

#### 1. Lister les générateurs

```bash
curl http://localhost:8200/api/v1/generators/list?category=text-to-video
```

#### 2. Info sur un générateur

```bash
curl http://localhost:8200/api/v1/generators/info/wan_2_1
```

#### 3. Générer une vidéo

```bash
curl -X POST http://localhost:8200/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Sahara desert sunset",
    "category": "text-to-video",
    "duration_seconds": 5,
    "generator_name": "wan_2_1"
  }'
```

#### 4. Vérifier le statut

```bash
curl http://localhost:8200/api/v1/status/TASK_ID
```

#### 5. Pipeline complet (Script → YouTube)

```bash
curl -X POST http://localhost:8200/api/v1/pipeline/full \
  -H "Content-Type: application/json" \
  -d '{
    "script_text": "Bienvenue en Algérie...",
    "title": "Discover Algeria",
    "use_ai_video": true,
    "generator_name": null,
    "publish": true
  }'
```

## 💰 Stratégie de Coûts

### Scénario 1 : 100% Gratuit (0€/mois)

```bash
# .env
FREE_ONLY_MODE=true
DEFAULT_GENERATOR=wan_2_1
```

**Capacité** :
- 100 vidéos/jour (WAN 2.1)
- Qualité : 85/100
- **Coût** : 0€

### Scénario 2 : Freemium Mix ($9.99/mois)

```bash
# .env
DEFAULT_GENERATOR=luma_dream  # $9.99/mo illimité
```

**Capacité** :
- Illimité (Luma Dream)
- Qualité : 90/100
- **Coût** : $9.99/mois

### Scénario 3 : Premium (Pay-as-you-go)

```bash
# .env
DEFAULT_GENERATOR=runway_gen4
MAX_BUDGET_PER_VIDEO=1.0  # Max $1 par vidéo
```

**Capacité** :
- Illimité
- Qualité : 95/100
- **Coût** : ~$0.25/vidéo (5 sec à $0.05/sec)

## 🧪 Tests

```bash
# Tests unitaires
pytest src/tests/test_generators.py -v

# Tests API
pytest src/tests/test_api_generators.py -v

# Tests d'intégration (pipeline complet)
pytest src/tests/test_integration.py -v

# Coverage
pytest --cov=src --cov-report=html
```

## 📊 Métriques

Chaque générateur est noté selon :

- **Quality Score** (0-100) : Réalisme + cohérence
- **Cost** : Prix par seconde de vidéo
- **Speed** : Temps de génération moyen
- **Free Tier** : Quota gratuit disponible

Exemple :

| Générateur | Quality | Cost/sec | Speed | Free Tier |
|-----------|---------|----------|-------|-----------|
| WAN 2.1 | 85 | $0.00 | 90s | 100/jour |
| Runway Gen-4 | 95 | $0.05 | 120s | ❌ |
| Kling AI | 90 | $0.00 | 120s | 66 crédits |
| Veo 2 | 93 | $0.50 | 180s | ❌ |

## 🚀 Déploiement

### Local (Windows/Linux/Mac)

```bash
# Clone
git clone https://github.com/IAFactory/dzirvideo.git
cd dzirvideo

# Configure
cp .env.example .env
# Éditer .env avec vos clés API

# Docker
docker compose up -d

# Ou Python direct
pip install -r requirements.txt
uvicorn src.api:app --host 0.0.0.0 --port 8200
```

### VPS Production

```bash
# Deploy automatique
bash deploy-to-vps.sh

# Ou manuel
ssh root@your-vps
cd /opt/dzirvideo
docker compose build
docker compose up -d
```

Voir [DEPLOYMENT.md](DEPLOYMENT.md) pour détails complets.

## 📚 Documentation

- [DEPLOYMENT.md](DEPLOYMENT.md) - Guide déploiement complet
- [QUICK_DEPLOY.md](QUICK_DEPLOY.md) - Déploiement en 5 minutes
- [FINAL_STATUS.md](FINAL_STATUS.md) - Statut complet du système
- [API Docs](http://localhost:8200/docs) - Documentation Swagger interactive

## 🔐 Sécurité

- **API Keys** : Jamais commitées (`.env` dans `.gitignore`)
- **Rate Limiting** : 60 requêtes/minute par IP
- **CORS** : Configuré pour domaines autorisés uniquement
- **HTTPS** : Obligatoire en production (Nginx + Let's Encrypt)

## 🤝 Contribuer

```bash
# Fork le repo
git clone https://github.com/YOUR_USERNAME/dzirvideo.git

# Créer une branche
git checkout -b feature/nouveau-generateur

# Commit
git commit -m "feat: ajout générateur XYZ"

# Push
git push origin feature/nouveau-generateur

# Créer une Pull Request
```

### Ajouter un nouveau générateur

1. Créer `src/generators/category/new_generator.py`
2. Hériter de `BaseGenerator`
3. Implémenter `_define_capabilities()`, `generate()`, `check_status()`
4. Ajouter dans `registry.py`
5. Tests dans `tests/test_new_generator.py`

Exemple :

```python
from ..base import BaseGenerator, GeneratorCapabilities

class NewGenerator(BaseGenerator):
    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_video=True,
            max_duration_seconds=10.0,
            quality_score=85,
            free_tier=True
        )

    async def generate(self, request):
        # ... votre logique
        pass
```

## 📞 Support

- **Issues** : https://github.com/IAFactory/dzirvideo/issues
- **Email** : support@iafactory.pro
- **Docs** : https://docs.iafactory.pro/dzirvideo

## 📜 License

MIT License - Copyright (c) 2025 IAFactory

## 🙏 Remerciements

Dzir IA Video utilise :

- **Alibaba Cloud** (WAN 2.1, Qwen 2.1) - Générateurs gratuits
- **Coqui TTS** - Text-to-Speech open source
- **FFmpeg** - Traitement vidéo
- **FastAPI** - Framework web moderne
- **Docker** - Containerisation
- Et 40+ plateformes d'IA pour les générateurs

---

**Version** : 2.1.0
**Date** : 2025-12-13
**Auteur** : IAFactory Team
