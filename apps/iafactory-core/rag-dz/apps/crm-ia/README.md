# crm-ia

> Application crm-ia - IAFactory SaaS Platform

## Status

| Aspect | Valeur |
|--------|--------|
| **Production** | [DEV] En developpement |
| **Stack** | Python/FastAPI |
| **Tests** | A implementer |
| **Documentation** | Ce fichier |

## Description

Application crm-ia faisant partie de la plateforme IAFactory.
Service backend/API.

## Quick Start

### Installation

```bash
pip install -r requirements.txt

# Backend (si applicable)
cd backend
pip install -r requirements.txt
```

### Developpement

```bash
uvicorn app.main:app --reload

# Backend
cd backend
uvicorn app.main:app --reload --port 8000
```

### Build

```bash
# No build (Python)
```

## Structure

```
crm-ia/
    crm_api.py
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
