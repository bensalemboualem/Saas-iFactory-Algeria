# 🚀 Dzir IA Video PRO - Upgrade Guide to v2.1

## Ce qui a été ajouté

### 1. Assistant IA de Script (`src/ai_assistant/script_optimizer.py`)

Un système intelligent qui transforme une idée basique en script viral optimisé :

**Fonctionnalités** :
- ✅ Hook accrocheur (3 premières secondes)
- ✅ Structure engageante (contenu principal)
- ✅ Call-to-action efficace
- ✅ Titre optimisé SEO (max 60 caractères)
- ✅ Description avec mots-clés
- ✅ Tags pertinents (10-15)
- ✅ **Score viral** (0-100) basé sur patterns YouTube
- ✅ Suggestions d'amélioration en temps réel

**API utilisée** :
- Claude Sonnet 4.5 (si API key fournie)
- Fallback intelligent (règles prédéfinies) si pas d'API

### 2. Interface Web PRO (`public/index-pro.html`)

Une interface moderne en 2 colonnes :

**Colonne Gauche - Chat IA** :
- Chat conversationnel avec l'assistant
- Boutons quick-action (Tech, Business, Éducation, Motivation)
- Historique des messages
- Indicateur de frappe

**Colonne Droite - Création Vidéo** :
- Preview du script généré
- Compteur de caractères
- Titre & description auto-remplis
- Options avancées (collapsible) :
  - Choix de voix (masculin/féminin)
  - Style de sous-titres (MrBeast, Ali Abdaal, Classic)
  - Musique de fond
- Barre de progression détaillée (5 étapes)
- Player vidéo intégré
- Download + Nouvelle vidéo

### 3. API PRO (`src/api_pro.py`)

Nouveaux endpoints :

```
POST /ai/optimize-script
- Input: { raw_idea, niche, tone, target_duration }
- Output: Script optimisé + metadata

POST /ai/analyze-script
- Input: { script }
- Output: Analyse + suggestions

GET /
- Sert l'interface PRO (au lieu de JSON)

GET /api
- Info JSON (rétrocompatibilité)
```

## Déploiement

### Option 1 : Test LOCAL (recommandé d'abord)

```bash
# 1. Installer les nouvelles dépendances
cd d:/IAFactory/rag-dz/apps/dzirvideo
pip install requests==2.31.0

# 2. (Optionnel) Ajouter API key Claude
# Créer/éditer .env
echo "CLAUDE_API_KEY=sk-ant-..." >> .env

# 3. Lancer avec l'API PRO
python -m uvicorn src.api_pro:app --host 0.0.0.0 --port 8200 --reload

# 4. Ouvrir http://localhost:8200
```

### Option 2 : Déploiement VPS PRODUCTION

```bash
# 1. Upload des fichiers
scp -r src/ai_assistant root@46.224.3.125:/opt/rag-dz/apps/dzirvideo/src/
scp public/index-pro.html root@46.224.3.125:/opt/rag-dz/apps/dzirvideo/public/
scp src/api_pro.py root@46.224.3.125:/opt/rag-dz/apps/dzirvideo/src/
scp requirements.txt root@46.224.3.125:/opt/rag-dz/apps/dzirvideo/

# 2. Rebuild & redeploy sur VPS
ssh root@46.224.3.125 "cd /opt/rag-dz/apps/dzirvideo && \
    docker-compose down && \
    docker-compose build --no-cache && \
    docker-compose up -d"

# 3. Vérifier
curl https://video.iafactoryalgeria.com/api
```

## Configuration API Claude (Optionnel)

Si tu veux activer l'IA avancée :

1. Obtenir une API key : https://console.anthropic.com/
2. Ajouter dans `.env` :
   ```
   CLAUDE_API_KEY=sk-ant-api03-...
   ```
3. Rebuild le container

**Note** : Sans API key, le système utilise un mode "fallback" avec des règles prédéfinies qui fonctionnent déjà bien.

## Prochaines Améliorations (si tu veux continuer)

### Phase 2 - Montage Avancé (2-3h)
- [ ] Sous-titres animés style MrBeast (zoom sur mots-clés)
- [ ] Transitions fluides entre scènes
- [ ] Background vidéo dynamique (au lieu d'image statique)
- [ ] Effets visuels (particules, glitch)

### Phase 3 - Bibliothèque Média (2h)
- [ ] Intégration Pexels API (vidéos B-roll gratuites)
- [ ] Pixabay Music API (musiques libres de droits)
- [ ] Templates visuels prédéfinis (Tech, Business, etc.)
- [ ] Auto-sélection d'images basée sur le script

### Phase 4 - Multi-voix & Audio Pro (1h)
- [ ] 5-10 voix différentes (ElevenLabs)
- [ ] Respirations naturelles
- [ ] Égalisation audio automatique
- [ ] Ducking (musique baisse quand voix parle)

### Phase 5 - Analytics & A/B Testing (1h)
- [ ] Preview avant génération finale
- [ ] Score viral en temps réel
- [ ] A/B testing de thumbnails
- [ ] Statistiques de performance

## Différences vs Version Basique

| Feature | Version Basique | Version PRO (v2.1) |
|---------|----------------|---------------------|
| Interface | Formulaire simple | Chat IA + Formulaire avancé |
| Script | Manuel | Auto-généré par IA |
| Optimisation | Aucune | Hook + CTA + SEO |
| Score viral | Non | Oui (0-100) |
| Suggestions | Non | Oui (temps réel) |
| Options avancées | Non | Voix, sous-titres, musique |
| **Générateurs vidéo** | **Statique** | **40+ générateurs IA** |
| **Génération dynamique** | **Non** | **WAN 2.1, Kling, Runway, etc.** |
| API endpoints | 4 | 10+ |
| Design | Basique | Professionnel |

## Test Rapide

1. Ouvre l'interface PRO
2. Clique sur le bouton "💻 Tech"
3. L'assistant génère un script optimisé
4. Clique "Créer la Vidéo PRO"
5. Attends 30-60 secondes
6. Preview & download

## Support

Si erreur, vérifier :
- `docker logs dzirvideo` sur VPS
- Console browser (F12) pour erreurs frontend
- `/status` endpoint pour config

---

**Version** : 2.1.0 (Multi-AI Generators)
**Date** : 2025-12-13
**Créé par** : IAFactory Team

**Note** : Ce guide sera mis à jour avec les instructions complètes pour les 40+ générateurs IA (WAN 2.1, Kling AI, Runway, FLUX.1, etc.) une fois l'implémentation de la Phase 2-3 terminée.
