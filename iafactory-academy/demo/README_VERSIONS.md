# IAFactory Academy - Système de Versions ON/OFF

## Vue d'ensemble

Ce système permet de gérer différentes versions de la démo pour différents prospects/partenaires.

```
demo/
├── config.py                    # Configuration centrale ON/OFF
├── minister_demo_generic.py     # Version générique (ON par défaut)
├── minister_demo_bbc.py         # Version BBC School (OFF par défaut)
├── minister_demo_full.py        # Version legacy (archivée)
├── README_VERSIONS.md           # Cette documentation
└── locales/                     # Traductions FR/AR/EN
    ├── fr.json
    ├── ar.json
    └── en.json
```

---

## Versions Disponibles

| Version | Fichier | Status | Usage |
|---------|---------|--------|-------|
| **Generic** | `minister_demo_generic.py` | ✅ ON | Pour tout prospect |
| **BBC School** | `minister_demo_bbc.py` | ❌ OFF | Deal BBC confirmé |
| **Nouvelle Horizon** | Template dans config | ❌ OFF | Nouvelle école |

---

## Commandes de Lancement

### Version Générique (Default)
```bash
python -m streamlit run demo/minister_demo_generic.py --server.port 8502
```

### Version BBC School
```bash
python -m streamlit run demo/minister_demo_bbc.py --server.port 8503
```

---

## Configuration (config.py)

### Structure des Versions

```python
VERSIONS = {
    "generic": {
        "enabled": True,           # ON par défaut
        "display_name": "IAFactory-School",
        "students": 1600,
        "demo_mode": True,         # Permet config dynamique
        "partner_type": "prospect",
    },
    "bbc": {
        "enabled": False,          # OFF par défaut
        "display_name": "BBC School",
        "students": 1600,
        "demo_mode": False,        # Config fixe
        "partner_type": "strategic",
    },
}
```

### Activer une Version

#### Méthode 1: Modifier config.py
```python
# Dans config.py, modifiez:
VERSIONS["generic"]["enabled"] = False
VERSIONS["bbc"]["enabled"] = True
```

#### Méthode 2: Via Python
```python
from config import enable_version
enable_version("bbc")  # Active BBC, désactive les autres
```

---

## Pricing Automatique

Le système calcule automatiquement les prix en fonction du nombre d'élèves:

| Élèves | Prix/mois/élève | Tier |
|--------|-----------------|------|
| < 500 | 700 DA | Standard |
| 500-999 | 650 DA | Premium |
| 1000-1999 | 600 DA | Enterprise |
| 2000+ | 550 DA | National |

### Fonctions de Calcul

```python
from config import calculate_pricing, calculate_iafactory_investment, calculate_roi

# Calculer le pricing pour 1600 élèves
pricing = calculate_pricing(1600)
# → {'price_per_student_month': 600, 'annual_total': 9_600_000, ...}

# Calculer l'investissement IAFactory
investment = calculate_iafactory_investment(1600)
# → {'total': 4_800_000, 'total_millions': 4.8, ...}

# Calculer le ROI sur 3 ans
roi = calculate_roi(1600)
# → {'pessimistic': {...}, 'realistic': {...}, 'optimistic': {...}}
```

---

## Différences entre Versions

### Version Générique
- **Couleur primaire**: Bleu (#3B82F6)
- **Mode démo**: ✅ Activé (slider pour ajuster le nombre d'élèves)
- **Sidebar**: Configuration dynamique visible
- **Branding**: IAFactory-School neutre

### Version BBC
- **Couleur primaire**: Vert Algérie (#006233)
- **Mode démo**: ❌ Désactivé (valeurs fixes)
- **Sidebar**: Statut partenariat stratégique
- **Branding**: BBC School × IAFactory
- **Badge**: "Partenaire Stratégique"
- **Note spéciale**: "100% offert par IAFactory"

---

## Mode Démo (Generic Only)

La version générique inclut un slider dans la sidebar pour:
- Ajuster le nombre d'élèves (100 - 5000)
- Voir les calculs dynamiques en temps réel
- Démontrer la flexibilité du pricing

```
⚙️ Configuration Démo
[Mode Démo]

Nombre d'élèves: [====1600====]

Prix/élève: 600 DA/mois
Tier: Enterprise
Invest. IAF: 4.8M DA
```

---

## Ajouter une Nouvelle École

1. **Ajouter la config dans config.py:**
```python
VERSIONS["nouvelle_ecole"] = {
    "enabled": False,
    "name": "nouvelle_ecole",
    "display_name": "Nouvelle École Academy",
    "display_name_ar": "أكاديمية المدرسة الجديدة",
    "tagline": "Excellence avec l'IA",
    "logo_emoji": "🏫",
    "primary_color": "#8B5CF6",
    "students": 800,
    "teachers": 15,
    "demo_mode": False,
    "partner_type": "client",
}
```

2. **Créer le fichier démo:**
```bash
cp demo/minister_demo_generic.py demo/minister_demo_nouvelle_ecole.py
# Modifier pour importer la bonne config
```

3. **Lancer:**
```bash
python -m streamlit run demo/minister_demo_nouvelle_ecole.py
```

---

## API de Configuration

### Fonctions Disponibles

| Fonction | Description |
|----------|-------------|
| `get_active_config()` | Retourne la config active avec calculs |
| `get_config_by_name(name)` | Retourne une config spécifique |
| `enable_version(name)` | Active une version, désactive les autres |
| `list_versions()` | Liste toutes les versions avec statut |
| `calculate_pricing(students)` | Calcule le pricing |
| `calculate_iafactory_investment(students)` | Calcule l'investissement |
| `calculate_roi(students, years)` | Calcule le ROI 3 scénarios |

### Exemple d'Usage

```python
from config import get_active_config, list_versions

# Voir les versions disponibles
print(list_versions())
# → {'generic': True, 'bbc': False, 'nouvelle_horizon': False}

# Obtenir la config active
config = get_active_config()
print(f"Active: {config['display_name']}")
print(f"ROI: {config['metrics']['roi_range']}")
print(f"Investment: {config['metrics']['investment_total']}")
```

---

## Checklist Avant Présentation

### Pour un Prospect Générique
- [ ] Lancer `minister_demo_generic.py`
- [ ] Vérifier que le mode démo est visible
- [ ] Tester le slider d'élèves
- [ ] Vérifier les 3 langues (FR/AR/EN)
- [ ] Tester Dark/Light mode

### Pour BBC School (Deal Confirmé)
- [ ] Modifier `config.py` pour activer BBC
- [ ] Lancer `minister_demo_bbc.py`
- [ ] Vérifier le branding vert Algérie
- [ ] Vérifier "Partenaire Stratégique" visible
- [ ] Vérifier "0 DA" pour BBC School
- [ ] Tester les 3 langues

---

## Troubleshooting

### La config ne se met pas à jour
```bash
# Redémarrer Streamlit
Ctrl+C
python -m streamlit run demo/minister_demo_generic.py
```

### Erreur d'import config
```bash
# Vérifier que vous êtes dans le bon répertoire
cd d:\iafactory-academy
python -m streamlit run demo/minister_demo_generic.py
```

### Les calculs semblent faux
```python
# Tester manuellement
python demo/config.py
# Affiche toutes les valeurs calculées
```

---

## Fichiers Archivés

| Fichier | Statut | Note |
|---------|--------|------|
| `minister_demo_full.py` | Archivé | Version legacy avant ON/OFF |

---

*Dernière mise à jour: Décembre 2025*
