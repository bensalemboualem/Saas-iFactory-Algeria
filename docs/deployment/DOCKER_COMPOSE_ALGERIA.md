# Déploiement IAFactory Algeria

> Guide de déploiement avec Docker Compose

---

## Fichiers Docker Compose

| Fichier | Usage |
|---------|-------|
| `docker-compose.algeria.yml` | Développement local |
| `docker-compose.algeria.prod.yml` | Production |

---

## Développement Local

### Lancer l'environnement

```bash
cd docker-compose
docker-compose -f docker-compose.algeria.yml up -d
```

### Services disponibles

| Service | URL | Port |
|---------|-----|------|
| Frontend | http://localhost:3010 | 3010 |
| API | http://localhost:8000 | 8000 |
| PostgreSQL | localhost:5432 | 5432 |
| Redis | localhost:6379 | 6379 |

### Arrêter l'environnement

```bash
docker-compose -f docker-compose.algeria.yml down
```

---

## Production

### Prérequis

- VPS avec Docker installé
- Domaine configuré (iafactoryalgeria.com)
- Certificat SSL (Let's Encrypt)

### Déploiement

```bash
cd docker-compose
docker-compose -f docker-compose.algeria.prod.yml up -d
```

### Vérification

```bash
# Vérifier les services
docker-compose -f docker-compose.algeria.prod.yml ps

# Logs
docker-compose -f docker-compose.algeria.prod.yml logs -f
```

---

## Variables d'Environnement

### Fichier .env.algeria

```env
# === RÉGION ===
REGION=algeria
TIMEZONE=Africa/Algiers
DEFAULT_LOCALE=fr-FR

# === DOMAINE ===
DOMAIN=iafactoryalgeria.com
API_URL=https://api.iafactoryalgeria.com
APP_URL=https://app.iafactoryalgeria.com

# === BASE DE DONNÉES ===
DATABASE_URL=postgresql://user:password@db:5432/iafactory
REDIS_URL=redis://redis:6379

# === PAIEMENT ===
PAYMENT_PROVIDER=chargily
PAYMENT_CURRENCY=DZD
CHARGILY_API_KEY=your_api_key
CHARGILY_SECRET_KEY=your_secret_key

# === AUTHENTIFICATION ===
AUTH_SECRET=your_auth_secret
NEXTAUTH_URL=https://app.iafactoryalgeria.com

# === IA ===
ANTHROPIC_API_KEY=your_key
OPENAI_API_KEY=your_key
DEEPSEEK_API_KEY=your_key
```

---

## Commandes Utiles

```bash
# Rebuild les images
docker-compose -f docker-compose.algeria.yml build

# Voir les logs d'un service
docker-compose -f docker-compose.algeria.yml logs api

# Accéder à un conteneur
docker-compose -f docker-compose.algeria.yml exec api sh

# Backup base de données
docker-compose -f docker-compose.algeria.yml exec db pg_dump -U user iafactory > backup.sql
```

---

## Support

- **Email:** support@iafactoryalgeria.com
