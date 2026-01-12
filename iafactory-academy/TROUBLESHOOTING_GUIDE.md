# TROUBLESHOOTING GUIDE (100+ solutions condensées)

Usage: cherche la catégorie, applique une des solutions rapides. Priorité: vérifier logs, reproduire, corriger le plus simple d’abord.

## Infrastructure & Deploy
- Deploy échoue: vérifier `.env`, ports déjà pris, `docker-compose logs`; relancer container fautif; `docker-compose down && up --build`.
- SSL ne marche pas: vérifier DNS A/AAAA; certbot logs; ouvrir 80/443; régénérer cert; tester `curl -I https://domaine`.
- DB connection errors: vérifier URL Postgres, user/pass; `alembic upgrade head`; test `psql` local; firewall/VPC.
- Services crash: `docker logs <service>`; manque de mémoire; healthcheck; fixer version Python/lib; redémarrer.
- Performance lente: activer gzip/nginx; ajouter cache Redis; profiler requêtes lentes; limiter N+1; augmenter ressources VPS.

## Marketing & Growth
- Pas de trafic: publier quotidien, réutiliser 30 posts du calendrier; lancer 1 campagne Google Search + 1 Meta; poster sur 3 communautés.
- CAC trop haut: tester 3 créas; resserrer ciblage; améliorer landing (preuves, FAQ, CTA clair); ajouter lead magnet.
- Conversion faible: réduire friction paiement; ajouter testimoniaux; garantir remboursement; offrir essai gratuit/mini cours.
- Ads ne marchent pas: couper ensembles <ROAS 2; augmenter budget sur gagnants; tester nouvelles accroches; vérifier pixels/UTM.

## Content & Courses
- Création trop lente: batcher scripts 1h; filmer en séries; utiliser `COURSE_SCRIPT_MODULE1.md`; externaliser montage.
- Low completion: raccourcir vidéos; ajouter quiz; envoyer emails de rappel; mettre des objectifs visibles.
- Pas d’engagement: CTA clair; demandes de commentaires; lives courts; rewards (certifs, shoutouts).

## Finance & Revenue
- Pas de ventes: page d’offre claire; bonus limité; urgence (fin de promo); upsell bundle; proposer call découverte.
- Churn élevé: séquence nurture; communauté; nouvelles leçons hebdo; support rapide; feedback loop.
- Paiements qui échouent: activer paiements locaux; tester Stripe keys; logs webhooks; mail d’alternative paiement.

## Motivation & Mindset
- Burnout: réduire scope; 1 tâche cruciale/jour; pause 24h; déléguer montage/ads.
- Impostor syndrome: montrer preuves (code, cours, démos); publier progrès; demander feedback restreint.
- Procrastination: règle 5 minutes; commit public quotidien; livrer brouillon imparfait; retirer distractions.

## Emergency Support (plan rapide)
- Discord/Slack communautés IA/indés
- Email experts/freelances (Fiverr/Upwork) pour micro-fixes
- Backup: `scripts/backup.sh` avant toute manip critique

## Check-list express avant d’escalader
- Logs lus? (backend/front/docker/nginx)
- Reproduit le bug? (navigateur privé, autre device)
- Variables d’env correctes? (.env vs prod)
- Derniers changements identifiés?
- Solution la plus simple testée?

## Résolution en 15 minutes (ordre conseillé)
1) Redémarrer le service concerné
2) Lire logs 200 lignes
3) Vérifier `.env` et secrets
4) Tester endpoint health
5) Tester DB connexion
6) Désactiver/vider cache si suspect
7) Réessayer déploiement

## Outils utiles
- `docker logs <name> --tail 200`
- `docker-compose ps`
- `curl -I https://...`
- `pytest` (backend)
- `npm run build` (frontend)
- `alembic upgrade head`

## Quand demander de l’aide
- >2h bloqué sur le même bug
- Incident prod (paiements down) > 15 minutes
- Perte de données: déclencher restauration depuis backup

Garde ce guide ouvert pendant le lancement. Commence par la solution la plus simple. 🚀
