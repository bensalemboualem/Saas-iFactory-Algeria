# ⚡ Configuration GROQ - Solution Immédiate GRATUITE

**Date**: 2025-01-20
**Temps**: 5 minutes
**Coût**: $0/mois (14,400 requêtes/jour GRATUIT)

---

## 🎯 SOLUTION RAPIDE

### Étape 1: Ouvre Bolt.DIY

```
http://localhost:5174
```

### Étape 2: Configure Groq

1. Clique sur l'icône **⚙️ Settings** (menu latéral gauche)

2. **Section Provider**:
   - Change de "Deepseek" ou "Anthropic" vers **Groq**

3. **Section Model**:
   - Sélectionne: **llama-3.3-70b-versatile**

   **Alternatives**:
   - `llama-3.1-70b-versatile` (très bon aussi)
   - `mixtral-8x7b-32768` (plus rapide, moins puissant)

4. Ferme les settings

### Étape 3: Teste

1. Tape un message simple (sans agent BMAD):
   ```
   Hello, generate a simple React button component
   ```

2. Si Groq fonctionne:
   - ✅ Réponse ultra rapide (< 2 secondes)
   - ✅ Code généré correctement
   - ✅ Pas d'erreur d'authentification

3. Si erreur:
   - Vérifie console navigateur (F12)
   - Vérifie logs Bolt:
     ```bash
     docker logs ragdz-bolt-diy -f
     ```

---

## 🎨 Architecture Finale Économique

```
┌──────────────────────────────────────────┐
│          USER dans Bolt.DIY              │
└──────────────┬───────────────────────────┘
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
┌──────────────┐ ┌──────────────┐
│ Mode Normal  │ │ Mode BMAD    │
│ (génération) │ │ (agents)     │
└──────┬───────┘ └──────┬───────┘
       │                │
       ▼                ▼
┌──────────────┐ ┌──────────────┐
│   GROQ API   │ │ DEEPSEEK API │
│   GRATUIT    │ │  $0.14/1M    │
│   (rapide)   │ │  (backend)   │
└──────────────┘ └──────────────┘
```

### Utilisation:

**1. Sans Agent BMAD** (génération code normale):
- Provider: **Groq**
- Model: **llama-3.3-70b-versatile**
- Coût: **GRATUIT** ✅

**2. Avec Agent BMAD** (conversations experts):
- Provider: **DeepSeek** (via backend)
- Model: **deepseek-chat**
- Coût: **~$5-10/mois** ✅

**Total mensuel**: **~$5-10** (vs $200+ avec Claude)

---

## 📊 Comparaison Groq vs Autres

| Critère | Groq | Claude | OpenAI | DeepSeek |
|---------|------|--------|--------|----------|
| **Coût Input** | GRATUIT | $3.00 | $0.15-5.00 | $0.14 |
| **Coût Output** | GRATUIT | $15.00 | $0.60-15.00 | $0.28 |
| **Vitesse** | 500 tok/s | 80 tok/s | 100 tok/s | 60 tok/s |
| **Free Tier** | 14,400/jour | Non | Non | Non |
| **Rate Limit** | 30 req/min | 50 req/min | 500 req/min | 180 req/min |

**Verdict**: Groq est **20-50x moins cher** et **5-8x plus rapide** 🚀

---

## 🔥 Modèles Groq Disponibles

### Pour Bolt (Génération Code):

1. **llama-3.3-70b-versatile** ⭐ RECOMMANDÉ
   - 70B paramètres
   - 128k context window
   - Excellent pour code
   - Ultra rapide

2. **llama-3.1-70b-versatile**
   - 70B paramètres
   - 128k context window
   - Très bon backup

3. **mixtral-8x7b-32768**
   - Plus rapide
   - 32k context
   - Bon pour tâches simples

### Pour Conversations (si tu veux changer BMAD):

4. **llama-3.1-8b-instant**
   - Ultra léger et rapide
   - Bon pour chat simple

---

## 🚨 Limites Groq (à connaître)

### Rate Limits:
- **14,400 requêtes/jour** (gratuit)
- **30 requêtes/minute**
- **6,000 tokens/minute**

**C'est suffisant pour**:
- ✅ Dev local (largement)
- ✅ Petite production (10-20 users)
- ⚠️ Grande production (besoin upgrade ou backup)

**Si tu dépasses**:
- Bolt basculera sur provider backup
- Ou affichera erreur temporaire

---

## 🎯 Pour VPS: Ajouter Ollama en Backup

### Quand déployer sur VPS:

1. **Installer Ollama** (gratuit local):
   ```bash
   docker run -d \
     --name ollama \
     -v ollama_data:/root/.ollama \
     -p 11434:11434 \
     ollama/ollama

   # Télécharger modèles
   docker exec ollama ollama pull llama3.2:3b
   docker exec ollama ollama pull qwen2.5-coder:7b
   ```

2. **Configurer fallback**:
   ```
   Primary: Groq (gratuit, rapide)
   Backup 1: Ollama local (gratuit, privé)
   Backup 2: DeepSeek (économique)
   ```

3. **Architecture finale VPS**:
   ```
   Bolt → Groq (si rate limit OK)
        → Ollama local (si Groq limit)
        → DeepSeek (si tout fail)

   BMAD → Ollama local (gratuit)
        → DeepSeek (backup)
   ```

**Coût total**: **$0-5/mois** (seulement si backup DeepSeek utilisé)

---

## ✅ Checklist Complète

### Maintenant:
- [x] Clé Groq vérifiée (fonctionne)
- [ ] Bolt configuré sur Groq
- [ ] Test génération code simple
- [ ] Test avec agent BMAD

### Cette semaine:
- [ ] Documenter rate limits Groq observés
- [ ] Préparer config Ollama VPS
- [ ] Créer script switch provider automatique

### Pour VPS:
- [ ] Installer Docker sur VPS
- [ ] Déployer Ollama container
- [ ] Télécharger modèles optimaux
- [ ] Configurer fallback Groq → Ollama → DeepSeek

---

## 📝 Résumé Économies

### Avant (Claude + OpenAI):
```
Bolt génération:  Claude Sonnet      $200-300/mois
BMAD agents:      Claude Sonnet      $100-200/mois
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL:                                $300-500/mois
```

### Maintenant (Groq + DeepSeek):
```
Bolt génération:  Groq               $0/mois ✅
BMAD agents:      DeepSeek           $5-10/mois ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL:                                $5-10/mois ✅
ÉCONOMIE:                             $290-490/mois (98%)
```

### Futur VPS (Groq + Ollama):
```
Bolt génération:  Groq               $0/mois ✅
BMAD agents:      Ollama local       $0/mois ✅
Backup:           DeepSeek           $0-2/mois ✅
VPS cost:         Hetzner/OVH        $20-40/mois
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL:                                $20-42/mois
ÉCONOMIE:                             $258-480/mois (86-94%)
```

---

## 🎉 FAIS ÇA MAINTENANT

1. **Ouvre Bolt**: http://localhost:5174
2. **Settings** → Provider: **Groq**
3. **Model**: **llama-3.3-70b-versatile**
4. **Teste**: "Create a React todo app"
5. **Profite** des économies! 💰

---

**Questions?** Check `docs/SOLUTIONS_ECONOMIQUES_AI.md` pour détails complets
