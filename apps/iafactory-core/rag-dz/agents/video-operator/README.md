# IA Factory Video Operator

Agent de montage vidéo automatisé - 100% IA Factory, trilingue (FR/AR/EN).

## 🎯 Fonctionnalités

- **Analyse automatique** : Détection de scènes, moments clés, motion
- **Montage intelligent** : Sélection des meilleurs segments
- **Multi-plateforme** : Export Instagram Reels, TikTok, YouTube Shorts
- **Sous-titres** : Génération automatique (Whisper)
- **Trilingue** : Français, Arabe, Anglais

## 🏗️ Architecture

```
VideoOperatorAgent
├── ANALYZE  → Détection scènes + transcription + motion
├── PLAN     → Sélection segments + planning cuts
├── EXECUTE  → FFmpeg processing
└── EXPORT   → Multi-platform resize
```

## 🚀 Démarrage rapide

### Installation locale

```bash
# Installer les dépendances
pip install -r requirements.txt

# Installer FFmpeg (si pas installé)
# Ubuntu/Debian:
sudo apt install ffmpeg

# macOS:
brew install ffmpeg

# Lancer l'API
python api.py
```

### Docker

```bash
docker build -t iafactory-video-operator .
docker run -p 8080:8080 -v /data:/opt/iafactory-rag-dz iafactory-video-operator
```

## 📡 API Endpoints

### Créer un job de montage

```bash
curl -X POST http://localhost:8080/api/v1/edit \
  -F "video=@input.mp4" \
  -F "target_duration=15" \
  -F "platforms=instagram_reels,tiktok" \
  -F "add_captions=true" \
  -F "language=fr"
```

**Réponse:**
```json
{
  "job_id": "a1b2c3d4",
  "status": "pending",
  "message": "Job créé. Traitement en cours..."
}
```

### Vérifier le statut

```bash
curl http://localhost:8080/api/v1/status/a1b2c3d4
```

**Réponse:**
```json
{
  "id": "a1b2c3d4",
  "status": "completed",
  "progress": 100,
  "message": "Montage terminé!",
  "outputs": {
    "instagram_reels": "/outputs/edited_a1b2c3d4_instagram_reels.mp4",
    "tiktok": "/outputs/edited_a1b2c3d4_tiktok.mp4"
  }
}
```

### Télécharger la vidéo

```bash
curl -O http://localhost:8080/api/v1/download/a1b2c3d4/instagram_reels
```

## 💻 Utilisation CLI

```bash
# Montage simple (15 sec, Instagram)
python video_operator.py input.mp4

# Personnalisé
python video_operator.py input.mp4 \
  --duration 30 \
  --platform tiktok \
  --captions \
  --output /my/output/dir
```

## 📊 Plateformes supportées

| Plateforme | Ratio | Durée max |
|------------|-------|-----------|
| Instagram Reels | 9:16 | 90s |
| TikTok | 9:16 | 180s |
| YouTube Shorts | 9:16 | 60s |
| Square (Feed) | 1:1 | 60s |

## 🎨 Templates

- **algerian_minimal** : Style épuré 🇩🇿
- **product_demo** : Démo produit 📦
- **food_promo** : Restaurant/Food 🍽️
- **cinematic** : Style film 🎬
- **energetic** : Rythme rapide ⚡

## 🔧 Configuration

Variables d'environnement :

```env
UPLOAD_DIR=/opt/iafactory-rag-dz/uploads/video-operator
OUTPUT_DIR=/opt/iafactory-rag-dz/outputs/video-operator
MAX_FILE_SIZE=524288000  # 500MB
ANTHROPIC_API_KEY=sk-...  # Pour Claude (optionnel)
OPENAI_API_KEY=sk-...     # Pour Whisper (optionnel)
```

## 📈 Roadmap

### Sprint 1 (Semaines 1-3) ✅
- [x] FFmpeg wrapper
- [x] Scene detection
- [x] Basic editing agent
- [x] FastAPI backend

### Sprint 2 (Semaines 4-6)
- [ ] Whisper integration (STT)
- [ ] Emotion detection
- [ ] Trending audio sync
- [ ] Color grading

### Sprint 3 (Semaines 7-9)
- [ ] Web UI
- [ ] Batch processing
- [ ] Analytics dashboard

### Sprint 4 (Semaines 10-12)
- [ ] GPU optimization
- [ ] Load testing
- [ ] Production deployment

## 💰 Pricing Model

### Algérie (Volume)
- Free: 3 reels/mois
- Starter: 500 DA/mois (20 reels)
- Pro: 2,000 DA/mois (100 reels)

### Algérie (Premium)
- Pro: DZD 9900/mois (50 reels)
- Enterprise: DZD 199900/mois (unlimited)

## 🤝 Intégration avec Dzir IA Video

Ce module s'intègre avec l'app Dzir IA Video :
1. VEO 3 génère les clips
2. Video Operator les monte automatiquement
3. Export vers toutes les plateformes

---

**IA Factory Algeria** 🇩🇿
