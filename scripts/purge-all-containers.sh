#!/bin/bash
# Script pour stopper et supprimer TOUS les conteneurs Docker (dangereux, tout sera supprimé)
# Usage : bash purge-all-containers.sh

echo "Arrêt de tous les conteneurs Docker..."
docker stop $(docker ps -aq)

echo "Suppression de tous les conteneurs Docker..."
docker rm $(docker ps -aq)

echo "Nettoyage terminé. Tous les conteneurs sont supprimés."
