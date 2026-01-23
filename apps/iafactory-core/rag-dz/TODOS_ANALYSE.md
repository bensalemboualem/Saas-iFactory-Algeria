# ANALYSE DES TODOs NON RESOLUS - IAFactory RAG-DZ
**Date:** 2025-12-27
**Total TODOs identifiés:** 83

---

## RESUME PAR CRITICITE

| Criticité | Quantité | Effort total estimé |
|-----------|----------|---------------------|
| CRITIQUE | 12 | ~16h |
| IMPORTANT | 28 | ~24h |
| MINEUR | 43 | ~12h |

---

## TODOs CRITIQUES (Production bloquée)

### TODO #1 - [CRITIQUE] Knowledge Base API - Stub complet
**Fichier:** `services/api/app/routers/knowledge.py:23-55`
**Contexte:** Toutes les routes `/api/knowledge-items/*` sont des stubs
**TODO actuel:**
```python
# TODO: Implement with real database query
# TODO: Implement with real database
# TODO: Implement knowledge item creation
# TODO: Implement deletion
```
**Impact:** L'intégration Archon UI ne fonctionne pas
**Effort estimé:** 2h
**Solution:** Implémenter avec PostgreSQL + modèle KnowledgeItem

---

### TODO #2 - [CRITIQUE] Mobile Pairing - Token DB
**Fichier:** `services/api/app/life_assistant/mobile_router.py:132`
**Contexte:** Fonction `create_mobile_pairing()`
**TODO actuel:**
```python
# TODO: Save to database (mobile_device_pairings table)
```
**Impact:** L'appairage mobile ne persiste pas (perdu au redémarrage)
**Effort estimé:** 1h
**Solution:** Créer table `mobile_device_pairings` + repository

---

### TODO #3 - [CRITIQUE] Mobile Token Validation
**Fichier:** `services/api/app/life_assistant/mobile_router.py:203`
**Contexte:** Fonction `connect_mobile_device()`
**TODO actuel:**
```python
# TODO: Validate token from database
```
**Impact:** Sécurité mobile compromise (tokens non validés)
**Effort estimé:** 30min
**Solution:** Implémenter validation token + expiration

---

### TODO #4 - [CRITIQUE] Billing Webhook Signatures
**Fichier:** `services/api/app/routers/billing_v2.py:510,530`
**Contexte:** Webhooks Chargily/Stripe
**TODO actuel:**
```python
# TODO: Vérifier la signature Chargily
# TODO: Vérifier la signature Stripe
```
**Impact:** SECURITE - Webhooks paiement non sécurisés!
**Effort estimé:** 2h
**Solution:** Implémenter HMAC verification selon docs Chargily/Stripe

---

### TODO #5 - [CRITIQUE] Voice Agent - BIG RAG Integration
**Fichier:** `services/api/app/voice/voice_agent_service.py:515`
**Contexte:** Fonction principale voice agent
**TODO actuel:**
```python
# TODO: Implémenter appel BIG RAG
```
**Impact:** Voice agent ne fait pas de RAG
**Effort estimé:** 2h
**Solution:** Appeler `hybrid_search.py` depuis voice service

---

### TODO #6 - [CRITIQUE] Payment Email Confirmation
**Fichier:** `services/api/app/routers/payment.py:315,328`
**Contexte:** Webhook payment success
**TODO actuel:**
```python
# TODO: Envoyer email confirmation
# TODO: Notifier user (email)
```
**Impact:** Utilisateurs ne reçoivent pas confirmation paiement
**Effort estimé:** 1h
**Solution:** Intégrer notification_service existant

---

### TODO #7 - [CRITIQUE] BMAD Process Kill
**Fichier:** `services/api/app/routers/bmad.py:200`
**Contexte:** Route `/bmad/kill`
**TODO actuel:**
```python
# TODO: Actually kill the subprocess
```
**Impact:** Impossible d'arrêter un agent BMAD bloqué
**Effort estimé:** 30min
**Solution:** Utiliser subprocess.terminate() avec tracking PID

---

### TODO #8 - [CRITIQUE] Progress Tracking
**Fichier:** `services/api/app/routers/progress.py:20,28`
**Contexte:** Routes `/progress/*`
**TODO actuel:**
```python
# TODO: Implement with real progress tracking
# TODO: Implement real progress tracking
```
**Impact:** UI ne peut pas afficher progression des tâches
**Effort estimé:** 2h
**Solution:** Redis pub/sub ou SSE avec tracking table

---

### TODO #9 - [CRITIQUE] Authentication Frontend
**Fichier:** `frontend/ia-factory-ui/app/login/page.tsx:29`
**Contexte:** Page login
**TODO actuel:**
```typescript
// TODO: Implement actual authentication with backend
```
**Impact:** Login non fonctionnel
**Effort estimé:** 2h
**Solution:** Connecter à `/api/auth/login` existant

---

### TODO #10 - [CRITIQUE] Video Studio - Initialisation
**Fichier:** `apps/video-studio/backend/main.py:31,40`
**Contexte:** Lifecycle FastAPI
**TODO actuel:**
```python
# TODO: Initialiser les connexions
# TODO: Fermer les connexions
```
**Impact:** Leaks de connexions possibles
**Effort estimé:** 30min
**Solution:** Implémenter lifespan avec async context managers

---

### TODO #11 - [CRITIQUE] Billing Service - Credit Renewal
**Fichier:** `services/api/app/services/billing_service.py:560`
**Contexte:** Renouvellement abonnements
**TODO actuel:**
```python
# TODO: Renouveler les crédits
```
**Impact:** Abonnés ne reçoivent pas crédits mensuels
**Effort estimé:** 2h
**Solution:** Scheduler Celery + logique credit reset

---

### TODO #12 - [CRITIQUE] Licence USB Check
**Fichier:** `services/api/app/security/licence_check.py:38-86`
**Contexte:** Vérification clé USB physique
**TODO actuel:**
```python
self.usb_vendor_id = "0x1234"  # TODO: Remplacer par vrai vendor ID
self.usb_product_id = "0x5678"  # TODO: Remplacer par vrai product ID
# TODO: Remplacer par vraie vérification USB
# TODO: Lire vraies données
```
**Impact:** Licence hardware non fonctionnelle
**Effort estimé:** 4h
**Solution:** Commander clé USB + implémenter pyusb

---

## TODOs IMPORTANTS (Fonctionnalités incomplètes)

### TODO #13 - [IMPORTANT] Client Onboarding - DocuSign
**Fichier:** `workflows/delivery/client_onboarding.py:95`
**Contexte:** Validation contrat
**TODO actuel:**
```python
# TODO: Intégrer DocuSign/HelloSign
```
**Effort estimé:** 4h
**Solution:** API DocuSign ou HelloSign

---

### TODO #14 - [IMPORTANT] Client Onboarding - Proxmox
**Fichier:** `workflows/delivery/client_onboarding.py:115`
**Contexte:** Provisioning infrastructure
**TODO actuel:**
```python
# TODO: Appeler API Proxmox pour créer container
```
**Effort estimé:** 4h
**Solution:** proxmoxer Python library

---

### TODO #15 - [IMPORTANT] Document Processing
**Fichier:** `workflows/delivery/client_onboarding.py:138`
**Contexte:** Import données client
**TODO actuel:**
```python
# TODO: Process uploaded documents
```
**Effort estimé:** 2h
**Solution:** Réutiliser ingest_router existant

---

### TODO #16 - [IMPORTANT] User Creation
**Fichier:** `workflows/delivery/client_onboarding.py:155`
**Contexte:** Setup utilisateurs
**TODO actuel:**
```python
# TODO: Implement user creation
```
**Effort estimé:** 1h
**Solution:** Appeler user_repository.create_user()

---

### TODO #17-18 - [IMPORTANT] Training Scheduling
**Fichier:** `workflows/delivery/client_onboarding.py:185-186`
**Contexte:** Planification formation
**TODO actuel:**
```python
# TODO: Envoyer email avec lien calendrier
# TODO: Créer événement Google Calendar
```
**Effort estimé:** 2h
**Solution:** Google Calendar API + email template

---

### TODO #19 - [IMPORTANT] Lead Generation - Data Enrichment
**Fichier:** `ia-factory/automation/workflows/lead_generation.py:113`
**Contexte:** Enrichissement leads
**TODO actuel:**
```python
# TODO: Intégrer Clearbit, LinkedIn, etc.
```
**Effort estimé:** 4h
**Solution:** Clearbit API ou Hunter.io

---

### TODO #20-22 - [IMPORTANT] Lead Notifications
**Fichier:** `ia-factory/automation/workflows/lead_generation.py:339-344`
**Contexte:** Notifications nouveaux leads
**TODO actuel:**
```python
# TODO: Envoyer notification WhatsApp/Telegram à Boualem
# TODO: Envoyer email via SMTP
# TODO: Créer tâche CRM
```
**Effort estimé:** 3h
**Solution:** Twilio/Telegram Bot + SMTP + CRM API

---

### TODO #23 - [IMPORTANT] Brand Invitation Email
**Fichier:** `ia-factory/backend/app/api/brand.py:311`
**Contexte:** Invitation membre équipe
**TODO actuel:**
```python
# TODO: Send invitation email
```
**Effort estimé:** 30min
**Solution:** notification_service.send_email()

---

### TODO #24 - [IMPORTANT] Sonelgaz Parser LLM
**Fichier:** `services/browser-automation/agents/sonelgaz.py:119`
**Contexte:** Parsing factures Sonelgaz
**TODO actuel:**
```python
# TODO: Implémenter le parsing intelligent avec le LLM
```
**Effort estimé:** 2h
**Solution:** Appeler Claude/GPT pour extraction structurée

---

### TODO #25 - [IMPORTANT] Daily Briefing - RSS
**Fichier:** `services/api/app/life_assistant/daily_briefing.py:100`
**Contexte:** News Geneva
**TODO actuel:**
```python
# TODO: Implement RSS parser for Geneva news
```
**Effort estimé:** 1h
**Solution:** feedparser library + sources CH

---

### TODO #26 - [IMPORTANT] Daily Briefing - Reminders
**Fichier:** `services/api/app/life_assistant/daily_briefing.py:206`
**Contexte:** Rappels utilisateur
**TODO actuel:**
```python
# TODO: Get from user_reminders table
```
**Effort estimé:** 30min
**Solution:** Query table user_reminders

---

### TODO #27 - [IMPORTANT] Daily Briefing - Tokens Tracking
**Fichier:** `services/api/app/life_assistant/daily_briefing.py:236`
**Contexte:** Statistiques tokens
**TODO actuel:**
```python
# TODO: Get from tokens_saved_tracking
```
**Effort estimé:** 30min
**Solution:** Query table tokens_saved_tracking

---

### TODO #28 - [IMPORTANT] Video Director - Real Generation
**Fichier:** `apps/video-studio/backend/agents/director.py:99`
**Contexte:** Génération vidéo par scène
**TODO actuel:**
```python
# TODO: Remplacer par une vraie génération vidéo par scène
```
**Effort estimé:** 4h
**Solution:** Appeler Replicate/FAL par scène

---

### TODO #29 - [IMPORTANT] Lipsync Service
**Fichier:** `apps/video-studio/backend/services/lipsync_service.py:130`
**Contexte:** Synchronisation lèvres
**TODO actuel:**
```python
# TODO: Implémenter appel à Wav2Lip
```
**Effort estimé:** 4h
**Solution:** Wav2Lip API ou Replicate model

---

### TODO #30 - [IMPORTANT] Character Video Generation
**Fichier:** `apps/video-studio/backend/services/character_service.py:256`
**Contexte:** Vidéo avec personnage
**TODO actuel:**
```python
# TODO: Implémenter génération vidéo avec character reference
```
**Effort estimé:** 4h
**Solution:** HeyGen ou D-ID API

---

### TODO #31 - [IMPORTANT] Gmail API
**Fichier:** `services/api/app/life_assistant/workspace_connector.py:82`
**Contexte:** Intégration Gmail
**TODO actuel:**
```python
# TODO: Implémenter Gmail API v1
```
**Effort estimé:** 3h
**Solution:** Google Gmail API + OAuth

---

### TODO #32 - [IMPORTANT] LLM Proxy
**Fichier:** `services/api/app/life_assistant/workspace_connector.py:206`
**Contexte:** Appel LLM
**TODO actuel:**
```python
# TODO: Call LLM Proxy
```
**Effort estimé:** 30min
**Solution:** Appeler multi_llm_service

---

### TODO #33 - [IMPORTANT] Google Calendar API
**Fichier:** `services/api/app/life_assistant/workspace_connector.py:371`
**Contexte:** Calendrier
**TODO actuel:**
```python
# TODO: Implement Google Calendar API
```
**Effort estimé:** 3h
**Solution:** Google Calendar API + OAuth

---

### TODO #34 - [IMPORTANT] Team Admin Key
**Fichier:** `services/api/app/team_seats/team_seats_router.py:192`
**Contexte:** Vérification admin
**TODO actuel:**
```python
# TODO: Vérification admin key
```
**Effort estimé:** 30min
**Solution:** Check role in JWT

---

### TODO #35 - [IMPORTANT] STT Service
**Fichier:** `services/api/app/voice/stt_service.py:471`
**Contexte:** Speech-to-text
**TODO actuel:**
```python
# TODO: Implémenter avec faster-whisper ou whisper
```
**Effort estimé:** 2h
**Solution:** faster-whisper local ou Groq Whisper API

---

### TODO #36 - [IMPORTANT] Hybrid Search Sparse Vectors
**Fichier:** `services/api/app/bigrag/hybrid_search.py:285`
**Contexte:** Search hybride
**TODO actuel:**
```python
# TODO: Utiliser Qdrant sparse vectors quand disponible
```
**Effort estimé:** 2h
**Solution:** Qdrant sparse vectors (bêta)

---

### TODO #37-38 - [IMPORTANT] PME PDF Generation
**Fichier:** `services/api/app/routers/pme_v2.py:626,649`
**Contexte:** Export PDF rapports
**TODO actuel:**
```python
# TODO: Intégrer reportlab ou weasyprint pour la génération PDF
# TODO: Implémenter avec reportlab
```
**Effort estimé:** 3h
**Solution:** reportlab ou weasyprint

---

### TODO #39 - [IMPORTANT] DZirvideo MoviePy
**Fichier:** `services/api/app/services/dzirvideo_service.py:357`
**Contexte:** Composition vidéo
**TODO actuel:**
```python
# TODO: Use MoviePy to compose video
```
**Effort estimé:** 4h
**Solution:** MoviePy video concatenation

---

### TODO #40 - [IMPORTANT] Rate Limiter Advanced
**Fichier:** `services/api/app/middleware/rate_limiter.py:301`
**Contexte:** Détection abus
**TODO actuel:**
```python
# TODO: Implémenter détection avancée avec embeddings
```
**Effort estimé:** 4h
**Solution:** Similarity check avec embeddings

---

## TODOs MINEURS (API Portal, Tests, Archon UI)

### TODO #41-47 - [MINEUR] API Portal Mocks
**Fichiers:** `apps/api-portal/frontend/src/components/*.tsx`
- ApiDocsPlayground.tsx:385 - Execute playground
- ApiKeysManager.tsx:246,284,312 - API keys CRUD
- ApiLogsTable.tsx:183 - Logs fetch
- ApiOverview.tsx:188 - Stats
- ApiUsageOverview.tsx:258 - Usage metrics

**Effort total:** 4h
**Solution:** Connecter au backend API existant

---

### TODO #48-49 - [MINEUR] Archon MCP
**Fichier:** `frontend/archon-ui/python/src/server/api_routes/mcp_api.py:150,180`
**TODO actuel:**
```python
# TODO: Implement real client detection in the future
# TODO: Implement real session tracking
```
**Effort total:** 2h

---

### TODO #50 - [MINEUR] Archon Optimistic Updates
**Fichier:** `frontend/archon-ui/archon-ui-main/src/features/knowledge/hooks/useKnowledgeQueries.ts:122`
**TODO actuel:**
```typescript
// TODO: Fix invisible optimistic updates
```
**Effort:** 1h

---

### TODO #51 - [MINEUR] Archon Ollama Instances
**Fichier:** `frontend/archon-ui/python/src/server/services/llm_provider_service.py:572`
**TODO actuel:**
```python
# TODO: Implement get_ollama_instances() method
```
**Effort:** 1h

---

### TODO #52 - [MINEUR] Qdrant Integration Archon
**Fichier:** `services/api/app/services/archon_integration_service.py:211`
**TODO actuel:**
```python
# TODO: Implémenter l'appel à Qdrant via le service backend
```
**Effort:** 1h

---

### TODO #53-57 - [MINEUR] Legacy Backup (peuvent être ignorés)
**Fichiers:** `services/api/app_legacy_backup/routers/*.py`
- bmad.py:200,213,234 - Legacy BMAD
- knowledge.py:23,37,44,55 - Legacy knowledge
- progress.py:20,28 - Legacy progress

**Effort:** 0h (code legacy, copié dans app/)

---

### TODO #58 - [MINEUR] Billing Overage
**Fichier:** `services/backend/billing/api.py:232`
**TODO actuel:**
```python
"overage_cost_chf": 0  # TODO: Calculate overage
```
**Effort:** 30min

---

### TODO #59 - [MINEUR] DOCX Generator Claude
**Fichier:** `ia-factory/automation/claude_skills/docx_generator.py:405`
**TODO actuel:**
```python
# TODO: Intégrer Claude API pour générer le contenu
```
**Effort:** 1h

---

### TODO #60 - [MINEUR] RAG Citations
**Fichier:** `agents/templates/rag-apps/rag-as-a-service/rag_as_a_service_service.py:139`
**TODO actuel:**
```python
citations = [] # TODO: Extract citations from chunks
```
**Effort:** 30min

---

### TODO #61 - [MINEUR] Video Routes Uncomment
**Fichier:** `apps/video-studio/backend/main.py:150`
**TODO actuel:**
```python
# TODO: Décommenter une fois les routes créées
```
**Effort:** 5min

---

### TODO #62 - [MINEUR] FFmpeg Comparison
**Fichier:** `apps/dzirvideo/src/pipeline_v2.py:527`
**TODO actuel:**
```python
# TODO: Create side-by-side comparison with FFmpeg
```
**Effort:** 1h

---

### TODO #63 - [MINEUR] Harmonize Colors
**Fichier:** `scripts/harmonize-colors.py:178`
**TODO actuel:**
```python
# TODO: implémenter correction
```
**Effort:** 30min

---

### TODO #64 - [MINEUR] Voice Transcription LLM Cleanup
**Fichier:** `services/api/app/voice_agent/transcription_service.py:199`
**TODO actuel:**
```python
# TODO: Intégrer avec LLM pour nettoyage avancé
```
**Effort:** 1h

---

### TODO #65-66 - [MINEUR] Voice Router Context
**Fichier:** `services/api/app/voice_agent/router.py:120,165`
**TODO actuel:**
```python
# TODO: Get user_country from tenant metadata
# TODO: Get user_id from authentication context
```
**Effort:** 30min

---

### TODO #67 - [MINEUR] Multi LLM Service Type
**Fichier:** `services/api/app/multi_llm/multi_llm_service.py:206`
**TODO actuel:**
```python
service_type=ServiceType.RAG_QUERY,  # TODO: Ajouter ServiceType.LLM_CHAT
```
**Effort:** 15min

---

### TODO #68 - [MINEUR] Bolt Zip Integration Tests
**Fichier:** `services/api/app/services/bolt_zip_service.py:447`
**TODO actuel:**
```python
# TODO: Add integration tests
```
**Effort:** 2h

---

### TODO #69 - [MINEUR] Chat Safe Ban Check
**Fichier:** `services/api/app/routers/chat_safe.py:125`
**TODO actuel:**
```python
# TODO: Implémenter check ban si besoin
```
**Effort:** 30min

---

### TODO #70-73 - [MINEUR] Mobile Briefing Parse
**Fichier:** `services/api/app/life_assistant/mobile_router.py:360,382`
**TODO actuel:**
```python
# TODO: Get user profile from DB
# TODO: Parse briefing_text into structured JSON
```
**Effort:** 1h

---

### TODO #74 - [MINEUR] Achievement Goals Track
**Fichier:** `apps/ia-agents/app/agents/motivation/components/AchievementBadges.tsx:82`
**TODO actuel:**
```typescript
goalsCompleted: 0, // TODO: Track goals
```
**Effort:** 30min

---

### TODO #75 - [MINEUR] Lead Capture Backend
**Fichier:** `apps/ia-agents/app/agents/motivation/components/LeadCaptureModal.tsx:19`
**TODO actuel:**
```typescript
// TODO: Send to backend/email service
```
**Effort:** 30min

---

---

## PLAN D'ACTION RECOMMANDE

### Sprint 1 - Sécurité & Paiements (4h)
1. TODO #4 - Webhook signatures Chargily/Stripe
2. TODO #6 - Payment email confirmation
3. TODO #11 - Credit renewal

### Sprint 2 - Mobile & Auth (4h)
1. TODO #2 - Mobile pairing DB
2. TODO #3 - Token validation
3. TODO #9 - Frontend auth

### Sprint 3 - Knowledge Base (3h)
1. TODO #1 - Knowledge API complète
2. TODO #8 - Progress tracking

### Sprint 4 - Voice & RAG (4h)
1. TODO #5 - Voice agent BIG RAG
2. TODO #35 - STT service
3. TODO #36 - Hybrid search sparse

### Sprint 5 - Video Studio (8h)
1. TODO #10 - Connexions lifecycle
2. TODO #28 - Video generation réelle
3. TODO #29 - Lipsync
4. TODO #30 - Character video

### Backlog - Intégrations (16h+)
- DocuSign, Proxmox, Gmail, Calendar
- Clearbit, CRM
- PDF generation

---

## SCRIPTS DE RECHERCHE

```bash
# Trouver tous les TODOs
grep -rn "# TODO\|// TODO" --include="*.py" --include="*.ts" --include="*.tsx" .

# TODOs critiques (security, payment, auth)
grep -rn "TODO.*security\|TODO.*payment\|TODO.*auth\|TODO.*token" --include="*.py" .

# Compter par fichier
grep -rn "# TODO" --include="*.py" . | cut -d: -f1 | sort | uniq -c | sort -rn
```
