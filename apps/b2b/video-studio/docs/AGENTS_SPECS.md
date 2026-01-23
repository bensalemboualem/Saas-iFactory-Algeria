# Spécifications des Agents IA - IAFactory Video Studio Pro

## Vue d'Ensemble du Système Multi-Agents

Le Video Studio Pro utilise un système orchestré de 5 agents IA spécialisés, chacun avec un rôle précis dans la chaîne de production de contenu.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATEUR PRINCIPAL                          │
│                                                                     │
│  Input Utilisateur ──► Analyse ──► Routage ──► Agents ──► Output   │
└─────────────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
   ┌─────────┐            ┌─────────┐            ┌─────────┐
   │SCÉNARIST│──────────► │STORYBOAR│──────────► │DIRECTOR │
   │         │            │         │            │         │
   └─────────┘            └─────────┘            └─────────┘
                                                      │
                          ┌───────────────────────────┤
                          ▼                           ▼
                    ┌─────────┐                 ┌─────────┐
                    │ GROWTH  │                 │DISTRIBUT│
                    │ HACKER  │                 │         │
                    └─────────┘                 └─────────┘
```

---

## Agent 1: Scénariste (Scriptwriter)

### Configuration
```python
SCRIPTWRITER_CONFIG = {
    "model": "claude-opus-4-20250514",
    "temperature": 0.8,  # Créativité élevée
    "max_tokens": 8000,
    "capabilities": [
        "script_generation",
        "viral_hooks",
        "content_segmentation",
        "multilingual"
    ]
}
```

### System Prompt
```markdown
Tu es un scénariste expert en création de contenu viral pour les réseaux sociaux.

## Ton expertise:
- Création de hooks captivants (3 premières secondes)
- Scripts optimisés pour YouTube, TikTok et Instagram Reels
- Storytelling émotionnel et engageant
- Connaissance des tendances actuelles
- Maîtrise du français, arabe et dialecte algérien (Darija)

## Format de sortie obligatoire:
Pour chaque script, tu fournis:

1. **HOOK** (0-3 secondes)
   - Phrase d'accroche percutante
   - Question provocante OU statistique choquante OU affirmation contre-intuitive

2. **INTRO** (3-15 secondes)
   - Présentation du sujet
   - Promesse de valeur

3. **SEGMENTS** (avec timestamps)
   - Chaque segment: timestamp_start, timestamp_end, contenu, direction_visuelle
   - Inclure des moments "viraux" identifiés pour les Shorts

4. **OUTRO** (dernières 10 secondes)
   - Récapitulatif
   - Call-to-action

5. **METADATA**
   - 5 titres optimisés
   - 10 hashtags pertinents
   - Description SEO
   - Score de viralité estimé (0-100)

## Règles:
- Chaque phrase doit pouvoir être visualisée
- Éviter le jargon technique sauf si expliqué
- Inclure des questions rhétoriques pour l'engagement
- Varier le rythme (tension/relâchement)
- Pour le contenu algérien: intégrer des expressions locales authentiques
```

### Fonctions Principales
```python
class ScriptwriterAgent:
    async def generate_script(
        self,
        topic: str,
        target_audience: str,
        platform: Platform,
        duration: int,
        language: Language,
        tone: Tone = "engaging"
    ) -> VideoScript:
        """Génère un script complet optimisé pour la plateforme cible."""
        
    async def generate_hook_variations(
        self,
        topic: str,
        count: int = 5
    ) -> List[str]:
        """Génère plusieurs variations de hooks pour A/B testing."""
        
    async def extract_shorts(
        self,
        full_script: VideoScript,
        count: int = 3
    ) -> List[ShortScript]:
        """Extrait les meilleurs moments pour des Shorts viraux."""
        
    async def localize_script(
        self,
        script: VideoScript,
        target_language: Language,
        cultural_context: str
    ) -> VideoScript:
        """Adapte le script à une autre langue/culture."""
```

### Exemple d'Output
```json
{
  "id": "script_abc123",
  "title": "L'IA va-t-elle remplacer les médecins en Algérie ?",
  "hook": "En 2025, un algorithme diagnostique le cancer mieux qu'un médecin algérien. Voici pourquoi c'est une bonne nouvelle.",
  "intro": "Salam ! Aujourd'hui, on va parler d'un sujet qui fait débat : l'intelligence artificielle dans nos hôpitaux.",
  "segments": [
    {
      "timestamp_start": 0.0,
      "timestamp_end": 15.0,
      "content": "...",
      "speaker": "host",
      "visual_direction": "Animation statistiques santé Algérie"
    }
  ],
  "viral_moments": [
    {"timestamp": 45.0, "reason": "Révélation choquante"},
    {"timestamp": 120.0, "reason": "Témoignage émotionnel"}
  ],
  "viral_score": 78,
  "suggested_hashtags": ["#IAAlgérie", "#SantéDZ", "#TechDZ"]
}
```

---

## Agent 2: Storyboarder

### Configuration
```python
STORYBOARDER_CONFIG = {
    "model": "claude-sonnet-4-20250514",
    "temperature": 0.6,
    "image_model": "fal-ai/flux/schnell",
    "video_model": "minimax",
    "capabilities": [
        "scene_decomposition",
        "visual_generation",
        "thumbnail_creation",
        "b_roll_suggestion"
    ]
}
```

### System Prompt
```markdown
Tu es un directeur artistique spécialisé dans le contenu vidéo digital.

## Ton rôle:
- Découper les scripts en scènes visuelles
- Suggérer des visuels percutants pour chaque segment
- Créer des prompts optimisés pour la génération d'images/vidéos
- Designer des thumbnails qui maximisent le CTR

## Pour chaque scène, tu fournis:
1. **Description visuelle** détaillée
2. **Prompt pour génération IA** (optimisé pour Flux/MiniMax)
3. **Type de plan** (close-up, wide, medium, etc.)
4. **Mouvement caméra** suggéré
5. **Palette de couleurs**
6. **B-roll suggestions** (2-3 alternatives)

## Règles visuelles:
- Contraste élevé pour les thumbnails
- Expressions faciales expressives
- Texte lisible sur mobile
- Cohérence visuelle entre les scènes
- Pour le contenu algérien: intégrer des éléments visuels locaux
```

### Fonctions Principales
```python
class StoryboarderAgent:
    async def decompose_script(
        self,
        script: VideoScript
    ) -> List[Scene]:
        """Découpe le script en scènes avec directions visuelles."""
        
    async def generate_scene_visual(
        self,
        scene: Scene,
        style: VisualStyle
    ) -> GeneratedVisual:
        """Génère le visuel pour une scène."""
        
    async def create_thumbnail(
        self,
        script: VideoScript,
        variations: int = 3
    ) -> List[Thumbnail]:
        """Crée des thumbnails optimisées pour le CTR."""
        
    async def suggest_broll(
        self,
        scene: Scene,
        style: str
    ) -> List[BRollSuggestion]:
        """Suggère des B-rolls pertinents."""
```

---

## Agent 3: Réalisateur (Director)

### Configuration
```python
DIRECTOR_CONFIG = {
    "ffmpeg_path": "/usr/bin/ffmpeg",
    "output_formats": {
        "youtube": {"width": 1920, "height": 1080, "fps": 30},
        "tiktok": {"width": 1080, "height": 1920, "fps": 30},
        "instagram": {"width": 1080, "height": 1920, "fps": 30},
        "square": {"width": 1080, "height": 1080, "fps": 30}
    },
    "subtitle_styles": {
        "default": {"font": "Arial", "size": 48, "color": "white"},
        "arabic": {"font": "Noto Sans Arabic", "size": 52, "rtl": True}
    }
}
```

### Fonctions Principales
```python
class DirectorAgent:
    async def assemble_video(
        self,
        project: VideoProject
    ) -> str:
        """Assemble tous les assets en vidéo finale."""
        
    async def add_subtitles(
        self,
        video_path: str,
        subtitles: SubtitleTrack,
        language: Language
    ) -> str:
        """Ajoute les sous-titres avec support RTL."""
        
    async def apply_transitions(
        self,
        clips: List[VideoClip],
        transition_type: str = "crossfade"
    ) -> str:
        """Applique les transitions entre clips."""
        
    async def render_multiformat(
        self,
        video_path: str,
        formats: List[str]
    ) -> Dict[str, str]:
        """Rend la vidéo en plusieurs formats."""
        
    async def extract_shorts(
        self,
        video_path: str,
        timestamps: List[Tuple[float, float]]
    ) -> List[str]:
        """Extrait les Shorts à partir de la vidéo longue."""
```

### Pipeline FFmpeg
```python
FFMPEG_PIPELINE = """
# Assemblage vidéo + audio + musique
ffmpeg -i video.mp4 -i voiceover.mp3 -i music.mp3 \
    -filter_complex "[1:a]volume=1.0[voice];[2:a]volume=0.3[music];[voice][music]amix=inputs=2[audio]" \
    -map 0:v -map "[audio]" \
    -c:v libx264 -preset fast -crf 23 \
    -c:a aac -b:a 128k \
    output.mp4

# Ajout sous-titres arabes (RTL)
ffmpeg -i input.mp4 \
    -vf "subtitles=subs.srt:force_style='FontName=Noto Sans Arabic,FontSize=24,Alignment=2'" \
    output_subtitled.mp4

# Conversion 16:9 vers 9:16 (TikTok)
ffmpeg -i input_16_9.mp4 \
    -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
    output_9_16.mp4
"""
```

---

## Agent 4: Growth Hacker

### Configuration
```python
GROWTH_HACKER_CONFIG = {
    "model": "grok-4.1-fast",  # Rapidité pour l'analyse
    "analytics_apis": [
        "youtube_analytics",
        "tiktok_insights",
        "instagram_insights"
    ],
    "ab_test_variations": 5
}
```

### System Prompt
```markdown
Tu es un expert en croissance et viralité sur les réseaux sociaux.

## Ton expertise:
- Analyse des tendances virales
- Optimisation des titres et descriptions
- Stratégie de hashtags
- Timing de publication optimal
- A/B testing

## Pour chaque contenu, tu fournis:
1. **Score de viralité prédictif** (0-100)
2. **5 variations de titres** classées par potentiel
3. **10 hashtags** par plateforme
4. **Meilleur moment de publication**
5. **Recommandations d'amélioration**

## Critères d'analyse:
- Émotions déclenchées
- Partageabilité
- Commentabilité
- Rétention prédite
- Potentiel de débat
```

### Fonctions Principales
```python
class GrowthHackerAgent:
    async def analyze_viral_potential(
        self,
        script: VideoScript
    ) -> ViralAnalysis:
        """Analyse le potentiel viral du contenu."""
        
    async def generate_title_variations(
        self,
        script: VideoScript,
        count: int = 5
    ) -> List[TitleVariation]:
        """Génère des variations de titres optimisés."""
        
    async def optimize_hashtags(
        self,
        content: str,
        platform: Platform
    ) -> List[Hashtag]:
        """Optimise les hashtags pour la plateforme."""
        
    async def recommend_posting_time(
        self,
        platform: Platform,
        audience: str,
        timezone: str
    ) -> datetime:
        """Recommande le meilleur moment de publication."""
```

---

## Agent 5: Distributeur

### Configuration
```python
DISTRIBUTOR_CONFIG = {
    "n8n_url": "http://localhost:5678",
    "platforms": {
        "youtube": {
            "api": "youtube_data_api_v3",
            "upload_endpoint": "/upload"
        },
        "tiktok": {
            "api": "tiktok_creator_api",
            "upload_endpoint": "/content/publish"
        },
        "instagram": {
            "api": "instagram_graph_api",
            "upload_endpoint": "/media"
        }
    }
}
```

### Fonctions Principales
```python
class DistributorAgent:
    async def publish_youtube(
        self,
        video_path: str,
        metadata: VideoMetadata
    ) -> PublishResult:
        """Publie sur YouTube avec métadonnées optimisées."""
        
    async def publish_tiktok(
        self,
        video_path: str,
        metadata: ShortMetadata
    ) -> PublishResult:
        """Publie sur TikTok."""
        
    async def publish_instagram(
        self,
        video_path: str,
        metadata: ReelMetadata
    ) -> PublishResult:
        """Publie sur Instagram Reels."""
        
    async def schedule_publication(
        self,
        video_path: str,
        platforms: List[Platform],
        schedule: datetime
    ) -> List[ScheduledPost]:
        """Planifie la publication multi-plateformes."""
        
    async def cross_post(
        self,
        content: VideoContent,
        platforms: List[Platform]
    ) -> CrossPostResult:
        """Publication simultanée multi-plateformes."""
```

### Workflow n8n
```json
{
  "name": "Video Publication Workflow",
  "nodes": [
    {
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "/publish-video"
      }
    },
    {
      "name": "Upload YouTube",
      "type": "n8n-nodes-base.youtube",
      "parameters": {
        "operation": "upload",
        "title": "={{$json.title}}",
        "description": "={{$json.description}}"
      }
    },
    {
      "name": "Notify Success",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#video-studio",
        "message": "Video published: {{$json.url}}"
      }
    }
  ]
}
```

---

## Orchestration Multi-Agents

### Séquence de Production
```python
async def orchestrate_video_production(
    topic: str,
    config: ProductionConfig
) -> VideoProject:
    """
    Orchestre la production complète d'une vidéo.
    """
    # 1. Génération du script
    scriptwriter = ScriptwriterAgent()
    script = await scriptwriter.generate_script(
        topic=topic,
        platform=config.platform,
        duration=config.duration,
        language=config.language
    )
    
    # 2. Storyboarding
    storyboarder = StoryboarderAgent()
    scenes = await storyboarder.decompose_script(script)
    
    # 3. Génération parallèle des assets
    assets = await asyncio.gather(
        generate_video_clips(scenes),
        generate_voiceover(script),
        generate_music(script.mood)
    )
    
    # 4. Montage
    director = DirectorAgent()
    video = await director.assemble_video(
        clips=assets[0],
        voiceover=assets[1],
        music=assets[2]
    )
    
    # 5. Optimisation
    growth_hacker = GrowthHackerAgent()
    optimization = await growth_hacker.analyze_viral_potential(script)
    
    # 6. Extraction Shorts
    shorts = await director.extract_shorts(
        video,
        script.viral_moments
    )
    
    return VideoProject(
        main_video=video,
        shorts=shorts,
        optimization=optimization
    )
```
