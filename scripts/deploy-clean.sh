#!/bin/bash
# Déploiement destructif : écrase tout, nettoie le dossier cible, vérifie et stoppe les conteneurs Docker
# Usage : bash deploy-clean.sh

TARGET_DIR="/var/www/app.iafactoryalgeria.com"
BACKUP_DIR="/var/www/app.iafactoryalgeria.com_backup_$(date +%Y%m%d_%H%M%S)"

# 1. Backup (optionnel, décommentez si besoin)
# echo "Backup de $TARGET_DIR vers $BACKUP_DIR ..."
# cp -r $TARGET_DIR $BACKUP_DIR

# 2. Nettoyage du dossier cible
if [ -d "$TARGET_DIR" ]; then
  echo "Suppression de tout le contenu de $TARGET_DIR ..."
  rm -rf $TARGET_DIR/*
else
  echo "Création du dossier $TARGET_DIR ..."
  mkdir -p $TARGET_DIR
fi

# 3. Vérification et arrêt des conteneurs Docker liés à l'app (si Docker utilisé)
if command -v docker &> /dev/null; then
  echo "Vérification des conteneurs Docker en cours ..."
  docker ps --format '{{.Names}}' | grep iafactory | while read cname; do
    echo "Arrêt du conteneur $cname ..."
    docker stop "$cname"
    docker rm "$cname"
  done
fi

echo "Dossier prêt pour le nouveau déploiement."
# 4. (Le pipeline CI/CD copiera ensuite les nouveaux fichiers ici)
