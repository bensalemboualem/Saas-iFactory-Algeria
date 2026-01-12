# prompt-creator

> Application prompt-creator - IAFactory SaaS Platform

## Status

| Aspect | Valeur |
|--------|--------|
| **Production** | [DEV] En developpement |
| **Stack** | HTML/CSS/JS |
| **Tests** | A implementer |
| **Documentation** | Ce fichier |

## Description

Application prompt-creator faisant partie de la plateforme IAFactory.
Service backend/API.

## Quick Start

### Installation

```bash
# No dependencies

# Backend (si applicable)
cd backend
pip install -r requirements.txt
```

### Developpement

```bash
# Open index.html in browser

# Backend
cd backend
uvicorn app.main:app --reload --port 8000
```

### Build

```bash
# No build required
```

## Structure

```
prompt-creator/
    backend/
    docs/
    frontend/
    templates/

```

## Configuration

Copier `.env.example` vers `.env` et configurer les variables:

```env
# API
API_URL=http://localhost:8000

# Voir .env.example pour la liste complete
```

## API Endpoints


| Methode | Endpoint | Description |
|---------|----------|-------------|
| GET | /api/v1/health | Health check |
| ... | ... | A documenter |


## TODO

- [ ] Completer la documentation
- [ ] Ajouter tests unitaires
- [ ] Ajouter tests integration
- [ ] Configurer CI/CD

## Liens

- [Documentation principale](../../docs/README.md)
- [Architecture](../../docs/ARCHITECTURE.md)
- [Audit](../../docs/AUDIT.md)

---

*IAFactory SaaS Platform - Generated 2025-12-20*
