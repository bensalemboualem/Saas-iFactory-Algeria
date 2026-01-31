# Déploiement IAFactory Algeria

## Fichiers Docker
- docker-compose.algeria.yml (Développement)
- docker-compose.algeria.prod.yml (Production)

## Variables d'environnement
REGION=algeria
CURRENCY=DZD
TIMEZONE=Africa/Algiers
PAYMENT_PROVIDER=chargily

## Commandes
# Développement
docker-compose -f docker-compose.algeria.yml up

# Production
docker-compose -f docker-compose.algeria.prod.yml up -d
