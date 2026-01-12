# LLM Council - Guide de Démarrage Rapide

## 🎯 Qu'est-ce que LLM Council ?

LLM Council est un système innovant qui consulte **plusieurs modèles d'IA simultanément** pour obtenir des réponses plus robustes et fiables. Au lieu de se fier à un seul modèle, le système:

1. **Collecte les opinions** de 3 modèles d'IA différents
2. **Optionnellement, fait une revue croisée** où chaque modèle évalue les autres
3. **Synthétise une réponse finale** optimale par un "chairman"

## 🚀 Installation Express (5 minutes)

### 1. Mettre à jour .env.local

```bash
# Copier l'exemple si vous n'avez pas encore de .env.local
cp .env.example .env.local

# Ajouter vos clés API
nano .env.local
```

Configurez au minimum:
```bash
# Pour Claude (chairman)
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Pour Gemini
GOOGLE_GENERATIVE_AI_API_KEY=AIzaSy-xxxxx

# Ollama sera disponible automatiquement via Docker
OLLAMA_BASE_URL=http://iafactory-ollama:11434
```

### 2. Démarrer Ollama

Ollama est déjà configuré dans docker-compose.yml. Pour le démarrer:

```bash
# Option 1: Démarrer uniquement Ollama
docker-compose up -d iafactory-ollama

# Option 2: Démarrer toute la stack (recommandé)
docker-compose up -d
```

Télécharger le modèle Llama 3:
```bash
docker exec -it iaf-dz-ollama ollama pull llama3:8b
```

### 3. Redémarrer le backend

```bash
docker-compose restart iafactory-backend
```

### 4. Tester l'installation

```bash
# Avec Python
python test-council.py

# Ou avec curl
curl http://localhost:8180/api/council/health
```

## 📖 Utilisation

### Via l'Interface Web

1. Ouvrir http://localhost:8182 (IAFactory Hub)
2. Cliquer sur "LLM Council" dans la navigation
3. Poser votre question
4. Attendre 15-30 secondes pour la réponse

### Via l'API

#### Test simple
```bash
curl -X POST http://localhost:8180/api/council/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Quelles sont les meilleures pratiques pour sécuriser une API REST ?",
    "enable_review": false
  }'
```

#### Avec revue croisée (plus lent)
```bash
curl -X POST http://localhost:8180/api/council/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Comment optimiser les performances PostgreSQL ?",
    "enable_review": true
  }'
```

#### Lister les providers disponibles
```bash
curl http://localhost:8180/api/council/providers
```

## 🔧 Configuration Avancée

### Changer le chairman

Dans `.env.local`:
```bash
COUNCIL_CHAIRMAN=gemini  # Par défaut: claude
```

### Activer la revue par défaut

```bash
COUNCIL_ENABLE_REVIEW=true  # Par défaut: false
```

### URL Ollama custom

```bash
OLLAMA_BASE_URL=http://mon-ollama:11434
```

## 📊 Architecture du Pipeline

```
┌─────────────────────────────────────────────────┐
│              STAGE 1: OPINIONS                  │
│  Claude, Gemini, Ollama répondent en parallèle  │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│         STAGE 2: REVIEW (optionnel)             │
│  Chaque modèle évalue les autres                │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│         STAGE 3: SYNTHESIS                      │
│  Chairman synthétise la réponse finale          │
└─────────────────────────────────────────────────┘
```

## 🎯 Cas d'usage recommandés

### ✅ Quand utiliser Council

- **Décisions importantes** : analyses stratégiques, recommandations
- **Validation technique** : architecture, sécurité, performance
- **Recherche approfondie** : synthèse de documentation
- **Questions complexes** : nécessitant plusieurs perspectives

### ❌ Quand NE PAS utiliser Council

- Questions simples et factuelles
- Besoins de rapidité (< 5s)
- Tâches créatives (génération de contenu)
- Cas où un seul modèle suffit

## 💰 Coûts estimés

### Mode Standard (sans review)
- **Latence**: 15-30 secondes
- **Coût par requête**: ~$0.015 (1.5¢)
- **Usage**: Questions de complexité moyenne

### Mode Premium (avec review)
- **Latence**: 30-60 secondes
- **Coût par requête**: ~$0.030 (3¢)
- **Usage**: Décisions critiques

**Note**: Ollama est gratuit (modèle local)

## 🐛 Dépannage

### Problème: "No available providers"

**Solution**: Vérifier vos clés API dans `.env.local`
```bash
# Vérifier
curl http://localhost:8180/api/council/providers

# Tester la connectivité
curl -X POST http://localhost:8180/api/council/test
```

### Problème: Ollama non disponible

**Solution**: Vérifier le container Ollama
```bash
# Status du container
docker ps | grep ollama

# Logs
docker logs iaf-dz-ollama

# Redémarrer
docker-compose restart iafactory-ollama

# Télécharger le modèle si manquant
docker exec -it iaf-dz-ollama ollama pull llama3:8b
```

### Problème: Timeout

**Solution**: Augmenter les timeouts dans `backend/rag-compat/app/modules/council/config.py`:
```python
STAGE1_TIMEOUT: int = 60  # Au lieu de 30
TOTAL_TIMEOUT: int = 180  # Au lieu de 90
```

### Problème: Erreur Claude ou Gemini

**Solution**: Vérifier les clés API et les quotas
```bash
# Test manuel Claude
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4-20250514","max_tokens":100,"messages":[{"role":"user","content":"test"}]}'

# Test manuel Gemini
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=$GOOGLE_GENERATIVE_AI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"test"}]}]}'
```

## 📚 Endpoints API

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/council/query` | POST | Interroger le Council |
| `/api/council/providers` | GET | Liste des providers |
| `/api/council/test` | POST | Tester la connectivité |
| `/api/council/config` | GET | Configuration actuelle |
| `/api/council/health` | GET | Santé du service |

## 🔗 Documentation complète

- **API Docs**: http://localhost:8180/docs#/Council
- **Architecture**: [ARCHITECTURE.md](../ARCHITECTURE.md)
- **Tests**: `python test-council.py`

## 📞 Support

Pour la démo du 6 décembre avec Algérie Télécom:
- Questions préparées dans `docs/DEMO_COUNCIL_DZ.md`
- Pricing détaillé dans `docs/COUNCIL_PRICING.md`

## 🎉 Checklist de validation

- [ ] Backend démarré avec Council activé
- [ ] Les 3 providers affichent "available: true"
- [ ] Test simple réussit (< 30s)
- [ ] Interface web accessible sur /council
- [ ] Documentation API visible sur /docs
