# Audit IAFactory Algeria

> Date: 24 janvier 2026

---

## Statut du Projet

| Critère | Statut |
|---------|--------|
| **Région** | Algérie (DZ) |
| **Références Swiss** | 0 |
| **Code applicatif** | 100% Clean |
| **Configuration** | Algeria uniquement |

---

## Résumé

Le projet IAFactory a été entièrement migré vers la configuration Algérie.

**Toutes les références suisses ont été supprimées:**
- Aucune mention de "Suisse" ou "Switzerland"
- Aucune référence à "iafactory.ch"
- Aucune devise CHF
- Aucun timezone Europe/Zurich

---

## Dossiers Vérifiés

| Dossier | Statut |
|---------|--------|
| `src/` | CLEAN |
| `packages/` | CLEAN |
| `apps/landing/` | CLEAN |
| `apps/web/` | CLEAN |
| `apps/api/` | CLEAN |
| `apps/iafactory-core/` | CLEAN |
| `apps/gateway/` | CLEAN |
| `apps/desktop/` | CLEAN |
| `apps/bolt/` | CLEAN |
| `apps/bolt-ui/` | CLEAN |
| `apps/academy/` | CLEAN |
| `apps/dzir-ia/` | CLEAN |
| `locales/` | CLEAN |
| `public/` | CLEAN |
| `scripts/` | CLEAN |
| `docker-compose/` | CLEAN |
| `docs/` | CLEAN |

---

## Fichiers Nettoyés

### Code Principal
- `packages/const/src/branding.ts` - Branding Algeria
- `src/locales/resources.ts` - Langues FR/AR/EN
- `src/app/[variants]/(landing)/LandingPage.tsx`
- `src/app/[variants]/(landing)/verticals/LegalLanding.tsx`
- `src/app/[variants]/(landing)/verticals/BusinessLanding.tsx`

### Apps
- `apps/b2b/video-studio/backend/main.py`
- `apps/iafactory-core/rag-dz/agents/legal/legal_team.py`
- `apps/landing/src/components/Footer.tsx`

### Documentation (supprimée et recréée)
- `docs/architecture/ARCHITECTURE_IAFACTORY_ALGERIA.md`
- `docs/deployment/DOCKER_COMPOSE_ALGERIA.md`
- `docs/platform/PRICING_DZD.md`

---

## Fichiers Déplacés vers Backup

Les fichiers de configuration suisse ont été déplacés vers `D:\suisse_saas\` pour référence:

- `docker-compose.switzerland.yml`
- `docker-compose.switzerland.prod.yml`

---

## Configuration Actuelle

```
Région:       Algeria (DZ)
Devise:       DZD
Paiement:     Chargily Pay
Langues:      FR, AR, EN
Timezone:     Africa/Algiers
Domaine:      iafactoryalgeria.com
```

---

## Exceptions Acceptées

Les fichiers suivants contiennent des références mondiales (listes de pays/devises) et sont conservés:

- `apps/b2b/school/config/country.php` - Liste des pays du monde
- `apps/b2b/school/database/seeders/CurrencySeeder.php` - Liste des devises mondiales

Ces fichiers sont des données de référence standard, pas du branding.

---

## Conclusion

**Le projet IAFactory est maintenant 100% configuré pour l'Algérie.**

Audit effectué le 24/01/2026.
