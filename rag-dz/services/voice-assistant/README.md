# 🎙️ DZ-VoiceAssistant

**Assistant vocal pour IAFactory Algeria** — Support Français + Darija (arabe algérien)

## 🎯 Fonctionnalités

- **Speech-to-Text (STT)** : Transcription vocale via GROQ Whisper
- **Text-to-Speech (TTS)** : Synthèse vocale via Edge TTS (Microsoft)
- **Multilingue** : Français et Darija (arabe algérien)
- **Routage intelligent** : Connexion aux assistants RAG, Legal, Fiscal, Park
- **Interface web moderne** : UI responsive avec visualisation audio

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (HTML/JS)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ MediaRecorder│  │ Audio Play  │  │ Target Selection        │  │
│  │ (WebM/Opus)  │  │ (MP3 Base64)│  │ RAG/Legal/Fiscal/Park   │  │
│  └──────┬──────┘  └──────▲──────┘  └───────────┬─────────────┘  │
└─────────┼────────────────┼─────────────────────┼────────────────┘
          │                │                     │
          ▼                │                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Backend FastAPI (Port 8201)                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ POST /stt   │  │ POST /tts   │  │ POST /route             │  │
│  │ Audio→Text  │  │ Text→Audio  │  │ Question→Assistant→Reply│  │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘  │
│         │                │                     │                 │
│         ▼                ▼                     ▼                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ GROQ Whisper│  │ Edge TTS    │  │ Internal HTTP Calls     │  │
│  │ (API Cloud) │  │ (Microsoft) │  │ RAG/Legal/Fiscal APIs   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 📡 Endpoints API

### `POST /api/voice/stt`
Convertit l'audio en texte (Speech-to-Text)

**Request:** `multipart/form-data`
- `audio`: Fichier audio (webm, ogg, wav, mp3)
- `language`: `auto` | `fr` | `ar`

**Response:**
```json
{
  "text": "Bonjour, quels sont les impôts pour un freelance?",
  "language_detected": "fr",
  "confidence": 0.95
}
```

### `POST /api/voice/route`
Route la question vers l'assistant approprié

**Request:**
```json
{
  "text": "Quels sont les impôts pour 5 millions de dinars?",
  "target": "fiscal",
  "options": {
    "language": "auto",
    "return_audio": true
  }
}
```

**Response:**
```json
{
  "text_answer": "En tant que freelance...",
  "audio_base64": "//uQxAAAAAANIA...",
  "source_module": "fiscal",
  "meta": { "status": "ok", "has_audio": true }
}
```

### `POST /api/voice/tts`
Convertit le texte en audio (Text-to-Speech)

**Request:**
```json
{
  "text": "Bonjour, je suis l'assistant vocal",
  "language": "fr",
  "voice": "female"
}
```

**Response:**
```json
{
  "audio_base64": "//uQxAAAAAANIA...",
  "format": "mp3",
  "duration_estimate": 3.5
}
```

## 🔧 Configuration

### Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `GROQ_API_KEY` | Clé API GROQ pour Whisper | (requis) |
| `STT_PROVIDER` | Provider STT : `groq`, `openai` | `groq` |
| `TTS_PROVIDER` | Provider TTS : `edge`, `openai` | `edge` |
| `RAG_DZ_URL` | URL du service RAG | `http://iaf-rag-prod:3000` |
| `LEGAL_API_URL` | URL de l'assistant juridique | `http://iaf-legal-assistant-prod:8197` |
| `FISCAL_API_URL` | URL de l'assistant fiscal | `http://iaf-fiscal-assistant-prod:8199` |

### Voix disponibles

**Français:**
- `fr-FR-DeniseNeural` (female, default)
- `fr-FR-HenriNeural` (male)

**Arabe Algérien:**
- `ar-DZ-AminaNeural` (female, default)
- `ar-DZ-IsmaelNeural` (male)

## 🚀 Déploiement

### Docker

```bash
# Build
docker build -t iaf-voice-assistant-api:latest .

# Run
docker run -d \
  --name iaf-voice-assistant-prod \
  --network iaf-prod-network \
  -p 8201:8201 \
  -e GROQ_API_KEY=gsk_xxx \
  -e RAG_DZ_URL=http://iaf-rag-prod:3000 \
  -e LEGAL_API_URL=http://iaf-legal-assistant-prod:8197 \
  -e FISCAL_API_URL=http://iaf-fiscal-assistant-prod:8199 \
  --restart unless-stopped \
  iaf-voice-assistant-api:latest
```

### Nginx

```nginx
# API Voice
location /api/voice/ {
    proxy_pass http://127.0.0.1:8201/api/voice/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 120s;
    client_max_body_size 25M;  # Pour les fichiers audio
}

# Frontend Voice
location /voice {
    rewrite ^/voice$ /voice/ permanent;
}
location /voice/ {
    proxy_pass http://127.0.0.1:8202/;
    proxy_http_version 1.1;
    proxy_set_header Host localhost;
}
```

## 📱 Utilisation Frontend

1. Ouvrir `https://www.iafactoryalgeria.com/voice/`
2. Cliquer sur le bouton 🎤 pour parler
3. Parler en français ou en darija
4. Voir la transcription, modifier si besoin
5. Choisir l'assistant (RAG, Juridique, Fiscal, Park)
6. Cliquer "Envoyer"
7. Lire ou écouter la réponse 🔊

## ⚠️ Limitations

- **Durée audio max** : 60 secondes par enregistrement
- **Taille fichier max** : 25 MB
- **Langues** : Français natif, Darija partiellement (arabe standard)
- **TTS** : Pas de voix darija native (utilise arabe standard DZ)

## 🔮 Évolutions futures

- [ ] Whisper local pour réduire les coûts
- [ ] Voix TTS darija custom (fine-tuning)
- [ ] Mode "push-to-talk" continu
- [ ] Historique des conversations vocales
- [ ] Widget flottant pour toutes les pages

## 📄 Licence

MIT — IAFactory Algeria 2024
