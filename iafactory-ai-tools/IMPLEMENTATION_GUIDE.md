# 📋 Template d'implémentation des endpoints restants

Ce document te guide pour implémenter les 6 autres outils en suivant exactement le même pattern que `translator.py`.

---

## ✅ Déjà implémenté

1. **Translation** - `/api/v1/translator/*`
   - ✅ `POST /translate` - Traduction simple
   - ✅ `POST /translate/batch` - Traduction par lot
   - ✅ `GET /languages` - Langues supportées
   - ✅ `GET /health` - Santé du service

---

## 🔨 À implémenter

### 2. Speech-to-Text

**Fichier**: `backend/app/api/v1/endpoints/speech_to_text.py`

```python
"""
Speech-to-Text API Endpoint
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.services.ai_providers.openai_service import OpenAIService
from app.models.responses import SpeechToTextResponse

router = APIRouter(prefix="/speech-to-text", tags=["Speech-to-Text"])

@router.post("/transcribe", response_model=SpeechToTextResponse)
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: Optional[str] = None,
    service: OpenAIService = Depends(get_openai_service)
):
    """Transcribe audio file to text"""
    # Validation du format
    # Appel du service OpenAI Whisper
    # Retour de la transcription
    pass
```

**Points clés**:
- Upload de fichiers avec `UploadFile`
- Validation des formats audio (mp3, wav, m4a, etc.)
- Limite de taille: 25MB
- Support multilingue (FR/AR/EN)

---

### 3. Text Generator

**Fichier**: `backend/app/api/v1/endpoints/text_generator.py`

```python
"""
Text Generation API Endpoint
"""
from fastapi import APIRouter, Depends
from app.models.requests import TextGenerationRequest
from app.models.responses import TextGenerationResponse

router = APIRouter(prefix="/text-generator", tags=["Text Generation"])

@router.post("/generate", response_model=TextGenerationResponse)
async def generate_text(
    request: TextGenerationRequest,
    service: OpenAIService = Depends(get_openai_service)
):
    """Generate text from prompt"""
    pass

@router.post("/improve", response_model=TextImprovementResponse)
async def improve_text(
    request: TextImprovementRequest,
    service: OpenAIService = Depends(get_openai_service)
):
    """Improve/rewrite existing text"""
    pass
```

**Points clés**:
- Différents styles (professional, casual, creative, etc.)
- Support multilingue
- Contrôle de la température (créativité)
- Limite de tokens

---

### 4. Image Generator

**Fichier**: `backend/app/api/v1/endpoints/image_generator.py`

```python
"""
Image Generation API Endpoint
"""
from fastapi import APIRouter, Depends
from app.models.requests import ImageGenerationRequest
from app.models.responses import ImageGenerationResponse

router = APIRouter(prefix="/image-generator", tags=["Image Generation"])

@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_image(
    request: ImageGenerationRequest,
    service: OpenAIService = Depends(get_openai_service)
):
    """Generate image from text prompt"""
    # Génération via DALL-E 3
    # Stockage de l'image sur S3
    # Retour de l'URL
    pass

@router.post("/batch", response_model=BatchImageGenerationResponse)
async def batch_generate_images(
    request: BatchImageGenerationRequest,
    service: OpenAIService = Depends(get_openai_service)
):
    """Generate multiple images"""
    pass
```

**Points clés**:
- Choix de la taille (1024x1024, etc.)
- Style (vivid vs natural)
- Qualité (standard vs HD)
- Stockage des images générées

---

### 5. Background Remover

**Fichier**: `backend/app/api/v1/endpoints/background_remover.py`

```python
"""
Background Removal API Endpoint
"""
from fastapi import APIRouter, UploadFile, File, Depends
from app.services.ai_providers.background_removal_service import BackgroundRemovalService
from app.models.responses import BackgroundRemovalResponse

router = APIRouter(prefix="/background-remover", tags=["Background Removal"])

@router.post("/remove", response_model=BackgroundRemovalResponse)
async def remove_background(
    image: UploadFile = File(...),
    return_mask: bool = False,
    service: BackgroundRemovalService = Depends(get_background_service)
):
    """Remove background from image"""
    # Utilise rembg (gratuit)
    # Retour de l'image sans fond
    pass
```

**Points clés**:
- Utilise rembg (open-source, gratuit)
- Retour en PNG avec transparence
- Option de retourner le masque
- Alpha matting pour de meilleurs bords

---

### 6. Image Upscaler

**Fichier**: `backend/app/api/v1/endpoints/image_upscaler.py`

**Service**: Créer `backend/app/services/ai_providers/image_upscaler_service.py`

```python
"""
Image Upscaling API Endpoint
"""
from fastapi import APIRouter, UploadFile, File
from app.models.responses import ImageUpscaleResponse

router = APIRouter(prefix="/image-upscaler", tags=["Image Upscaling"])

@router.post("/upscale", response_model=ImageUpscaleResponse)
async def upscale_image(
    image: UploadFile = File(...),
    scale_factor: int = 2
):
    """Upscale image 2x, 3x, or 4x"""
    # Utilise Replicate API ou Real-ESRGAN local
    pass
```

**Options d'implémentation**:
1. **Replicate API** (payant mais facile)
2. **Real-ESRGAN local** (gratuit mais nécessite GPU)

---

### 7. Image Transformer (Image-to-Image)

**Fichier**: `backend/app/api/v1/endpoints/image_transformer.py`

```python
"""
Image-to-Image Transformation API Endpoint
"""
from fastapi import APIRouter, UploadFile, File
from app.models.requests import ImageToImageRequest
from app.models.responses import ImageToImageResponse

router = APIRouter(prefix="/image-transformer", tags=["Image Transformation"])

@router.post("/transform", response_model=ImageToImageResponse)
async def transform_image(
    image: UploadFile = File(...),
    prompt: str,
    strength: float = 0.8
):
    """Transform image based on text prompt"""
    # Utilise Stable Diffusion img2img
    # Via Replicate API ou local
    pass
```

---

## 🔄 Checklist pour chaque endpoint

Pour chaque nouveau endpoint, suis cette checklist:

### 1. Créer le fichier endpoint
```bash
touch backend/app/api/v1/endpoints/[nom_outil].py
```

### 2. Copier la structure de `translator.py`
- Router FastAPI
- Dependencies
- Error handling
- Logging

### 3. Ajouter au router principal
```python
# Dans backend/app/api/v1/router.py
from app.api.v1.endpoints import [nom_outil]
api_router.include_router([nom_outil].router)
```

### 4. Créer/adapter le service si nécessaire
```bash
touch backend/app/services/ai_providers/[nom_service].py
```

### 5. Tester l'endpoint
```python
# Ajouter un test dans test_api.py
def test_[nom_outil]():
    response = requests.post(f"{BASE_URL}/[nom_outil]/...")
    assert response.status_code == 200
```

### 6. Documenter dans Swagger
- Les endpoints apparaissent automatiquement dans `/api/v1/docs`

---

## 💡 Services à créer

En plus d'OpenAI, tu auras besoin de:

### BackgroundRemovalService (déjà fait)
- Utilise rembg (gratuit)
- Localisé dans: `services/ai_providers/background_removal_service.py`

### ImageUpscalerService (à créer)
```python
# backend/app/services/ai_providers/image_upscaler_service.py
class ImageUpscalerService:
    async def upscale(self, image_bytes, scale_factor):
        # Option 1: Replicate API
        # Option 2: Real-ESRGAN local
        pass
```

### StabilityAIService (à créer)
```python
# backend/app/services/ai_providers/stability_service.py
class StabilityAIService:
    async def image_to_image(self, image, prompt, strength):
        # Pour image transformation
        pass
```

---

## 📦 Dépendances additionnelles

Si tu veux utiliser des modèles locaux (gratuit mais nécessite GPU):

```bash
# Pour Whisper local
pip install openai-whisper torch torchaudio

# Pour Stable Diffusion local
pip install diffusers transformers accelerate

# Pour Real-ESRGAN local
pip install realesrgan
```

---

## 🚀 Ordre d'implémentation recommandé

1. ✅ Translation (fait)
2. 🔥 Speech-to-Text (priorité haute pour École Nouvelle Horizon)
3. 🔥 Text Generator (core feature pour RAG)
4. Image Generator (valeur ajoutée marketing)
5. Background Remover (facile, déjà le service)
6. Image Upscaler
7. Image Transformer

---

## 🎯 Gain de temps

Pour aller vite:
1. Copie `translator.py`
2. Remplace les noms
3. Adapte la logique métier
4. Test et itère

**Temps estimé par endpoint**: 1-2 heures si tu suis le pattern.

---

Bon dev ! 🚀
