# IAFactory CI/CD Pipeline Avancé

## Fonctionnalités du pipeline
- **Lint JS & CSS** : Vérifie la qualité du code JavaScript et CSS
- **Tests unitaires** : Exécute les tests automatisés (Jest)
- **Build** : Compile le projet (Next.js ou autre)
- **Audit CSS** : Vérifie l'absence de `.help-*` dans le code actif (isolation CSS)
- **Minification** : Minifie les assets pour la prod
- **Déploiement** : Déploiement automatisé (exemple : Vercel)
- **Archivage** : Archive les artefacts de build

## Scripts NPM disponibles
- `npm run lint:js` : Lint JavaScript/TypeScript
- `npm run lint:css` : Lint CSS
- `npm test` : Tests unitaires
- `npm run build` : Build du projet
- `npm run audit:css` : Audit d’isolation CSS (.iaf-*)
- `npm run minify` : Minification (adapter selon stack)
- `npm run deploy` : Déploiement (adapter selon infra)

## Audit CSS personnalisé
Le script `audit-css.js` vérifie qu’aucune classe `.help-*` n’est présente dans le code CSS actif (hors commentaires/docs). Le pipeline échoue si une occurrence est détectée.

## Intégration CI/CD (GitHub Actions)
Le workflow `.github/workflows/ci-cd.yml` automatise toutes les étapes ci-dessus à chaque push/pull request sur `main`.

## Configuration du déploiement
- Pour Vercel : ajouter le secret `VERCEL_TOKEN` dans les secrets GitHub
- Pour d’autres plateformes : adapter le script `deploy` dans `package.json`

## Personnalisation
- Adapter les chemins dans `audit-css.js` selon l’architecture réelle
- Adapter les étapes build/minify/deploy selon la stack réelle

---

*Dernière mise à jour : Janvier 2026*
