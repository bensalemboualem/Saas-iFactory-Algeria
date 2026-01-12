# IAF Media-to-Reels Pipeline v1.0

## Architecture n8n

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          TRIGGER LAYER                                               │
│  ┌──────────────┐                                                                   │
│  │   Webhook    │ POST /media-upload                                                │
│  │   (n8n)      │ { youtube_url | file, client_email, slack_channel, delivery }    │
│  └──────┬───────┘                                                                   │
└─────────┼───────────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          INGESTION LAYER                                             │
│                                                                                      │
│  ┌─────────┐         ┌──────────────┐         ┌──────────────┐                      │
│  │   IF    │────────▶│ YouTube DL   │────────▶│              │                      │
│  │ Router  │         │ (yt-dlp)     │         │    MERGE     │                      │
│  │         │────────▶│ File Binary  │────────▶│    Audio     │                      │
│  └─────────┘         └──────────────┘         └──────┬───────┘                      │
│                                                       │                              │
└───────────────────────────────────────────────────────┼──────────────────────────────┘
                                                        │
                                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          PROCESSING LAYER                                            │
│                                                                                      │
│  ┌──────────────────────────────────────────────────────────────────────┐           │
│  │                         WHISPER (STT)                                 │           │
│  │  cockpit.iafactory.ch/api/agent/voice/upload                         │           │
│  │  Input: audio blob | Output: input_text (transcription)              │           │
│  │  Timeout: 120s | Language: auto-detect                               │           │
│  └──────────────────────────────────┬───────────────────────────────────┘           │
│                                     │                                                │
│                    ┌────────────────┴────────────────┐                              │
│                    ▼                                 ▼                              │
│  ┌─────────────────────────────┐   ┌─────────────────────────────┐                  │
│  │      ARCHON (LLM)           │   │        BMAD (RAG)           │                  │
│  │  /api/agent/voice/text      │   │    /api/rag/query           │                  │
│  │                             │   │                             │                  │
│  │  Analyse strategique:       │   │  Collection: bmad_knowledge │                  │
│  │  - Hooks emotionnels        │   │  Top K: 5 documents         │                  │
│  │  - Moments forts            │   │                             │                  │
│  │  - Citations marquantes     │   │  Contexte supplementaire    │                  │
│  └──────────────┬──────────────┘   └──────────────┬──────────────┘                  │
│                 │                                  │                                 │
│                 └──────────────┬───────────────────┘                                │
│                                ▼                                                     │
│  ┌──────────────────────────────────────────────────────────────────────┐           │
│  │                         MERGE ANALYSIS                                │           │
│  │  Combine: Archon output + BMAD context                               │           │
│  └──────────────────────────────────┬───────────────────────────────────┘           │
│                                     │                                                │
└─────────────────────────────────────┼────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          CREATIVE LAYER                                              │
│                                                                                      │
│  ┌──────────────────────────────────────────────────────────────────────┐           │
│  │                      CLAUDE (Anthropic API)                          │           │
│  │  Model: claude-sonnet-4-20250514                                               │           │
│  │  Max Tokens: 4096                                                    │           │
│  │                                                                      │           │
│  │  INPUT:                                                              │           │
│  │  - Transcription complete                                            │           │
│  │  - Analyse strategique Archon                                        │           │
│  │  - Contexte BMAD enrichi                                             │           │
│  │                                                                      │           │
│  │  OUTPUT: 3 Scripts Reels avec:                                       │           │
│  │  ┌─────────────────────────────────────────────────────────────┐    │           │
│  │  │ SCRIPT 1, 2, 3:                                              │    │           │
│  │  │  - HOOK (3s): Phrase d'accroche                              │    │           │
│  │  │  - TENSION (10s): Probleme ou revelation                     │    │           │
│  │  │  - PAYOFF (5s): Solution ou twist                            │    │           │
│  │  │  - CTA (2s): Call to action                                  │    │           │
│  │  │  + Texte overlay exact                                       │    │           │
│  │  │  + Timing precis                                             │    │           │
│  │  │  + Suggestion B-roll/visuel                                  │    │           │
│  │  │  + Style musique                                             │    │           │
│  │  │  + Hashtags optimises                                        │    │           │
│  │  └─────────────────────────────────────────────────────────────┘    │           │
│  └──────────────────────────────────┬───────────────────────────────────┘           │
│                                     │                                                │
└─────────────────────────────────────┼────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          DELIVERY LAYER                                              │
│                                                                                      │
│  ┌─────────────────┐                                                                │
│  │  Parse & Pack   │  Structure JSON finale avec metadata                           │
│  └────────┬────────┘                                                                │
│           │                                                                          │
│           ▼                                                                          │
│  ┌─────────────────┐                                                                │
│  │  Switch Router  │  delivery_method: email | slack | both                         │
│  └────────┬────────┘                                                                │
│           │                                                                          │
│     ┌─────┴─────┬─────────────┐                                                     │
│     ▼           ▼             ▼                                                     │
│  ┌──────┐   ┌───────┐   ┌──────────┐                                               │
│  │ Email│   │ Slack │   │  Both    │                                               │
│  │ SMTP │   │ API   │   │ Parallel │                                               │
│  └──────┘   └───────┘   └──────────┘                                               │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## Nodes n8n Details

| # | Node | Type | Endpoint/Config | Output |
|---|------|------|-----------------|--------|
| 1 | trigger_webhook | Webhook | POST /media-upload | {youtube_url, file, client_email} |
| 2 | detect_input_type | IF | youtube_url.isNotEmpty | Branch routing |
| 3 | youtube_download | HTTP Request | /api/media/youtube-extract | Audio binary |
| 4 | file_to_binary | Move Binary | jsonToBinary | Audio binary |
| 5 | merge_audio | Merge | Multiplex | Unified audio stream |
| 6 | whisper_transcription | HTTP Request | /api/agent/voice/upload | {input_text} |
| 7 | archon_strategic_analysis | HTTP Request | /api/agent/voice/text | {output_text} strategic |
| 8 | bmad_context_fetch | HTTP Request | /api/rag/query | {results} context docs |
| 9 | merge_analysis | Merge | Combine by position | Enriched context |
| 10 | claude_reels_generator | HTTP Request | Anthropic API | 3 scripts JSON |
| 11 | parse_reels_output | Code (JS) | JSON parsing | Structured pack |
| 12 | delivery_router | Switch | delivery_method | Route decision |
| 13 | send_email | Email Send | SMTP | Email confirmation |
| 14 | send_slack | Slack | Slack API | Channel message |
| 15 | response_success | Respond Webhook | JSON | Client confirmation |

## Data Flow BMAD <-> Claude

```
BMAD Knowledge Base                     Claude Generation
     │                                        │
     │  1. Query: transcription text          │
     ▼                                        │
┌─────────────┐                              │
│ RAG Search  │  collection: bmad_knowledge   │
│ top_k: 5    │                              │
└──────┬──────┘                              │
       │                                      │
       │  2. Results: [{doc, score, meta}]    │
       ▼                                      │
┌─────────────────────────────────────────────┴───────┐
│                    MERGE NODE                       │
│                                                     │
│  Combined Payload:                                  │
│  {                                                  │
│    transcription: "...",      <- Whisper           │
│    strategic_analysis: "...", <- Archon            │
│    bmad_context: [            <- BMAD              │
│      { content: "...", relevance: 0.92 },          │
│      { content: "...", relevance: 0.87 }           │
│    ]                                               │
│  }                                                  │
└─────────────────────────┬───────────────────────────┘
                          │
                          │  3. Full context to Claude
                          ▼
┌─────────────────────────────────────────────────────┐
│                  CLAUDE API                         │
│                                                     │
│  System: Expert contenu viral                       │
│  User: "Basé sur TRANSCRIPTION + ANALYSE +          │
│         CONTEXTE BMAD, génère 3 scripts..."        │
│                                                     │
│  Output: JSON structuré 3 Reels                    │
└─────────────────────────────────────────────────────┘
```

## Exemple Payload Webhook

```json
POST /media-upload
{
  "youtube_url": "https://youtube.com/watch?v=xxx",
  "client_email": "client@example.com",
  "slack_channel": "#content-team",
  "delivery_method": "both",
  "options": {
    "language": "fr",
    "style": "business",
    "target_platform": "instagram"
  }
}
```

## Exemple Output Pack

```json
{
  "pack_id": "REELS_1702912345678",
  "created_at": "2025-12-18T14:30:00Z",
  "reels_scripts": [
    {
      "id": 1,
      "title": "Le Secret des Top Performers",
      "structure": {
        "hook": {
          "duration": "3s",
          "text": "Ce que 99% des gens ignorent sur la productivité...",
          "visual": "Face cam, regard intense"
        },
        "tension": {
          "duration": "10s",
          "text": "J'ai analysé 500 entrepreneurs et découvert UN pattern",
          "visual": "B-roll: graphiques, bureau, café"
        },
        "payoff": {
          "duration": "5s",
          "text": "Ils commencent TOUS leur journée par ça",
          "visual": "Reveal moment, transition rapide"
        },
        "cta": {
          "duration": "2s",
          "text": "Follow pour la suite",
          "visual": "Logo + CTA animé"
        }
      },
      "music_style": "Motivational, builds tension",
      "hashtags": ["#productivity", "#entrepreneur", "#mindset", "#success"]
    }
  ],
  "metadata": {
    "source_duration": "5:32",
    "processing_time_ms": 45000,
    "model": "claude-sonnet-4-20250514"
  }
}
```

## Credentials Required

| Service | Credential Type | Notes |
|---------|----------------|-------|
| Anthropic | API Key | claude-sonnet-4-20250514 access |
| Slack | OAuth2 | Bot token avec chat:write |
| SMTP | Username/Password | Pour envoi email |
| IAF Cockpit | API Key (optional) | Si auth requise sur endpoints |

## Installation n8n

```bash
# Import workflow
n8n import:workflow --input=n8n_workflow_media_reels.json

# Set credentials
n8n credential:set anthropicApi
n8n credential:set slackOAuth2Api
n8n credential:set smtp
```
