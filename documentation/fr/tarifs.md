# Tarifs IAFactory

IAFactory propose des formules simples pour démarrer avec l’IA multi‑modèles en Algérie, ainsi qu’une facturation à l’usage pour l’API (tokens et images).
Les tarifs détaillés sont indiqués ci‑dessous et peuvent évoluer ; en cas de modification, la page Tarifs fait foi.

## 1. Formules IAFactory (abonnement)

Tous les abonnés IAFactory disposent de crédits inclus pour utiliser le chat, les assistants et l’API.

| Formule  | Crédits mensuels inclus | Description rapide                  |
|----------|-------------------------|-------------------------------------|
| Starter  | 500 DZD                 | Pour tester IAFactory sur un petit volume. |
| Standard | 1 000 DZD               | Pour un usage régulier dans une petite équipe. |
| Expert   | 2 500 DZD               | Pour un usage intensif ou plusieurs projets. |

Vous pouvez également passer sur une facturation à l’usage (“pay as you go”) directement depuis vos paramètres API IAFactory.

## 2. Modèles & Tarifs API

L’API IAFactory donne accès à plusieurs modèles texte et image, facturés au volume de tokens ou par image.

### 2.1 Modèles texte

Les prix sont indiqués en DZD par million de tokens (input et output).

| Modèle           | Type  | Prix (input / 1M tokens) | Prix (output / 1M tokens) |
|------------------|-------|--------------------------|---------------------------|
| gpt-4.1          | Texte | 250 DZD                  | 1 000 DZD                 |
| gpt-5.2          | Texte | 500 DZD                  | 1 500 DZD                 |
| claude-sonnet-4.5| Texte | 750 DZD                  | 3 750 DZD                 |
| gemini-3-pro     | Texte | 312 DZD                  | 1 250 DZD                 |
| mistral-medium   | Texte | 125 DZD                  | 375 DZD                   |
| deepseek-v3      | Texte | 70 DZD                   | 140 DZD                   |

Ces tarifs s’appliquent aux appels API et, selon la configuration, à certaines fonctionnalités avancées de la plateforme.

### 2.2 Modèles image

Les modèles image IAFactory sont facturés à la génération.

| Modèle                  | Type   | Prix |
|-------------------------|--------|------|
| flux-schnell            | Image  | 8 DZD / image  |
| stable-diffusion-3.5    | Image  | 16 DZD / image |

## 3. Comprendre la facturation

### 3.1 Tokens (texte)

Un token correspond à une petite unité de texte (mots, morceaux de mots, symboles).
Le coût final d’un appel texte dépend à la fois des tokens d’entrée (prompt) et des tokens de sortie (réponse).

Exemple de calcul (simplifié) :
- 500 tokens en entrée + 1 500 tokens en sortie = 2 000 tokens au total (0,002 M tokens).
- Coût = (prix input × 0,0005) + (prix output × 0,0015), selon le modèle choisi.

### 3.2 Images

Pour les modèles image, chaque génération est facturée à l’unité (par image), selon le modèle utilisé.
Le coût est donc simplement : nombre d’images générées × prix par image.

## 4. FAQ Tarifs

### Les prix incluent‑ils la TVA ?

Les prix sont exprimés en DZD ; l’application de la TVA dépend de votre statut et des règles en vigueur en Algérie. (à préciser dans vos CGU / mentions légales)

### Que se passe‑t‑il si je dépasse mes crédits mensuels ?

Au‑delà des crédits inclus dans votre formule, la consommation peut basculer en mode “pay as you go” selon les tarifs modèles ci‑dessus. (à préciser selon votre implémentation réelle)

### Puis‑je changer de formule à tout moment ?

Le changement de formule (upgrade/downgrade) est possible depuis votre espace client, sous réserve des conditions d’engagement précisées dans les CGU. (à préciser)

### Les tarifs peuvent‑ils évoluer ?

Oui. IAFactory peut ajuster les tarifs en fonction des coûts des fournisseurs et des évolutions du marché, avec un préavis conformément aux Conditions d’Utilisation.

### Où trouver plus de détails techniques sur les modèles ?

La page **Documentation API → Models & Pricing** décrit les modèles, les endpoints et les paramètres techniques à utiliser dans vos intégrations.
