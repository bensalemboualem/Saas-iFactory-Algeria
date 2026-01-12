# REVOCATION URGENTE - CLES API EXPOSEES

**STATUT**: A EXECUTER IMMEDIATEMENT
**Temps estime**: 30-45 minutes
**Date**: 30 Decembre 2025

---

## ACTIONS AUTOMATIQUES COMPLETEES

Les actions suivantes ont ete effectuees automatiquement:

| Action | Fichier | Statut |
|--------|---------|--------|
| Cree .env.example securise | `iafactory-academy/.env.example` | OK |
| Corrige .env.example avec secrets | `onestschooled/.env.example` | OK |
| Cree .env.new template | `rag-dz/.env.new` | OK |
| Cree .env.new template | `iafactory-academy/.env.new` | OK |
| Cree .env.new template | `onestschooled/.env.new` | OK |
| Supprime password hardcode Grafana | `docker-compose.observability.yml` | OK |

### Prochaines etapes MANUELLES:

1. **REVOQUER les cles** (voir guide ci-dessous)
2. **Remplir les .env.new** avec les nouvelles cles
3. **Renommer**: `mv .env.new .env`
4. **Tester** chaque application

---

## CHECKLIST RAPIDE

```
[ ] 1. OpenAI (iafactory-academy)
[ ] 2. Anthropic (iafactory-academy)
[ ] 3. Google AI (rag-dz + iafactory-academy)
[ ] 4. Mistral (rag-dz + iafactory-academy)
[ ] 5. Groq (iafactory-academy)
[ ] 6. DeepSeek (rag-dz)
[ ] 7. Cohere (rag-dz)
[ ] 8. Together AI (rag-dz)
[ ] 9. OpenRouter (rag-dz)
[ ] 10. Supabase (rag-dz + iafactory-academy)
[ ] 11. Stripe (onestschooled)
[ ] 12. AWS S3 (iafactory-academy)
[ ] 13. Mots de passe DB + Mail (onestschooled)
[ ] 14. Nettoyer historique Git
[ ] 15. Creer nouveaux .env.example
```

---

## 1. OPENAI

**Cle exposee dans**: `iafactory-academy/.env`
```
OPENAI_API_KEY=sk-proj-ysvcisY37XVws6sIMnjCFnUKh-...
```

### Action:
1. Ouvrir: https://platform.openai.com/api-keys
2. Cliquer sur la cle `sk-proj-ysvcisY37XVws6sIMnjCFnUKh...`
3. Cliquer **"Revoke key"**
4. Creer une nouvelle cle
5. Copier la nouvelle cle (elle ne sera plus visible apres)

### Mettre a jour:
```bash
# iafactory-academy/.env
OPENAI_API_KEY=sk-proj-NOUVELLE_CLE_ICI
```

---

## 2. ANTHROPIC

**Cle exposee dans**: `iafactory-academy/.env`
```
ANTHROPIC_API_KEY=sk-ant-api03-KXmMM4l1RKlMUxyjAxC44lNLDN7e8mRwr4...
```

### Action:
1. Ouvrir: https://console.anthropic.com/settings/keys
2. Trouver la cle commencant par `sk-ant-api03-KXmMM4l1...`
3. Cliquer **"Delete"**
4. Cliquer **"Create Key"**
5. Nommer: `iafactory-academy-prod`

### Mettre a jour:
```bash
# iafactory-academy/.env
ANTHROPIC_API_KEY=sk-ant-api03-NOUVELLE_CLE_ICI
```

---

## 3. GOOGLE AI (Generative AI / Gemini)

**Cles exposees dans**:
- `rag-dz/.env`: `AIzaSyB21Sv2aZEJ33TJ02dfLMx-PklP4ZVcG40`
- `iafactory-academy/.env`: `AIzaSyB-jLhkFVfPtOs1txBjzu0anKk1BXWDsdg`

### Action:
1. Ouvrir: https://console.cloud.google.com/apis/credentials
2. Dans "API Keys", trouver les 2 cles
3. Cliquer sur chaque cle > **"DELETE KEY"**
4. Cliquer **"+ CREATE CREDENTIALS" > "API Key"**
5. **IMPORTANT**: Restreindre la cle:
   - Cliquer "Edit API key"
   - "API restrictions" > "Restrict key"
   - Selectionner: "Generative Language API"
   - "Application restrictions" > IP addresses (prod) ou None (dev)

### Mettre a jour:
```bash
# rag-dz/.env
GOOGLE_GENERATIVE_AI_API_KEY=AIzaNOUVELLE_CLE_RAG_DZ

# iafactory-academy/.env
GOOGLE_GENERATIVE_AI_API_KEY=AIzaNOUVELLE_CLE_ACADEMY
```

---

## 4. MISTRAL AI

**Cle exposee dans**: `rag-dz/.env` ET `iafactory-academy/.env`
```
MISTRAL_API_KEY=U4TD40GfA96d4txjFQzQSps2PXaxKYHC
```
*Note: Meme cle utilisee dans les 2 projets!*

### Action:
1. Ouvrir: https://console.mistral.ai/api-keys
2. Supprimer la cle `U4TD40GfA...`
3. Creer 2 nouvelles cles:
   - `rag-dz-prod`
   - `iafactory-academy-prod`

### Mettre a jour:
```bash
# rag-dz/.env
MISTRAL_API_KEY=NOUVELLE_CLE_RAG_DZ

# iafactory-academy/.env
MISTRAL_API_KEY=NOUVELLE_CLE_ACADEMY
```

---

## 5. GROQ

**Cle exposee dans**: `iafactory-academy/.env`
```
GROQ_API_KEY=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
```

### Action:
1. Ouvrir: https://console.groq.com/keys
2. Supprimer la cle `gsk_mw3p2HWS...`
3. Creer une nouvelle cle

### Mettre a jour:
```bash
# iafactory-academy/.env
GROQ_API_KEY=gsk_NOUVELLE_CLE_ICI
```

---

## 6. DEEPSEEK

**Cle exposee dans**: `rag-dz/.env`
```
DEEPSEEK_API_KEY=sk-e2d7d214600946479856ffafbe1ce392
```

### Action:
1. Ouvrir: https://platform.deepseek.com/api_keys
2. Supprimer la cle exposee
3. Creer une nouvelle cle

### Mettre a jour:
```bash
# rag-dz/.env
DEEPSEEK_API_KEY=sk-NOUVELLE_CLE_ICI
```

---

## 7. COHERE

**Cle exposee dans**: `rag-dz/.env`
```
COHERE_API_KEY=bAVVqL7U4wv2gmd4gbGBQwpVXDEGZqFm42czSg3a
```

### Action:
1. Ouvrir: https://dashboard.cohere.com/api-keys
2. Cliquer sur la cle > **"Delete"**
3. Cliquer **"+ Create API Key"**

### Mettre a jour:
```bash
# rag-dz/.env
COHERE_API_KEY=NOUVELLE_CLE_ICI
```

---

## 8. TOGETHER AI

**Cle exposee dans**: `rag-dz/.env`
```
TOGETHER_API_KEY=99ac6265846d3cb6a8f83e038605d01a...
```

### Action:
1. Ouvrir: https://api.together.xyz/settings/api-keys
2. Supprimer la cle existante
3. Generer une nouvelle cle

### Mettre a jour:
```bash
# rag-dz/.env
TOGETHER_API_KEY=NOUVELLE_CLE_ICI
```

---

## 9. OPENROUTER

**Cle exposee dans**: `rag-dz/.env`
```
OPEN_ROUTER_API_KEY=sk-or-v1-b096b9798cd36d238b56f7d5476dbedb...
```

### Action:
1. Ouvrir: https://openrouter.ai/keys
2. Supprimer la cle `sk-or-v1-b096b9...`
3. Creer une nouvelle cle

### Mettre a jour:
```bash
# rag-dz/.env
OPEN_ROUTER_API_KEY=sk-or-v1-NOUVELLE_CLE_ICI
```

---

## 10. SUPABASE

**Cles exposees dans**: `rag-dz/.env`, `iafactory-academy/.env`
```
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Action:
1. Ouvrir: https://supabase.com/dashboard
2. Selectionner le projet
3. **Settings** > **API**
4. Section "Service Role Key" > **"Generate new key"**
5. **ATTENTION**: Cela invalidera immediatement l'ancienne cle!

### Mettre a jour:
```bash
# rag-dz/.env
SUPABASE_URL=https://votre-projet.supabase.co
SUPABASE_ANON_KEY=eyJ...NOUVEAU_ANON
SUPABASE_SERVICE_KEY=eyJ...NOUVEAU_SERVICE

# iafactory-academy/.env (si applicable)
SUPABASE_URL=https://votre-projet.supabase.co
SUPABASE_ANON_KEY=eyJ...NOUVEAU_ANON
SUPABASE_SERVICE_KEY=eyJ...NOUVEAU_SERVICE
```

---

## 11. STRIPE

**Cles exposees dans**: `onestschooled/.env`
```
STRIPE_KEY=pk_test_51RLKWDRqrKCv3tOsLdcQNSogKq740paUlep...
STRIPE_SECRET=sk_test_51RLKWDRqrKCv3tOsArRKYCi2XTXi4CzKaR0...
```

### Action:
1. Ouvrir: https://dashboard.stripe.com/apikeys
2. Pour la **Test Mode** (ce sont des cles test):
   - Cliquer "Roll key" sur la Secret key
   - La Publishable key n'a pas besoin d'etre changee (publique)
3. Si vous avez aussi des cles **Live** exposees:
   - Switcher en "Live mode"
   - "Roll key" sur la Secret key
   - **ATTENTION**: Les paiements en cours seront interrompus!

### Mettre a jour:
```bash
# onestschooled/.env
STRIPE_KEY=pk_test_MEME_CLE_OK
STRIPE_SECRET=sk_test_NOUVELLE_SECRET_KEY
```

---

## 12. AWS S3

**Cles exposees dans**: `iafactory-academy/.env`
```
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
```

### Action:
1. Ouvrir: https://console.aws.amazon.com/iam/home#/security_credentials
2. Ou via IAM: https://console.aws.amazon.com/iam/home#/users
3. Selectionner l'utilisateur
4. **Security credentials** > **Access keys**
5. Cliquer **"Make inactive"** sur l'ancienne cle
6. Cliquer **"Create access key"**
7. Une fois la nouvelle cle testee, **supprimer** l'ancienne

### Mettre a jour:
```bash
# iafactory-academy/.env
AWS_ACCESS_KEY_ID=AKIANOUVEAUCLE
AWS_SECRET_ACCESS_KEY=NOUVELLE_SECRET_KEY
AWS_REGION=eu-west-3
AWS_BUCKET_NAME=votre-bucket
```

---

## 13. MOTS DE PASSE DB + MAIL (onestschooled)

**Exposes dans**: `onestschooled/.env`
```
DB_PASSWORD="mYDbp@ass123"
MAIL_PASSWORD="121211"
```

### Action Base de Donnees:
```sql
-- Se connecter a MySQL en tant que root
mysql -u root -p

-- Changer le mot de passe
ALTER USER 'onestschooled'@'localhost' IDENTIFIED BY 'NouveauMotDePasse$ecure2025!';
FLUSH PRIVILEGES;
```

### Action Mail (Gmail/SMTP):
1. Si Gmail: https://myaccount.google.com/apppasswords
   - Revoquer l'ancien mot de passe d'application
   - Creer un nouveau
2. Si autre provider: Changer dans le dashboard du provider

### Mettre a jour:
```bash
# onestschooled/.env
DB_PASSWORD="NouveauMotDePasse$ecure2025!"
MAIL_PASSWORD="nouveau_app_password"
```

---

## 14. NETTOYER L'HISTORIQUE GIT

**CRITIQUE**: Meme apres avoir change les cles, elles restent dans l'historique Git!

### Pour chaque projet:

```bash
# === RAG-DZ ===
cd D:\IAFactory\rag-dz

# Verifier si c'est un repo git
git status

# Si oui, supprimer .env de l'historique
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env .env.local .env.production .env.development" \
  --prune-empty --tag-name-filter cat -- --all

# Nettoyer les references
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (COORDINATION EQUIPE REQUISE!)
git push origin --force --all
git push origin --force --tags
```

```bash
# === IAFACTORY-ACADEMY ===
cd D:\IAFactory\iafactory-academy

git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env backend/.env frontend/.env demo/**/.env" \
  --prune-empty --tag-name-filter cat -- --all

git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push origin --force --all
```

```bash
# === ONESTSCHOOLED ===
cd D:\IAFactory\onestschooled

git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push origin --force --all
```

### Alternative plus simple avec BFG:

```bash
# Installer BFG (plus rapide que filter-branch)
# Telecharger: https://rtyley.github.io/bfg-repo-cleaner/

# Utilisation
java -jar bfg.jar --delete-files .env D:\IAFactory\rag-dz
cd D:\IAFactory\rag-dz
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push --force
```

---

## 15. CREER .env.example POUR CHAQUE PROJET

### rag-dz/.env.example
```bash
# === DATABASE ===
DATABASE_URL=postgresql://user:password@localhost:5432/ragdz
REDIS_URL=redis://localhost:6379

# === LLM PROVIDERS ===
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
GOOGLE_GENERATIVE_AI_API_KEY=AIza-your-key-here
MISTRAL_API_KEY=your-key-here
DEEPSEEK_API_KEY=sk-your-key-here
COHERE_API_KEY=your-key-here
TOGETHER_API_KEY=your-key-here
OPEN_ROUTER_API_KEY=sk-or-v1-your-key-here
GROQ_API_KEY=gsk_your-key-here

# === SUPABASE ===
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# === VECTOR DB ===
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your-key-here

# === ENVIRONMENT ===
ENVIRONMENT=development
DEBUG=false
```

### iafactory-academy/.env.example
```bash
# === DATABASE ===
DATABASE_URL=postgresql://user:password@localhost:5432/academy
REDIS_URL=redis://localhost:6379

# === LLM PROVIDERS ===
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
GOOGLE_GENERATIVE_AI_API_KEY=AIza-your-key-here
MISTRAL_API_KEY=your-key-here
GROQ_API_KEY=gsk_your-key-here

# === SUPABASE ===
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# === AWS ===
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=eu-west-3
AWS_BUCKET_NAME=your-bucket

# === EMAIL ===
SENDGRID_API_KEY=your-sendgrid-key

# === STRIPE ===
STRIPE_SECRET_KEY=sk_test_your-key
STRIPE_WEBHOOK_SECRET=whsec_your-secret

# === ENVIRONMENT ===
ENVIRONMENT=development
DEBUG=false
SECRET_KEY=generate-with-openssl-rand-hex-32
```

### onestschooled/.env.example
```bash
APP_NAME=OneStSchooled
APP_ENV=local
APP_KEY=base64:generate-with-php-artisan-key-generate
APP_DEBUG=false
APP_URL=http://localhost

# === DATABASE ===
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=onestschooled
DB_USERNAME=your_username
DB_PASSWORD=your_secure_password

# === MAIL ===
MAIL_MAILER=smtp
MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_ENCRYPTION=tls

# === STRIPE ===
STRIPE_KEY=pk_test_your_publishable_key
STRIPE_SECRET=sk_test_your_secret_key

# === FIREBASE ===
FIREBASE_CREDENTIALS=path/to/firebase-credentials.json

# === TENANT ===
TENANT_DOMAIN=localhost
```

---

## VERIFICATION POST-REVOCATION

Apres avoir revoque toutes les cles, verifier que tout fonctionne:

### Script de test rapide:

```bash
# Tester rag-dz
cd D:\IAFactory\rag-dz
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('OpenAI:', 'OK' if os.getenv('OPENAI_API_KEY') else 'MISSING')
print('Anthropic:', 'OK' if os.getenv('ANTHROPIC_API_KEY') else 'MISSING')
print('Google:', 'OK' if os.getenv('GOOGLE_GENERATIVE_AI_API_KEY') else 'MISSING')
"

# Tester un appel API simple
curl -X POST http://localhost:8000/api/health
```

```bash
# Tester iafactory-academy
cd D:\IAFactory\iafactory-academy
docker-compose up -d
curl http://localhost:8000/health
```

```bash
# Tester onestschooled
cd D:\IAFactory\onestschooled
php artisan config:clear
php artisan cache:clear
php artisan serve
# Verifier que le site charge
```

---

## RECAPITULATIF

| Provider | Lien Direct | Statut |
|----------|-------------|--------|
| OpenAI | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) | [ ] |
| Anthropic | [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys) | [ ] |
| Google AI | [console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials) | [ ] |
| Mistral | [console.mistral.ai/api-keys](https://console.mistral.ai/api-keys) | [ ] |
| Groq | [console.groq.com/keys](https://console.groq.com/keys) | [ ] |
| DeepSeek | [platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys) | [ ] |
| Cohere | [dashboard.cohere.com/api-keys](https://dashboard.cohere.com/api-keys) | [ ] |
| Together | [api.together.xyz/settings/api-keys](https://api.together.xyz/settings/api-keys) | [ ] |
| OpenRouter | [openrouter.ai/keys](https://openrouter.ai/keys) | [ ] |
| Supabase | [supabase.com/dashboard](https://supabase.com/dashboard) | [ ] |
| Stripe | [dashboard.stripe.com/apikeys](https://dashboard.stripe.com/apikeys) | [ ] |
| AWS | [console.aws.amazon.com/iam](https://console.aws.amazon.com/iam/home#/security_credentials) | [ ] |

---

## APRES LA REVOCATION

Une fois toutes les cles revoquees:

1. [ ] Mettre a jour le `.gitignore` de chaque projet:
   ```
   .env
   .env.local
   .env.production
   .env.*.local
   ```

2. [ ] Commiter les `.env.example`:
   ```bash
   git add .env.example
   git commit -m "Add .env.example template (secrets removed)"
   ```

3. [ ] Informer l'equipe du force push:
   ```
   ⚠️ Force push effectue sur [repo]
   Tous les membres doivent faire:
   git fetch origin
   git reset --hard origin/main
   ```

4. [ ] Configurer un secrets manager pour le futur:
   - Dev: fichiers `.env` locaux (jamais commits)
   - Prod: HashiCorp Vault, AWS Secrets Manager, ou GitHub Secrets

---

*Guide genere le 30 Decembre 2025*
*Temps estime: 30-45 minutes*
*Priorite: CRITIQUE - A faire MAINTENANT*
