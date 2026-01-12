# 🇩🇿 BBC School IA - Mode Démo Ministre

Interface de démonstration professionnelle pour la présentation ministérielle du Programme National IA.

## 🚀 Lancement Rapide

### Windows
```bash
cd demo
run_demo.bat
```

### Linux/Mac
```bash
cd demo
chmod +x run_demo.sh
./run_demo.sh
```

### Manuel
```bash
pip install streamlit pandas plotly
streamlit run minister_demo_full.py
```

L'interface s'ouvre sur **http://localhost:8501**

---

## 📋 Fonctionnalités

### 6 Boutons Préprogrammés

| Bouton | Contenu |
|--------|---------|
| 📋 Résumé Exécutif | Programme complet, chiffres clés, partenaires |
| 🤖 Module L2 | Détails LLM & Transformers |
| 💰 Budget & ROI | Répartition, coût/élève, comparaison régionale |
| 📅 Calendrier | Timeline complète, jalons critiques |
| 📈 Scaling 500 | Plan de croissance 2026-2028 |
| 📝 Quiz Éthique | Générateur de quiz dynamique |

### Support Multilingue

- 🇫🇷 **Français** - Interface principale
- 🇩🇿 **Arabe** - كم عدد الوحدات؟ متى يبدأ؟ الميزانية؟
- 🇬🇧 **English** - Coming soon

### Chat Intelligent

Posez des questions en langage naturel :
- "Quel est le budget total ?"
- "كم عدد الوحدات في البرنامج؟"
- "Génère 3 questions éthique IA collège"

---

## 📊 Statistiques Affichées

| Métrique | Valeur |
|----------|--------|
| Documents indexés | 487 |
| Temps réponse | 1.2s |
| Précision RAG | 94% |
| Langues | 3 |

---

## 🎯 Données Programme

### Chiffres Clés
- **50** formateurs certifiés
- **10** écoles pilotes
- **700** élèves phase 1
- **12.5M DA** budget total
- **3 Février 2026** lancement

### Modules Lycée (8)
| ID | Module | Heures |
|----|--------|--------|
| L1 | Fondamentaux IA | 12 |
| L2 | LLM & Transformers | 16 |
| L3 | Vision par Ordinateur | 14 |
| L4 | NLP Avancé | 16 |
| L5 | IA Générative | 14 |
| L6 | Éthique IA | 10 |
| L7 | Projet Intégrateur | 20 |
| L8 | IA & Carrières | 8 |

---

## 🛠️ Fichiers

| Fichier | Description |
|---------|-------------|
| `minister_demo.py` | Version simple |
| `minister_demo_full.py` | Version complète avec chat |
| `requirements.txt` | Dépendances Python |
| `run_demo.bat` | Lanceur Windows |
| `run_demo.sh` | Lanceur Linux/Mac |

---

## ✅ Checklist Pré-Démo

- [ ] Connexion internet stable
- [ ] Navigateur Chrome/Firefox
- [ ] Résolution 1920x1080 minimum
- [ ] Mode plein écran (F11)
- [ ] Tester tous les boutons
- [ ] Préparer questions arabes

---

## 🎨 Personnalisation

### Changer les couleurs
Modifier le CSS dans `minister_demo_full.py` :
```python
# Couleurs Algérie
primary_color = "#006233"  # Vert
accent_color = "#D21034"   # Rouge
```

### Ajouter des réponses
Ajouter dans le dictionnaire `RESPONSES` :
```python
RESPONSES["ma_reponse"] = """
## Mon titre
Contenu markdown...
"""
```

---

## 📞 Support

**IAFactory Academy**
- Email: contact@iafactory.ch
- Web: https://iafactory.ch

---

*© 2025 IAFactory Academy - Programme National IA BBC School Algérie*
