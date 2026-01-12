# IAFactory - SaaS Gateway IA Algérie

## Vision
Gateway multi-providers IA + paiement monnaie locale
Marché : 2M étudiants + PME + professions libérales Algérie

## Architecture CORE
iafactory-gateway-python (port 3001) :
- 9 providers IA
- PostgreSQL crédits
- Facturation automatique
- Webhook Chargily

RÈGLE : Tout passe par gateway, jamais appels directs providers

## Projets
- gateway-python : CORE
- academy : LMS (8200/3100)
- ai-tools : Outils (8220/3110)
- video-platform : Vidéos (8240/3120)
- core-apps : 10 apps principales
- agents : 15 agents

## Fichiers critiques
NE JAMAIS modifier sans plan :
- .env (clés API)
- migrations/
- services/chargily/
- core/auth.py

Voir .claude/commands/ pour workflows
