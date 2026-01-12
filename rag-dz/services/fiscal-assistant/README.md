# DZ-FiscalAssistant 🇩🇿💰

**Module 4 de IAFactory Algeria - Simulateur Fiscal Algérie**

## 📋 Description

DZ-FiscalAssistant est un simulateur fiscal pour l'Algérie qui permet d'estimer les impôts et cotisations sociales. Il utilise :

- **Moteur de calcul déterministe** : Règles fiscales configurables (YAML)
- **LLM (GROQ)** : Génération d'explications pédagogiques
- **RAG DZ** : Contexte documentaire (lois, circulaires DGI)

## ⚠️ Avertissement Important

**Ce module fournit des ESTIMATIONS indicatives uniquement.**

- Les calculs ne constituent PAS un conseil fiscal professionnel
- Les taux et règles peuvent évoluer
- Consultez toujours un expert-comptable ou la DGI pour les montants officiels

## 🚀 Fonctionnalités

### Impôts & Taxes supportés

| Code | Nom | Description |
|------|-----|-------------|
| IRG | Impôt sur le Revenu Global | Barème progressif (0% à 35%) |
| IFU | Impôt Forfaitaire Unique | Régime simplifié (5% à 12%) |
| TAP | Taxe sur l'Activité Professionnelle | 1% à 2% du CA |
| TVA | Taxe sur la Valeur Ajoutée | 9% (réduit) ou 19% (normal) |
| IBS | Impôt sur les Bénéfices des Sociétés | 19% à 26% |
| CNAS | Cotisations Sociales Salariés | 35% (employeur + salarié) |
| CASNOS | Cotisations Non-Salariés | 15% |

### Profils supportés

- 💻 **Freelance** : Travailleur indépendant, consultant
- 🏢 **Entreprise** : SARL, SPA, EURL
- 👔 **Salarié** : Employé
- 🛒 **Commerçant** : Activité commerciale
- ❓ **Autre** : Autre situation

## 🔧 Architecture

### Backend (Python/FastAPI)

```
dz-fiscal-assistant/
├── Dockerfile
├── README.md
└── backend/
    ├── main.py              # API FastAPI
    └── dz_tax_rules.yaml    # Règles fiscales configurables
```

#### Composants principaux

1. **TaxRulesEngine** : Moteur de calcul déterministe
   - `load_rules()` : Charge les règles depuis YAML
   - `compute_irg()` : Calcul IRG progressif
   - `compute_ifu()` : Calcul IFU forfaitaire
   - `compute_tap()` : Calcul TAP
   - `compute_tva()` : Estimation TVA
   - `compute_ibs()` : Calcul IBS
   - `compute_cnas()` : Calcul CNAS
   - `compute_casnos()` : Calcul CASNOS

2. **LLM Integration** : Explications pédagogiques
   - Le LLM ne fait PAS les calculs
   - Il génère uniquement les textes explicatifs

### Frontend (HTML/Tailwind)

```
apps/fiscal-assistant/
└── index.html    # Interface utilisateur
```

## 📡 API Endpoints

### POST `/api/dz-fiscal/simulate`

Simulation fiscale complète.

**Request:**
```json
{
  "profile_type": "freelance",
  "activity_sector": "Développement logiciel",
  "regime": "IFU",
  "revenue_period": "annuel",
  "revenue_amount": 3000000,
  "charges_amount": 500000,
  "salaries_amount": 0,
  "social_covered": true,
  "detail_level": "détaillé"
}
```

**Response:**
```json
{
  "summary": "Estimation fiscale pour profil freelance...",
  "currency": "DZD",
  "totals": {
    "estimated_tax_total": 150000,
    "estimated_social_total": 450000,
    "estimated_net_income": 1900000
  },
  "breakdown": [
    {
      "label": "IFU",
      "amount": 150000,
      "basis": "Taux 5% sur CA de 3,000,000 DZD",
      "notes": ["TVA incluse dans l'IFU", "TAP incluse dans l'IFU"]
    },
    {
      "label": "CASNOS",
      "amount": 450000,
      "basis": "Assiette: 3,000,000 DZD",
      "notes": ["Taux CASNOS: 15%"]
    }
  ],
  "explanations": [...],
  "references": [...],
  "disclaimer": "⚠️ Cette simulation est fournie à titre indicatif...",
  "followup_questions": [...]
}
```

### GET `/api/dz-fiscal/profiles`

Liste des profils et régimes disponibles.

### GET `/api/dz-fiscal/rules`

Informations sur les règles fiscales chargées.

## ⚙️ Configuration des Règles Fiscales

Les règles sont définies dans `dz_tax_rules.yaml` :

```yaml
version: "2024-2025"
last_updated: "2024-01-01"
currency: "DZD"

irg:
  enabled: true
  tranches:
    - min: 0
      max: 240000
      rate: 0
    - min: 240001
      max: 480000
      rate: 0.23
    # ...

ifu:
  enabled: true
  seuil_ca_max: 30000000
  tranches:
    - min: 0
      max: 10000000
      rate: 0.05
    # ...
```

### Modification des règles

1. Éditer `dz_tax_rules.yaml`
2. Redémarrer le container ou appeler `/reload-rules` (si implémenté)
3. Les nouveaux taux s'appliquent immédiatement

## 🐳 Déploiement Docker

### Build
```bash
docker build -t iaf-fiscal-assistant .
```

### Run
```bash
docker run -d \
  --name iaf-fiscal-assistant-prod \
  --network iaf-prod-network \
  -p 8199:8199 \
  -e GROQ_API_KEY=your_key \
  -e RAG_API_URL=http://iaf-dz-connectors-prod:8195 \
  iaf-fiscal-assistant
```

## 🌐 URLs

| Service | Port | Route |
|---------|------|-------|
| Backend API | 8199 | `/api/dz-fiscal/` |
| Frontend | 8200 | `/fiscal/` |

## 📝 Scénarios d'exemple

### Scénario 1 : Freelance développeur

```json
{
  "profile_type": "freelance",
  "activity_sector": "Développement logiciel",
  "regime": "IFU",
  "revenue_period": "annuel",
  "revenue_amount": 5000000,
  "social_covered": true
}
```

**Résultat estimé :**
- IFU : 250,000 DZD (5%)
- CASNOS : 750,000 DZD (15%)
- Net estimé : ~4,000,000 DZD

### Scénario 2 : Petite SARL

```json
{
  "profile_type": "entreprise",
  "activity_sector": "Commerce",
  "regime": "réel",
  "revenue_period": "annuel",
  "revenue_amount": 20000000,
  "charges_amount": 5000000,
  "salaries_amount": 3000000,
  "social_covered": true
}
```

**Résultat estimé :**
- IBS : ~3,120,000 DZD (26% sur bénéfice)
- TAP : 400,000 DZD (2%)
- CNAS : 1,050,000 DZD (35%)
- Net estimé : variable

### Scénario 3 : Salarié

```json
{
  "profile_type": "salarié",
  "revenue_period": "mensuel",
  "revenue_amount": 80000,
  "social_covered": true
}
```

**Résultat estimé :**
- IRG : Selon barème progressif avec abattement 10%
- CNAS : Retenue salariale 9%

## 📚 Références

- [Direction Générale des Impôts (DGI)](https://www.mfdgi.gov.dz)
- Code des Impôts Directs et Taxes Assimilées
- Loi de Finances 2024

## 📝 Licence

Module de IAFactory Algeria - Usage interne
