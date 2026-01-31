# ⚡ DÉPLOIEMENT RAPIDE - 5 MINUTES

## 🎯 PRÉ-REQUIS

✅ VPS Hetzner actif
✅ Accès SSH root
✅ Toutes les clés API obtenues (Fal.ai, Replicate, ElevenLabs, Stripe, Cloudflare R2)

---

## 🚀 DÉPLOIEMENT EN 3 COMMANDES

### **1. COPIER LES FICHIERS SUR LE VPS** (2 min)

**Depuis votre machine locale:**
```bash
# Copier tout le dossier video-studio vers le VPS
scp -r D:\IAFactory\rag-dz\apps\video-studio root@VOTRE_IP_VPS:/opt/iafactory/

# OU via Git (si le repo est sur GitHub)
ssh root@VOTRE_IP_VPS
cd /opt/iafactory
git clone https://github.com/VOTRE_ORG/rag-dz.git
```

---

### **2. LANCER LE SCRIPT D'INSTALLATION** (2 min)

**Sur le VPS:**
```bash
# Se connecter au VPS
ssh root@VOTRE_IP_VPS

# Aller dans le dossier
cd /opt/iafactory/video-studio

# Rendre le script exécutable
chmod +x deploy.sh

# Lancer l'installation automatique
./deploy.sh
```

**Le script va:**
- ✅ Installer Docker + Docker Compose
- ✅ Installer FFmpeg
- ✅ Installer Nginx
- ✅ Créer le fichier .env
- ✅ Lancer les containers

---

### **3. CONFIGURER VOS CLÉS API** (1 min)

```bash
# Éditer le .env avec vos vraies clés
cd /opt/iafactory/rag-dz/apps/video-studio
nano .env
```

**Remplacez UNIQUEMENT ces lignes:**
```bash
FAL_KEY=fal_VOTRE_VRAIE_CLE
REPLICATE_API_TOKEN=r8_VOTRE_VRAI_TOKEN
ELEVENLABS_API_KEY=sk_VOTRE_VRAIE_CLE
S3_ACCESS_KEY=VOTRE_VRAIE_CLE_R2
S3_SECRET_KEY=VOTRE_VRAI_SECRET_R2
S3_ENDPOINT=https://VOTRE_ACCOUNT_ID.r2.cloudflarestorage.com
STRIPE_PUBLISHABLE_KEY=pk_live_VOTRE_VRAIE_CLE
STRIPE_SECRET_KEY=sk_live_VOTRE_VRAIE_CLE
STRIPE_WEBHOOK_SECRET=whsec_VOTRE_VRAI_SECRET
```

**Générer les secrets JWT:**
```bash
# Génération automatique des secrets
JWT_SECRET=$(openssl rand -base64 32)
NEXTAUTH_SECRET=$(openssl rand -base64 32)

# Les copier dans le .env
echo "JWT_SECRET=$JWT_SECRET"
echo "NEXTAUTH_SECRET=$NEXTAUTH_SECRET"
```

**Sauvegarder:** `Ctrl+X` → `Y` → `Enter`

**Redémarrer les services:**
```bash
docker-compose restart
```

---

## 🌐 CONFIGURATION DNS + SSL (Bonus - 5 min)

### **1. Configurer vos DNS**

**Sur Cloudflare (ou votre registrar):**
```
Type A: video-studio.iafactoryalgeria.com → VOTRE_IP_VPS
Type A: api.iafactoryalgeria.com → VOTRE_IP_VPS
```

**Attendre 2-5 minutes que les DNS se propagent.**

---

### **2. Configurer Nginx + SSL**

```bash
cd /opt/iafactory/rag-dz/apps/video-studio

# Rendre le script exécutable
chmod +x setup-nginx.sh

# Lancer la configuration automatique
./setup-nginx.sh
```

**Le script va demander:**
- Domaine frontend: `video-studio.iafactoryalgeria.com`
- Domaine API: `api.iafactoryalgeria.com`
- Email Let's Encrypt: `votre@email.com`

**Il va ensuite:**
- ✅ Configurer Nginx reverse proxy
- ✅ Obtenir les certificats SSL
- ✅ Activer HTTPS automatiquement

---

## ✅ VÉRIFICATION

### **Tester que tout fonctionne:**

```bash
# 1. Backend API
curl https://api.iafactoryalgeria.com/health
# Doit retourner: {"status":"healthy",...}

# 2. Documentation API
curl https://api.iafactoryalgeria.com/docs
# Doit retourner du HTML (Swagger UI)

# 3. Frontend (dans le navigateur)
https://video-studio.iafactoryalgeria.com
# Doit afficher la page d'accueil
```

---

## 📊 COMMANDES UTILES

```bash
# Voir l'état des services
cd /opt/iafactory/rag-dz/apps/video-studio
docker-compose ps

# Voir les logs en temps réel
docker-compose logs -f

# Redémarrer un service
docker-compose restart backend
docker-compose restart frontend

# Arrêter tout
docker-compose down

# Redémarrer tout
docker-compose up -d

# Rebuild après modification
docker-compose up -d --build

# Voir l'utilisation des ressources
docker stats
```

---

## 🔧 TROUBLESHOOTING

### **Problème: "Connection refused"**
```bash
# Vérifier que les containers tournent
docker-compose ps

# Voir les logs
docker-compose logs backend
docker-compose logs frontend
```

### **Problème: "Database connection failed"**
```bash
# Se connecter à PostgreSQL
docker exec -it video-studio-db-1 psql -U postgres

# Lister les bases
\l

# Se connecter à la DB
\c iafactory_video

# Lister les tables
\dt

# Quitter
\q
```

### **Problème: Backend démarre mais erreurs dans les logs**
```bash
# Vérifier le .env
cat .env | grep -E "FAL_KEY|REPLICATE|ELEVENLABS"

# Vérifier que les clés API sont valides
# Tester manuellement chaque API
```

### **Problème: Frontend affiche erreur 502**
```bash
# Le backend n'est probablement pas démarré
docker-compose restart backend

# Attendre 30s puis tester
curl http://localhost:8000/health
```

---

## 🎉 C'EST EN PROD!

Si tous les tests passent, votre application est en production!

**Accès:**
- 🌐 Frontend: https://video-studio.iafactoryalgeria.com
- 🔧 API: https://api.iafactoryalgeria.com
- 📚 Documentation: https://api.iafactoryalgeria.com/docs

**Prochaines étapes:**
1. ✅ Tester la génération de vidéos
2. ✅ Configurer les webhooks Stripe
3. ✅ Activer le monitoring (Sentry)
4. ✅ Configurer les backups automatiques

---

## 📞 BESOIN D'AIDE?

**Erreurs courantes et solutions:**
- Voir `DEPLOY_VPS.md` section Troubleshooting
- Consulter les logs: `docker-compose logs -f`
- Vérifier la checklist: `PRODUCTION_CHECKLIST.md`

**Si rien ne fonctionne:**
1. Vérifier que Docker tourne: `docker ps`
2. Vérifier le .env: `cat .env`
3. Redémarrer tout: `docker-compose down && docker-compose up -d`
