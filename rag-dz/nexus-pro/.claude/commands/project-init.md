# /project-init

Initialise le projet Nexus AI Platform.

## Étapes

1. Vérifier l'environnement
```bash
docker --version && docker compose version && git --version && node --version && python --version
```

2. Créer la structure si nécessaire
```bash
mkdir -p orchestrators/{meta,bmad,archon,bolt}/src
mkdir -p orchestrators/shared
mkdir -p {scripts,docs,requirements}
```

3. Initialiser les submodules
```bash
git submodule update --init --recursive
```

4. Vérifier .env
```bash
if [ ! -f .env ]; then
    echo "⚠️ Copiez .env.example vers .env"
    cp .env.example .env
fi
```

5. Valider docker-compose
```bash
docker compose config
```

## Résultat attendu

```
✅ Docker OK
✅ Git OK  
✅ Node OK
✅ Python OK
✅ Structure créée
✅ Submodules initialisés
✅ .env configuré
✅ docker-compose.yml valide

Prêt pour PRP-001
```
