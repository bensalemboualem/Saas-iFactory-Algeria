# Service Level Agreement (SLA)

**IAFACTORY - Accord de Niveau de Service**

*Dernière mise à jour : 19 janvier 2026*

---

## 1. Introduction

Ce document définit les niveaux de service garantis par IAFACTORY pour ses différents plans d'abonnement.

---

## 2. Disponibilité du service

### 2.1 Engagements par plan

| Plan | Disponibilité garantie | Maintenance planifiée |
|------|------------------------|----------------------|
| Free | Best effort | Non notifiée |
| Pro | 99.5% | 24h à l'avance |
| Pro+ | 99.9% | 48h à l'avance |
| Enterprise | 99.95% | 72h à l'avance |

### 2.2 Calcul de la disponibilité

```
Disponibilité (%) = ((Temps total - Temps d'indisponibilité) / Temps total) × 100
```

**Exclusions du calcul :**
- Maintenance planifiée et notifiée
- Cas de force majeure
- Problèmes liés aux fournisseurs tiers (OpenAI, Anthropic, etc.)
- Problèmes réseau côté utilisateur

---

## 3. Performance

### 3.1 Temps de réponse API

| Métrique | Free | Pro | Pro+ | Enterprise |
|----------|------|-----|------|------------|
| Latence médiane | < 2s | < 1s | < 500ms | < 200ms |
| Latence P95 | < 5s | < 3s | < 2s | < 1s |
| Rate limit | 10 req/min | 60 req/min | 300 req/min | Custom |

### 3.2 Temps de traitement IA

Les temps de réponse IA dépendent des modèles utilisés et ne sont pas garantis par ce SLA. Temps indicatifs :

| Modèle | Temps typique (1K tokens) |
|--------|--------------------------|
| GPT-3.5 | 1-3 secondes |
| GPT-4 | 5-15 secondes |
| Claude 3 Sonnet | 3-8 secondes |
| Claude 3 Opus | 10-30 secondes |

---

## 4. Support technique

### 4.1 Canaux de support

| Plan | Email | Chat | Téléphone | Slack/Teams dédié |
|------|-------|------|-----------|-------------------|
| Free | ✓ | - | - | - |
| Pro | ✓ | - | - | - |
| Pro+ | ✓ | ✓ | - | - |
| Enterprise | ✓ | ✓ | ✓ | ✓ |

### 4.2 Temps de réponse (premier contact)

| Priorité | Description | Free | Pro | Pro+ | Enterprise |
|----------|-------------|------|-----|------|------------|
| **P1 - Critique** | Service totalement indisponible | 5 jours | 4h | 1h | 15 min |
| **P2 - Majeur** | Fonctionnalité majeure impactée | 5 jours | 8h | 4h | 1h |
| **P3 - Modéré** | Fonctionnalité mineure impactée | 5 jours | 24h | 8h | 4h |
| **P4 - Faible** | Question, amélioration | 5 jours | 48h | 24h | 8h |

### 4.3 Définition des priorités

**P1 - Critique :**
- La plateforme est complètement inaccessible
- Perte de données utilisateur
- Faille de sécurité critique

**P2 - Majeur :**
- Fonctionnalité principale non fonctionnelle (chat, génération)
- Performance sévèrement dégradée (> 10x le temps normal)
- Authentification défaillante

**P3 - Modéré :**
- Fonctionnalité secondaire non fonctionnelle
- Bug affectant l'expérience utilisateur
- Lenteur modérée

**P4 - Faible :**
- Demande d'information
- Suggestion d'amélioration
- Bug cosmétique

---

## 5. Maintenance

### 5.1 Maintenance planifiée

- **Fenêtre standard** : Dimanche 02:00-06:00 UTC
- **Notification** : Selon le plan (voir section 2.1)
- **Communication** : Email + bannière in-app

### 5.2 Maintenance d'urgence

Pour les correctifs de sécurité critiques, une maintenance d'urgence peut être effectuée avec un préavis minimal. Les utilisateurs Enterprise seront contactés directement.

---

## 6. Sauvegarde et récupération

### 6.1 Politique de sauvegarde

| Élément | Fréquence | Rétention |
|---------|-----------|-----------|
| Base de données | Toutes les 6h | 30 jours |
| Fichiers utilisateur | Quotidienne | 30 jours |
| Logs | Continue | 90 jours |

### 6.2 Objectifs de récupération

| Métrique | Objectif |
|----------|----------|
| RPO (Recovery Point Objective) | 6 heures |
| RTO (Recovery Time Objective) | 4 heures |

---

## 7. Sécurité

### 7.1 Engagements

- Chiffrement TLS 1.3 pour toutes les communications
- Chiffrement AES-256 des données au repos
- Audits de sécurité annuels (Pro+ et Enterprise)
- Conformité RGPD et loi algérienne 18-07

### 7.2 Notification des incidents

| Sévérité | Délai de notification |
|----------|----------------------|
| Critique (brèche données) | 24 heures |
| Majeur | 48 heures |
| Mineur | Rapport mensuel |

---

## 8. Crédits de service (Compensation)

### 8.1 Éligibilité

Les crédits de service s'appliquent uniquement aux plans payants (Pro, Pro+, Enterprise) en cas de non-respect des engagements de disponibilité.

### 8.2 Calcul des crédits

| Disponibilité mensuelle | Crédit |
|------------------------|--------|
| 99.0% - 99.5% | 10% de la facture mensuelle |
| 95.0% - 99.0% | 25% de la facture mensuelle |
| 90.0% - 95.0% | 50% de la facture mensuelle |
| < 90.0% | 100% de la facture mensuelle |

### 8.3 Procédure de réclamation

1. Soumettre une demande dans les 30 jours suivant l'incident
2. Email à sla@iafactory.ai avec :
   - Dates et heures des incidents
   - Description de l'impact
   - Captures d'écran si disponibles
3. Réponse sous 10 jours ouvrés
4. Crédit appliqué sur la prochaine facture

### 8.4 Limitations

- Crédit maximum : 100% de la facture mensuelle
- Non cumulable avec d'autres remises
- Non convertible en espèces
- Non applicable si l'utilisateur est en infraction avec les CGU

---

## 9. Exclusions

Ce SLA ne s'applique pas dans les cas suivants :

1. **Force majeure** : catastrophes naturelles, guerres, pandémies
2. **Fournisseurs tiers** : indisponibilité d'OpenAI, Anthropic, Google
3. **Actions utilisateur** : abus, violation des CGU
4. **Réseau** : problèmes ISP côté utilisateur
5. **Alpha/Beta** : fonctionnalités en préversion

---

## 10. Modifications

IAFACTORY se réserve le droit de modifier ce SLA avec un préavis de 30 jours. Les modifications défavorables ne s'appliquent pas aux abonnements Enterprise en cours.

---

## 11. Contact

**Support SLA :**
- Email : sla@iafactory.ai
- Portail : status.iafactory.ai

**Escalade (Enterprise) :**
- Account Manager dédié
- Hotline directe

---

*Ce SLA est effectif à compter du 19 janvier 2026.*
