#  TODO RÉEL IAFactory - 11 janvier 2026, 15h05

## PHASE IMMÉDIATE (maintenant)

### 1. Gateway - Finaliser (3h)
- [ ] Tester 8 providers avec vraies clés
- [ ] Connecter PostgreSQL crédits (actuellement in-memory)
- [ ] Valider webhook Chargily
- [ ] Ajouter rate limiting
- [ ] Réactiver auth sur prod

### 2. Apps Core - Migrer vers gateway (4h)
- [ ] iafactory-academy : remplacer OpenAI/Anthropic directs
- [ ] iafactory-ai-tools : remplacer providers directs
- [ ] iafactory-video-platform : remplacer providers directs
- [ ] 10 apps core : tester + connecter gateway
- [ ] 15 agents : tester + connecter gateway
- [ ] 8 apps experimental : tester basique

### 3. Infra - Mutualiser (2h)
- [ ] 1 PostgreSQL partagé (pas 7)
- [ ] 1 Redis partagé (pas 6)
- [ ] Centraliser JWT (supprimer 4 locaux)

### 4. Sécurité (1h)
- [ ] Nettoyer 14 fichiers .env
- [ ] Rotation clés prod
- [ ] .gitignore partout

### 5. Docs/Config Claude (2h)
- [ ] CLAUDE.md : iafactory-gateway-python
- [ ] CLAUDE.md : iafactory-core-apps
- [ ] CLAUDE.md : iafactory-agents
- [ ] Slash-commands /plan-feature, /implement, /review
- [ ] README chaque dossier

### 6. Apps oubliées (3h)
- [ ] 11 apps rag-dz non catégorisées
- [ ] 5 verticales (can2025, pme-dz, etc.)
- [ ] onestschooled refactor

TOTAL RÉEL : ~15h de travail restant

## ORDRE EXÉCUTION

1. Connecter PostgreSQL gateway (maintenant)
2. Migrer academy vers gateway (maintenant)
3. Tests providers (maintenant)
4. Reste en sessions futures
