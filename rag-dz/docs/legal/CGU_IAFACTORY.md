# CONDITIONS GÉNÉRALES D'UTILISATION (CGU)
## Plateforme IA Factory

**Version:** 1.0
**Date d'effet:** 22 Novembre 2024
**Société:** IA Factory SA, Genève, Suisse

---

## ARTICLE 1 - DÉFINITIONS

**1.1** "Plateforme" désigne l'ensemble des services, applications et interfaces mis à disposition par IA Factory, incluant:
- IAF Hub (interface de gestion)
- IAF Studio (éditeur de code assisté par IA)
- IAF Docs (gestion documentaire et RAG)
- API IA Factory

**1.2** "Utilisateur" désigne toute personne physique ou morale utilisant la Plateforme.

**1.3** "Données Utilisateur" désigne l'ensemble des données, documents, fichiers et contenus uploadés, générés ou traités par l'Utilisateur via la Plateforme.

**1.4** "Solution On-Premise" ou "Pocket" désigne le déploiement local de la Plateforme sur l'infrastructure propre de l'Utilisateur (SSD portable, serveur local).

**1.5** "Solution Cloud" désigne l'hébergement des services sur l'infrastructure gérée par IA Factory.

---

## ARTICLE 2 - ACCEPTATION DES CGU

**2.1** L'utilisation de la Plateforme implique l'acceptation pleine et entière des présentes CGU.

**2.2** IA Factory se réserve le droit de modifier les présentes CGU. L'Utilisateur sera informé de toute modification 30 jours avant son entrée en vigueur.

**2.3** La poursuite de l'utilisation de la Plateforme après modification vaut acceptation des nouvelles CGU.

---

## ARTICLE 3 - INSCRIPTION ET COMPTE UTILISATEUR

**3.1 Création de Compte**
L'accès à certaines fonctionnalités de la Plateforme nécessite la création d'un compte utilisateur. L'Utilisateur s'engage à fournir des informations exactes et à les maintenir à jour.

**3.2 Sécurité du Compte**
L'Utilisateur est seul responsable de la confidentialité de ses identifiants de connexion. Toute activité réalisée depuis son compte est réputée effectuée par lui.

**3.3 Suspension**
IA Factory se réserve le droit de suspendre ou supprimer tout compte en cas de violation des présentes CGU, sans préavis ni indemnité.

---

## ARTICLE 4 - SOUVERAINETÉ DES DONNÉES

### 4.1 Principe Fondamental

**IA Factory s'engage à respecter la souveraineté des données de ses Utilisateurs selon le principe suivant:**

| Type de Déploiement | Localisation des Données | Responsable du Traitement |
|---------------------|--------------------------|---------------------------|
| Cloud Suisse (CH) | Serveurs Infomaniak, Genève | IA Factory SA |
| Cloud Algérie (DZ) | Infrastructure locale DZ | IA Factory DZ |
| On-Premise (Pocket) | Infrastructure Utilisateur | **Utilisateur** |

### 4.2 Solution On-Premise (Pocket)

**4.2.1 Responsabilité de l'Utilisateur**

Dans le cadre d'un déploiement On-Premise (Solution Pocket sur SSD):

- **L'Utilisateur est seul responsable** de la sécurité, de la sauvegarde et de la confidentialité des Données Utilisateur stockées sur son infrastructure locale.

- **IA Factory décline toute responsabilité** en cas de:
  - Perte de données due à une défaillance matérielle
  - Vol ou destruction du support de stockage
  - Accès non autorisé aux données locales
  - Défaut de sauvegarde par l'Utilisateur
  - Catastrophe naturelle ou sinistre affectant l'infrastructure locale

**4.2.2 Obligations de l'Utilisateur**

L'Utilisateur s'engage à:
- Maintenir des sauvegardes régulières de ses données
- Sécuriser l'accès physique à son infrastructure
- Mettre à jour régulièrement les composants logiciels
- Respecter les recommandations de sécurité d'IA Factory

### 4.3 Solution Cloud

**4.3.1 Hébergement Suisse**

Les données hébergées sur l'infrastructure Cloud Suisse d'IA Factory sont:
- Stockées exclusivement sur des serveurs situés en Suisse (Infomaniak, Genève)
- Soumises au droit suisse et à la LPD
- Protégées par des mesures de sécurité conformes aux standards de l'industrie

**4.3.2 Aucun Transfert International**

IA Factory garantit qu'aucune Donnée Utilisateur hébergée sur l'infrastructure Cloud Suisse ne sera transférée vers des pays tiers sans le consentement explicite de l'Utilisateur.

### 4.4 Routage Intelligent

La Plateforme intègre un "Routeur de Souveraineté" permettant de:
- Sélectionner automatiquement l'infrastructure appropriée selon la localisation de l'Utilisateur
- Garantir que les requêtes API respectent les exigences réglementaires locales
- Afficher clairement la juridiction applicable à chaque session

---

## ARTICLE 5 - SYSTÈME WALLET ET CONSOMMATION

### 5.1 Fonctionnement du Wallet

**5.1.1** Le Wallet est un portefeuille virtuel crédité par l'activation de Clés de Recharge.

**5.1.2** Chaque requête API effectuée via la Plateforme entraîne un débit automatique du Wallet, calculé selon:
- Le Provider utilisé (Groq, OpenRouter, OpenAI, Anthropic, etc.)
- Le modèle IA sélectionné
- Le volume de tokens traités (entrée et sortie)
- Une marge commerciale de 30%

### 5.2 Transparence Tarifaire

**5.2.1** La grille tarifaire complète est disponible à tout moment via l'endpoint `/api/keys/pricing`.

**5.2.2** Exemple de tarification (par million de tokens):

| Provider | Modèle | Entrée | Sortie |
|----------|--------|--------|--------|
| Groq | llama-3.3-70b | $0.77 | $1.03 |
| OpenRouter | claude-3.5-sonnet | $3.90 | $19.50 |
| OpenAI | gpt-4o-mini | $0.20 | $0.78 |

*Tarifs incluant la marge de 30%, susceptibles de modification.*

### 5.3 Alertes et Notifications

**5.3.1** L'Utilisateur est notifié lorsque son solde atteint:
- 20% du crédit initial
- 10% du crédit initial
- 0% (épuisement)

**5.3.2** L'épuisement du crédit entraîne la suspension immédiate de l'accès aux services API payants.

---

## ARTICLE 6 - UTILISATION ACCEPTABLE

### 6.1 Usages Autorisés

La Plateforme est destinée à:
- Le développement et le déploiement d'applications d'IA
- La recherche et l'analyse de documents (RAG)
- La génération de contenu assistée par IA
- L'automatisation de tâches professionnelles

### 6.2 Usages Interdits

Il est strictement interdit d'utiliser la Plateforme pour:
- Générer du contenu illégal, diffamatoire ou haineux
- Contourner les mesures de sécurité ou de limitation
- Effectuer des attaques informatiques ou du scraping abusif
- Revendre l'accès à la Plateforme sans autorisation
- Stocker des données sensibles non chiffrées (données de santé, bancaires, etc.)
- Toute activité contraire à la législation suisse ou internationale

### 6.3 Contenu Généré par IA

**6.3.1** L'Utilisateur reconnaît que le contenu généré par les modèles d'IA peut contenir des erreurs ou des inexactitudes.

**6.3.2** L'Utilisateur est seul responsable de la vérification et de l'utilisation du contenu généré.

**6.3.3** IA Factory ne garantit pas l'exactitude, la complétude ou l'adéquation à un usage particulier du contenu généré.

---

## ARTICLE 7 - PROPRIÉTÉ INTELLECTUELLE

### 7.1 Droits d'IA Factory

La Plateforme, son code source, ses interfaces, sa documentation et ses marques sont la propriété exclusive d'IA Factory SA. Toute reproduction non autorisée est interdite.

### 7.2 Droits de l'Utilisateur

**7.2.1** L'Utilisateur conserve la pleine propriété de ses Données Utilisateur.

**7.2.2** Le contenu généré par l'IA à partir des données de l'Utilisateur appartient à l'Utilisateur.

**7.2.3** IA Factory n'utilise pas les Données Utilisateur pour entraîner des modèles d'IA sans consentement explicite.

---

## ARTICLE 8 - PROTECTION DES DONNÉES PERSONNELLES

### 8.1 Conformité Réglementaire

IA Factory traite les données personnelles en conformité avec:
- La Loi fédérale sur la Protection des Données (LPD) suisse
- Le Règlement Général sur la Protection des Données (RGPD) européen
- La loi algérienne n°18-07 relative à la protection des personnes physiques dans le traitement des données à caractère personnel

### 8.2 Données Collectées

Les données personnelles collectées sont:
- Données d'identification (nom, email)
- Données de facturation
- Données d'utilisation (logs, métriques)
- Données techniques (adresse IP, navigateur)

### 8.3 Droits des Utilisateurs

L'Utilisateur dispose des droits suivants:
- Droit d'accès à ses données
- Droit de rectification
- Droit à l'effacement ("droit à l'oubli")
- Droit à la portabilité
- Droit d'opposition

Pour exercer ces droits: privacy@iafactory.ch

### 8.4 Délégué à la Protection des Données

DPO: dpo@iafactory.ch

---

## ARTICLE 9 - LIMITATION DE RESPONSABILITÉ

### 9.1 Exclusions

IA Factory ne peut être tenue responsable:
- Des dommages indirects, consécutifs ou punitifs
- De la perte de données, de profits ou d'opportunités commerciales
- Des interruptions de service dues aux Providers tiers
- De l'utilisation faite par l'Utilisateur du contenu généré
- **Des données stockées sur l'infrastructure On-Premise de l'Utilisateur**

### 9.2 Plafond de Responsabilité

En tout état de cause, la responsabilité totale d'IA Factory est limitée au montant total payé par l'Utilisateur au cours des 12 derniers mois.

### 9.3 Force Majeure

IA Factory ne saurait être tenue responsable en cas de force majeure (catastrophe naturelle, guerre, pandémie, défaillance d'infrastructure nationale, etc.).

---

## ARTICLE 10 - RÉSILIATION

### 10.1 Résiliation par l'Utilisateur

L'Utilisateur peut résilier son compte à tout moment via l'interface de la Plateforme. Le crédit non consommé n'est pas remboursé.

### 10.2 Résiliation par IA Factory

IA Factory peut résilier le compte d'un Utilisateur en cas de:
- Violation des présentes CGU
- Activité frauduleuse ou illégale
- Non-paiement

### 10.3 Effets de la Résiliation

À la résiliation:
- L'accès à la Plateforme est immédiatement suspendu
- Les Données Utilisateur Cloud sont supprimées sous 30 jours
- Les Données Utilisateur On-Premise restent sous la responsabilité de l'Utilisateur

---

## ARTICLE 11 - DROIT APPLICABLE ET LITIGES

### 11.1 Droit Applicable

Les présentes CGU sont régies par le droit suisse, à l'exclusion de ses règles de conflit de lois.

### 11.2 Juridiction Compétente

Tout litige relatif à l'interprétation ou l'exécution des présentes CGU relève de la compétence exclusive des tribunaux du Canton de Genève, Suisse.

### 11.3 Médiation Préalable

Avant toute action judiciaire, les parties s'engagent à tenter une résolution amiable du litige par voie de médiation, pendant une durée minimale de 30 jours.

---

## ARTICLE 12 - DISPOSITIONS DIVERSES

### 12.1 Intégralité

Les présentes CGU, conjointement avec les CGV et la Politique de Confidentialité, constituent l'intégralité de l'accord entre l'Utilisateur et IA Factory.

### 12.2 Divisibilité

Si une disposition des présentes CGU est déclarée nulle ou inapplicable, les autres dispositions restent en vigueur.

### 12.3 Non-Renonciation

Le fait pour IA Factory de ne pas exercer un droit prévu aux présentes CGU ne constitue pas une renonciation à ce droit.

---

## ARTICLE 13 - CONTACT

Pour toute question relative aux présentes CGU:

**IA Factory SA**
Rue du Rhône XX
1204 Genève, Suisse

Email: legal@iafactory.ch
Support: support@iafactory.ch
DPO: dpo@iafactory.ch

---

*Document généré le 22 Novembre 2024*
*© 2024 IA Factory SA - Tous droits réservés*
