# 🔧 Correction et Démarrage

## ✅ Problèmes Corrigés

1. ✅ Dockerfile backend : Ajout des dépendances système manquantes
2. ✅ docker-compose.yml : Suppression de `version: '3.8'` (obsolète)
3. ✅ Dockerfile frontend : Correction du port (5173)

---

## 🚀 Maintenant, Démarrer les Services

### Étape 1 : Configuration .env

```powershell
# Créer .env depuis le template
Copy-Item .env.example .env

# Éditer .env
notepad .env
```

**Configuration MINIMALE dans `.env` :**
```env
# Générer avec: openssl rand -hex 32
# Ou utiliser temporairement:
API_SECRET_KEY=temp-secret-key-for-testing-only-change-in-production

# Choisir un mot de passe
POSTGRES_PASSWORD=ragdz2024secure

# Le reste peut rester par défaut
```

---

### Étape 2 : Build et Démarrage

```powershell
# Build les images (prend 5-10 minutes la première fois)
docker-compose build

# Démarrer tous les services
docker-compose up -d

# Attendre que tout démarre (60 secondes)
Start-Sleep -Seconds 60
```

---

### Étape 3 : Vérification

```powershell
# Voir le status
docker-compose ps

# Devrait afficher quelque chose comme:
# NAME                STATUS              PORTS
# ragdz-backend       Up (healthy)        0.0.0.0:8180->8180/tcp
# ragdz-postgres      Up (healthy)        0.0.0.0:5432->5432/tcp
# ragdz-redis         Up (healthy)        0.0.0.0:6379->6379/tcp
# etc.
```

**Vérifier les logs si problème :**
```powershell
docker-compose logs backend
docker-compose logs postgres
```

---

### Étape 4 : Test

```powershell
# Test manuel backend
curl http://localhost:8180/health

# Si ça marche, lancer le test complet
python test_all_interfaces.py
```

---

## 🔍 Si le Build Échoue Encore

### Backend ne build pas

```powershell
# Voir les détails de l'erreur
docker-compose build backend --no-cache

# Si erreur sur torch ou librosa:
# C'est normal, le téléchargement est long
# Attendre jusqu'à la fin du build
```

### Frontend ne build pas

```powershell
# Build frontend séparément
docker-compose build frontend --no-cache

# Voir les logs détaillés
docker-compose logs frontend
```

---

## 📊 Ordre de Démarrage Recommandé

Si `docker-compose up -d` pose problème, démarrer dans l'ordre :

```powershell
# 1. Base de données
docker-compose up -d postgres
Start-Sleep -Seconds 30

docker-compose up -d redis qdrant
Start-Sleep -Seconds 10

# 2. Vérifier que la DB est prête
docker-compose logs postgres | Select-String "ready to accept"

# 3. Backend
docker-compose up -d backend
Start-Sleep -Seconds 20

# 4. Frontend et monitoring
docker-compose up -d frontend prometheus grafana

# 5. Vérifier tout
docker-compose ps
```

---

## 🚨 Dépannage

### Erreur : "port already allocated"

```powershell
# Trouver qui utilise le port
netstat -ano | findstr :8180

# Tuer le processus ou changer le port dans docker-compose.yml
```

### Erreur : PostgreSQL ne démarre pas

```powershell
# Voir les logs
docker-compose logs postgres

# Redémarrer
docker-compose restart postgres
Start-Sleep -Seconds 30
docker-compose restart backend
```

### Erreur : "pip install failed"

Le build peut prendre **5-10 minutes** car il télécharge PyTorch (~800MB).
Soyez patient et ne pas annuler !

Si vraiment ça échoue :
```powershell
# Build sans cache
docker-compose build --no-cache backend

# OU simplifier requirements.txt temporairement
# (commenter torch, librosa, transformers si juste pour tester)
```

---

## ✅ Checklist de Vérification

Avant de lancer le test :

- [ ] `.env` existe et contient `API_SECRET_KEY` et `POSTGRES_PASSWORD`
- [ ] `docker-compose build` a réussi (peut prendre 5-10 min)
- [ ] `docker-compose up -d` lancé
- [ ] Attendu 60 secondes minimum
- [ ] `docker-compose ps` montre tous les services "Up"
- [ ] `curl http://localhost:8180/health` retourne JSON
- [ ] Pas d'erreurs dans `docker-compose logs`

---

## 🎯 Commandes Complètes (Copier-Coller)

### Option 1 : Build Complet

```powershell
# PowerShell - Tout en une fois
cd C:\Users\bbens\rag-dz

# Config
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "⚠️  Éditez .env maintenant !"
    notepad .env
    Read-Host "Appuyez sur Entrée après avoir configuré .env"
}

# Build (5-10 minutes)
Write-Host "🔨 Build des images (ceci peut prendre 5-10 minutes)..."
docker-compose build

# Démarrage
Write-Host "🚀 Démarrage des services..."
docker-compose up -d

# Attente
Write-Host "⏳ Attente du démarrage (60 secondes)..."
Start-Sleep -Seconds 60

# Vérification
Write-Host "📊 Status des services:"
docker-compose ps

# Test
Write-Host "🧪 Test du backend:"
curl http://localhost:8180/health

Write-Host "`n✅ Si le backend répond, lancez: python test_all_interfaces.py"
```

### Option 2 : Build Progressif (Recommandé si problèmes)

```powershell
# 1. Build backend seulement
docker-compose build backend

# 2. Build frontend seulement
docker-compose build frontend

# 3. Démarrer progressivement
docker-compose up -d postgres redis qdrant
Start-Sleep -Seconds 30

docker-compose up -d backend
Start-Sleep -Seconds 20

docker-compose up -d frontend prometheus grafana

# 4. Vérifier
docker-compose ps
docker-compose logs --tail=50
```

---

## 📞 Prochaines Étapes

Une fois que `docker-compose ps` montre tous les services "Up" :

1. Lancer le test : `python test_all_interfaces.py`
2. Ouvrir les interfaces :
   - Frontend: http://localhost:5173
   - API Docs: http://localhost:8180/docs
   - Grafana: http://localhost:3001

---

**Le build peut prendre 5-10 minutes la première fois (téléchargement PyTorch). Soyez patient ! 🕐**
