# TODO EXHAUSTIF IAFactory - 11 janvier 2026

## FAIT (30%)
- Ports renumérotés
- Billing désactivé
- Structure éclatée
- Gateway Python basique (OpenAI, Anthropic, Groq, DeepSeek, Mistral)
- Système crédits in-memory

## CRITIQUE - A FAIRE MAINTENANT
- [ ] Ajouter 9 providers manquants (Gemini, Cohere, Together, OpenRouter, Perplexity, Replicate, etc.)
- [ ] Base de données PostgreSQL pour crédits
- [ ] Réactiver auth sur endpoints
- [ ] Tester chaque provider

## IMPORTANT - SEMAINE 1
- [ ] Remplacer providers directs dans academy/ai-tools/video
- [ ] Centraliser JWT (remplacer 4 implémentations)
- [ ] Webhook Chargily paiements
- [ ] Tests end-to-end

## MOYEN - SEMAINE 2
- [ ] Mutualiser PostgreSQL (72)
- [ ] Mutualiser Redis (62)
- [ ] Nettoyer 14 fichiers .env
- [ ] Rotation clés prod
- [ ] CLAUDE.md pour chaque dossier

## OPTIONNEL
- [ ] Monitoring
- [ ] CI/CD
- [ ] Tests auto
