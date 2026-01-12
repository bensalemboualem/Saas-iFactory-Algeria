# Guide de Rotation Rapide des Clés API - 20 Minutes

**Objectif**: Sécuriser le projet en régénérant les 5 clés API critiques exposées.

---

## Étape 1: Exécuter le script automatique (2 min)

```bash
# Windows
cd d:\IAFactory\rag-dz
scripts\rotate_api_keys.bat

# Linux/Mac
cd /path/to/rag-dz
chmod +x scripts/rotate_api_keys.sh
./scripts/rotate_api_keys.sh
```

**Résultat**:
- ✅ Fichier `.env.ready` supprimé du tracking Git
- ✅ Backup créé dans `apps/video-studio/.env.ready.EXPOSED.backup.txt`
- ✅ Template `.env.local` créé dans `services/api/`
- ✅ `.gitignore` mis à jour

---

## Étape 2: Régénérer les 5 clés CRITIQUES (15 min)

### 🔑 OpenRouter (Provider principal PAID)

1. **Ouvrir**: https://openrouter.ai/keys
2. **Login**: Avec votre compte OpenRouter
3. **Révoquer ancienne clé**:
   - Chercher la clé qui commence par `sk-or-v1-`
   - Cliquer sur "Revoke"
4. **Créer nouvelle clé**:
   - Nom: "IA Factory Algeria - Production"
   - Cliquer "Create API Key"
   - **COPIER** la clé: `sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
5. **Coller** dans `services/api/.env.local`:
   ```bash
   OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

### 🔑 Groq (Provider FREE - Backup)

1. **Ouvrir**: https://console.groq.com/keys
2. **Login**: Avec votre compte Groq
3. **Révoquer ancienne clé**:
   - Cliquer sur les 3 points à côté de l'ancienne clé
   - "Delete API Key"
4. **Créer nouvelle clé**:
   - Cliquer "Create API Key"
   - Nom: "IA Factory Algeria Prod"
   - **COPIER**: `gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
5. **Coller** dans `.env.local`:
   ```bash
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

### 🔑 Anthropic (Tests directs Claude)

1. **Ouvrir**: https://console.anthropic.com/settings/keys
2. **Login**: Avec votre compte Anthropic
3. **Révoquer ancienne clé**:
   - Chercher clé commençant par `sk-ant-api03-KXm`
   - Cliquer "Delete"
4. **Créer nouvelle clé**:
   - Cliquer "Create Key"
   - Nom: "IA Factory Algeria"
   - **COPIER**: `sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
5. **Coller** dans `.env.local`:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

### 🔑 OpenAI (Tests directs GPT)

1. **Ouvrir**: https://platform.openai.com/api-keys
2. **Login**: Avec votre compte OpenAI
3. **Révoquer ancienne clé**:
   - Chercher clé commençant par `sk-proj-ysv`
   - Cliquer "Revoke"
4. **Créer nouvelle clé**:
   - Cliquer "+ Create new secret key"
   - Nom: "IA Factory Algeria"
   - Permissions: "All" (ou "Read" seulement si préféré)
   - **COPIER**: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
5. **Coller** dans `.env.local`:
   ```bash
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

### 🔑 Google Gemini (Fallback gratuit)

1. **Ouvrir**: https://makersuite.google.com/app/apikey
2. **Login**: Avec votre compte Google
3. **Révoquer ancienne clé** (si existante):
   - Cliquer sur les 3 points
   - "Delete API key"
4. **Créer nouvelle clé**:
   - Cliquer "Get API key"
   - Choisir projet ou créer nouveau
   - **COPIER**: `AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
5. **Coller** dans `.env.local`:
   ```bash
   GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## Étape 3: Générer JWT_SECRET_KEY (1 min)

### Option A: PowerShell (Windows)
```powershell
# Ouvrir PowerShell et exécuter:
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | % {[char]$_})
```

### Option B: Python
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Option C: En ligne
https://generate-secret.vercel.app/64

**Copier le résultat** dans `.env.local`:
```bash
JWT_SECRET_KEY=votre_secret_genere_ici
```

---

## Étape 4: Vérifier .env.local (1 min)

Ouvrir `services/api/.env.local` et vérifier:

```bash
# DOIT contenir (exemples):
OPENROUTER_API_KEY=sk-or-v1-abc123...    # ✅ Commence par sk-or-v1-
GROQ_API_KEY=gsk_def456...                # ✅ Commence par gsk_
ANTHROPIC_API_KEY=sk-ant-ghi789...        # ✅ Commence par sk-ant-
OPENAI_API_KEY=sk-proj-jkl012...          # ✅ Commence par sk-proj-
GOOGLE_API_KEY=AIzaSymno345...            # ✅ Commence par AIzaSy
JWT_SECRET_KEY=pqr678stu901vwx234...      # ✅ 64 caractères aléatoires

# NE DOIT PAS contenir:
VOTRE_NOUVELLE_CLE_ICI                    # ❌ Placeholder non remplacé
```

---

## Étape 5: Vérifier la rotation (1 min)

```bash
cd d:\IAFactory\rag-dz
python scripts\verify_keys_rotation.py
```

**Résultat attendu**:
```
✅ [CHECK 1/5] .env.local existe et contient des clés
✅ [CHECK 2/5] .gitignore protège les fichiers sensibles
✅ [CHECK 3/5] .env.ready est supprimé du tracking Git
✅ [CHECK 4/5] Aucune clé exposée détectée dans le codebase
✅ [CHECK 5/5] Historique Git récent semble propre

✅ ROTATION DES CLES TERMINEE AVEC SUCCES
```

---

## Étape 6: Commit des changements (1 min)

```bash
git add .gitignore
git commit -m "security: remove exposed API keys from tracking

- Suppression de .env.ready du tracking Git
- Ajout de .env.local et .env.ready au .gitignore
- Rotation des 5 clés API critiques effectuée
- Backup des clés exposées créé (non commité)"

# NE PAS PUSH AVANT D'AVOIR VERIFIE:
git diff HEAD~1
# Vérifier qu'aucune clé n'apparaît dans le diff
```

---

## ✅ Checklist Finale

Avant de passer à l'étape suivante (migration SQL):

- [ ] `.env.local` créé dans `services/api/`
- [ ] 5 clés API critiques régénérées et collées dans `.env.local`
- [ ] JWT_SECRET_KEY généré (64 caractères)
- [ ] `python scripts/verify_keys_rotation.py` → 5/5 checks passent
- [ ] `.env.ready` supprimé du tracking Git
- [ ] Commit créé (pas encore push)
- [ ] Aucune clé visible dans `git diff HEAD~1`

---

## En cas de problème

### Erreur: "VOTRE_NOUVELLE_CLE_ICI still in .env.local"
**Solution**: Ouvrez `.env.local` et remplacez tous les placeholders par les vraies clés

### Erreur: "Clés exposées trouvées dans le codebase"
**Solution**:
1. Vérifier si c'est le backup `.env.ready.EXPOSED.backup.txt` → OK
2. Si c'est un autre fichier, le supprimer ou l'ajouter au `.gitignore`

### Erreur: ".env.ready still tracked by Git"
**Solution**:
```bash
git rm --cached apps/video-studio/.env.ready
git commit -m "security: remove .env.ready from tracking"
```

### Impossible de générer JWT_SECRET_KEY
**Solution**: Utilisez https://generate-secret.vercel.app/64 et copiez le résultat

---

## Prochaine Étape

Une fois les 5 checks validés:

```bash
cd services\api
deploy_zero_risque.bat
```

Cela appliquera la migration SQL et démarrera l'API avec les nouvelles clés.

**Temps total**: 20 minutes ⏱️
