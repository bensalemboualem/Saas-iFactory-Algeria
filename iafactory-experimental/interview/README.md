# interview

> Application interview - IAFactory SaaS Platform

## Status

| Aspect | Valeur |
|--------|--------|
| **Production** | [DEV] En developpement |
| **Stack** | Next.js 14 |
| **Tests** | A implementer |
| **Documentation** | Ce fichier |

## Description

Application interview faisant partie de la plateforme IAFactory.
Application frontend.

## Quick Start

### Installation

```bash
npm install

```

### Developpement

```bash
npm run dev

```

### Build

```bash
npm run build
```

## Structure

```
interview/
    app/
    public/
    src/
    next-env.d.ts, next.config.js, postcss.config.js, tailwind.config.js
```

## Configuration

Copier `.env.example` vers `.env` et configurer les variables:

```env
# API
API_URL=http://localhost:8000

# Voir .env.example pour la liste complete
```

## API Endpoints

Non applicable (frontend only)

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
