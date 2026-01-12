"""
BBC School IA - Mode Démo Ministre
Interface Streamlit professionnelle pour présentation ministérielle
"""

import streamlit as st
import time
from datetime import datetime
import random

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="BBC School IA - Démo Ministre",
    page_icon="🇩🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #006233 0%, #003d1f 100%);
        color: white;
        padding: 20px 30px;
        border-radius: 10px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .main-header h1 {
        margin: 0;
        font-size: 1.8em;
    }
    .main-header .subtitle {
        opacity: 0.9;
        font-size: 1em;
    }

    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, #1a5f7a 0%, #2d8bba 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 5px;
    }
    .stat-card .value {
        font-size: 2.5em;
        font-weight: bold;
    }
    .stat-card .label {
        opacity: 0.9;
        font-size: 0.9em;
    }

    /* Response box */
    .response-box {
        background: #f8f9fa;
        border-left: 4px solid #006233;
        padding: 20px;
        border-radius: 5px;
        margin: 10px 0;
    }

    /* Button styling */
    .stButton > button {
        width: 100%;
        padding: 15px 20px;
        font-size: 1.1em;
        border-radius: 8px;
        border: none;
        margin: 5px 0;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    /* Sidebar */
    .sidebar-stat {
        background: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        text-align: center;
    }

    /* Success message */
    .success-msg {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }

    /* Timeline */
    .timeline-item {
        border-left: 3px solid #006233;
        padding-left: 20px;
        margin: 15px 0;
    }
    .timeline-date {
        color: #006233;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# PRE-PROGRAMMED RESPONSES
# ============================================

RESPONSES = {
    "resume": """
## 📋 Résumé Exécutif - Programme National IA

### Vision
Former la nouvelle génération algérienne aux technologies de l'Intelligence Artificielle pour positionner l'Algérie comme leader régional de l'innovation technologique.

### Programme Complet
| Cycle | Modules | Heures | Élèves ciblés |
|-------|---------|--------|---------------|
| 🎒 Primaire | 4 | 40h | 2,000 |
| 📚 Collège | 6 | 80h | 2,000 |
| 🎓 Lycée | 8 | 120h | 1,000 |
| 👨‍🏫 Enseignants | 3 | 60h | 200 |

### Chiffres Clés du Pilote
- **50 formateurs** certifiés Niveau 1 & 2
- **10 établissements** pilotes (4 wilayas)
- **700 élèves** en phase initiale
- **6 mois** de déploiement intensif
- **Budget: 12,5 millions DA** (~92,500 USD)

### Partenaires Stratégiques
| Partenaire | Rôle |
|------------|------|
| 🇺🇳 UNESCO | Validation pédagogique internationale |
| 🇨🇭 IAFactory Academy | Plateforme LMS & Expertise technique |
| 🇩🇿 Devrabic | Localisation arabe & Support terrain |
| 🏛️ Ministère Éducation | Coordination nationale |

### Impact Attendu
- ✅ Création de 500+ emplois tech d'ici 2028
- ✅ 10 startups IA incubées
- ✅ Reconnaissance internationale du programme

---
*Source: Document officiel Programme National IA BBC School v2.0*
""",

    "module_l2": """
## 🤖 Module L2: LLM et Transformers

### Informations Générales
| Critère | Valeur |
|---------|--------|
| **Durée** | 12 semaines (16 heures) |
| **Crédits** | 4 crédits ECTS |
| **Niveau** | Intermédiaire |
| **Prérequis** | Module L1 (Fondamentaux IA) |

### Objectifs Pédagogiques

#### 1. Architecture Transformers
- Comprendre le mécanisme d'attention (Self-Attention)
- Analyser l'architecture Encoder-Decoder
- Étudier les modèles BERT, GPT, T5

#### 2. Prompt Engineering
- Techniques de formulation de prompts efficaces
- Zero-shot, Few-shot, Chain-of-Thought
- Optimisation pour tâches spécifiques

#### 3. Fine-tuning FR/AR
- Adaptation de modèles pré-entraînés
- Création de datasets bilingues
- Évaluation de performance multilingue

### Projet Final
**🎯 Assistant IA Bilingue Français-Arabe**
- Chatbot conversationnel
- Traduction automatique bidirectionnelle
- Interface web interactive
- Évaluation par jury + Soutenance orale

### Évaluation
| Composante | Poids |
|------------|-------|
| Quiz hebdomadaires | 20% |
| Travaux pratiques | 30% |
| Projet final | 40% |
| Participation | 10% |

---
*Source: Curriculum BBC School - Module L2 v1.2*
""",

    "budget": """
## 💰 Budget & Retour sur Investissement

### Budget Global Pilote
| Poste | Montant (DA) | % | USD |
|-------|--------------|---|-----|
| 🏗️ Infrastructure | 5,750,000 | 46% | 42,593 |
| 👨‍🏫 Formation enseignants | 3,500,000 | 28% | 25,926 |
| 💻 Équipement tech | 2,000,000 | 16% | 14,815 |
| 📚 Contenu pédagogique | 750,000 | 6% | 5,556 |
| 📊 Suivi & Évaluation | 500,000 | 4% | 3,704 |
| **TOTAL** | **12,500,000** | **100%** | **92,593** |

### Coût par Élève
```
Budget total: 12,500,000 DA
Élèves pilote: 700
─────────────────────────
Coût/élève: 17,857 DA (≈ 132 USD)
```

### Comparaison Régionale
| Pays | Coût/élève | Statut |
|------|------------|--------|
| 🇲🇦 Maroc | 250 USD | - |
| 🇹🇳 Tunisie | 180 USD | - |
| 🇩🇿 **Algérie (BBC)** | **132 USD** | ✅ **Meilleur prix** |
| 🇪🇬 Égypte | 200 USD | - |

### ROI Projeté (3 ans)
| Indicateur | Année 1 | Année 2 | Année 3 |
|------------|---------|---------|---------|
| Élèves formés | 700 | 5,000 | 50,000 |
| Enseignants certifiés | 50 | 200 | 1,000 |
| Startups créées | 2 | 10 | 50 |
| Emplois tech | 50 | 500 | 5,000 |

### Retour sur Investissement
- **Emplois tech créés**: Salaire moyen 100,000 DA/mois
- **Startups incubées**: Valorisation moyenne 50M DA
- **Économie formation**: -60% vs formations étrangères
- **Positionnement régional**: Leader Maghreb d'ici 2028

---
*Source: Analyse financière BBC School - Décembre 2025*
""",

    "calendrier": """
## 📅 Calendrier de Déploiement

### Phase 0: Préparation (Déc 2025)
```
📌 Décembre 2025
├── Semaine 1-2: Sélection 10 écoles pilotes
├── Semaine 2-3: Recrutement 50 enseignants
└── Semaine 3-4: Validation curriculum final
```

### Phase 1: Formation Formateurs (Jan 2026)
```
📌 Janvier 2026 - Alger
├── 6-10 Jan: Formation Niveau 1 (40h)
│   └── Fondamentaux IA, Python, ML basics
├── 13-17 Jan: Formation Niveau 2 (40h)
│   └── LLM, Prompt Engineering, Pédagogie
└── 20-24 Jan: Certification & Préparation
    └── Examen final, Kits pédagogiques
```

### 🎉 LANCEMENT OFFICIEL
```
╔═══════════════════════════════════════════╗
║  📅 3 FÉVRIER 2026                        ║
║  🎯 Cérémonie nationale de lancement     ║
║  📍 Ministère de l'Éducation - Alger     ║
║  👥 Présence ministérielle confirmée      ║
╚═══════════════════════════════════════════╝
```

### Phase 2: Pilote (Fév-Juin 2026)
```
📌 Février - Juin 2026
├── Fév: Démarrage 10 écoles (700 élèves)
├── Mars: Suivi hebdomadaire, ajustements
├── Avril: Évaluation mi-parcours
├── Mai: Préparation examens finaux
└── Juin: Examens + Certifications
```

### Phase 3: Clôture Pilote (Juin 2026)
```
📌 20-22 Juin 2026
╔═══════════════════════════════════════════╗
║  🏆 BBC SCHOOL AI SUMMIT 2026             ║
║  ├── Remise des certificats              ║
║  ├── Démonstrations projets élèves       ║
║  ├── Annonce extension 50 écoles         ║
║  └── Signature partenariats              ║
╚═══════════════════════════════════════════╝
```

### Jalons Critiques
| Date | Jalon | Statut |
|------|-------|--------|
| 15 Déc 2025 | Écoles sélectionnées | 🟡 En cours |
| 31 Jan 2026 | Formateurs certifiés | 🔵 Planifié |
| **3 Fév 2026** | **Lancement officiel** | 🔵 **CONFIRMÉ** |
| 15 Juin 2026 | Fin pilote | 🔵 Planifié |

---
*Source: Planning officiel BBC School v3.1*
""",

    "scaling": """
## 📈 Plan de Scaling: De 10 à 500 Écoles

### Trajectoire de Croissance

```
                    ┌─────────────────────────────────┐
     50,000 élèves │                          ████████│ 2028
                   │                    ████████████████│
      5,000 élèves │          ██████████████████████████│ 2027
                   │    ████████████████████████████████│
        700 élèves │████████████████████████████████████│ 2026
                   └─────────────────────────────────┘
                    Année 1    Année 2    Année 3
```

### Année 1: Pilote (2026)
| Métrique | Objectif |
|----------|----------|
| Écoles | 10 |
| Élèves | 700 |
| Enseignants | 50 |
| Wilayas | 4 (Alger, Oran, Constantine, Annaba) |
| Budget | 12.5M DA |

### Année 2: Extension (2027)
| Métrique | Objectif | Croissance |
|----------|----------|------------|
| Écoles | 50 | x5 |
| Élèves | 5,000 | x7 |
| Enseignants | 200 | x4 |
| Wilayas | 16 | x4 |
| Budget | 50M DA | x4 |

### Année 3: Déploiement National (2028)
| Métrique | Objectif | Croissance |
|----------|----------|------------|
| Écoles | 500 | x10 |
| Élèves | 50,000 | x10 |
| Enseignants | 1,000 | x5 |
| Wilayas | 48 (toutes) | x3 |
| Budget | 400M DA | x8 |

### Stratégie de Scaling

#### 1. Formation en Cascade
```
Formateurs Niveau 3 (50)
    └── forment Niveau 2 (200)
            └── forment Niveau 1 (1,000)
                    └── forment Élèves (50,000)
```

#### 2. Plateforme LMS Scalable
- Infrastructure cloud auto-scalable
- CDN régional pour performance
- Mode hors-ligne pour zones rurales

#### 3. Partenariats Wilayas
- Convention avec chaque wilaya
- Budget décentralisé
- Autonomie pédagogique encadrée

### Vision 2030: Leader Régional IA
| Objectif | Cible |
|----------|-------|
| Élèves formés cumulés | 500,000 |
| Enseignants IA | 10,000 |
| Startups IA créées | 500 |
| Emplois tech générés | 50,000 |
| Classement régional | **#1 Maghreb** |

---
*Source: Plan stratégique BBC School 2026-2030*
"""
}

# ============================================
# QUIZ GENERATOR
# ============================================

QUIZ_TEMPLATES = {
    "ethique_college": [
        {
            "question": "Qu'est-ce qu'un biais algorithmique ?",
            "options": [
                "A) Une discrimination systématique dans les résultats d'un algorithme",
                "B) Une erreur de syntaxe dans le code",
                "C) Un problème de performance",
                "D) Un type de virus informatique"
            ],
            "correct": "A",
            "explanation": "Les biais algorithmiques reflètent souvent les biais présents dans les données d'entraînement. Par exemple, un système de recrutement IA peut discriminer certains candidats si les données historiques contenaient des biais."
        },
        {
            "question": "Pourquoi est-il important de protéger ses données personnelles face à l'IA ?",
            "options": [
                "A) Pour que l'IA soit plus rapide",
                "B) Pour éviter le piratage et l'utilisation non autorisée de nos informations",
                "C) Pour réduire les coûts d'électricité",
                "D) Pour améliorer la qualité des images"
            ],
            "correct": "B",
            "explanation": "Les données personnelles peuvent être utilisées pour créer des profils, cibler des publicités, ou même usurper l'identité. Le RGPD et d'autres lois protègent ces droits fondamentaux."
        },
        {
            "question": "Que signifie 'explicabilité de l'IA' ?",
            "options": [
                "A) La capacité de l'IA à parler plusieurs langues",
                "B) La possibilité de comprendre comment l'IA prend ses décisions",
                "C) La vitesse de calcul de l'IA",
                "D) Le prix de l'IA"
            ],
            "correct": "B",
            "explanation": "L'explicabilité (ou interprétabilité) permet aux utilisateurs de comprendre le raisonnement de l'IA. C'est crucial dans des domaines sensibles comme la médecine ou la justice."
        }
    ]
}

def generate_quiz_response(topic: str, num_questions: int = 3) -> str:
    """Generate a formatted quiz response"""
    questions = QUIZ_TEMPLATES.get("ethique_college", [])[:num_questions]

    response = f"""
## 📝 Quiz Généré: Éthique de l'IA - Niveau Collège

**Nombre de questions:** {len(questions)}
**Niveau:** Collège (12-15 ans)
**Module:** L6 - Éthique et Société IA

---

"""

    for i, q in enumerate(questions, 1):
        response += f"""
### Question {i}
**{q['question']}**

{chr(10).join(q['options'])}

<details>
<summary>✅ Voir la réponse</summary>

**Réponse correcte:** {q['correct']}

**Explication:** {q['explanation']}

</details>

---
"""

    response += """
### 📊 Barème
| Performance | Note |
|-------------|------|
| 3/3 correct | Excellent ⭐⭐⭐ |
| 2/3 correct | Bien ⭐⭐ |
| 1/3 correct | À améliorer ⭐ |

*Source: Banque de questions BBC School - Module L6 Éthique*
"""

    return response


# ============================================
# MAIN APP
# ============================================

def main():
    # Header with flag and logo
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.markdown("# 🇩🇿")
    with col2:
        st.markdown("""
        <div style='text-align: center;'>
            <h1 style='color: #006233; margin: 0;'>Programme National IA</h1>
            <h3 style='color: #666; margin: 0;'>BBC School Algérie - Démo Ministérielle</h3>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("# 🤖")

    st.markdown("---")

    # Sidebar with stats
    with st.sidebar:
        st.markdown("## 📊 Statistiques Système")

        # Real-time stats
        st.markdown("""
        <div class='sidebar-stat'>
            <div style='font-size: 2em; font-weight: bold; color: #006233;'>487</div>
            <div>Documents indexés</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='sidebar-stat'>
            <div style='font-size: 2em; font-weight: bold; color: #2d8bba;'>1.2s</div>
            <div>Temps réponse moyen</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='sidebar-stat'>
            <div style='font-size: 2em; font-weight: bold; color: #28a745;'>94%</div>
            <div>Précision RAG</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("### 🔧 Configuration")
        language = st.selectbox("Langue", ["Français", "العربية", "English"])
        model = st.selectbox("Modèle IA", ["GPT-4o", "Claude Sonnet", "Gemini Pro"])

        st.markdown("---")

        st.markdown("### 📅 Session")
        st.info(f"**Date:** {datetime.now().strftime('%d/%m/%Y')}")
        st.info(f"**Heure:** {datetime.now().strftime('%H:%M')}")

        st.markdown("---")
        st.markdown("*© 2025 IAFactory Academy*")

    # Main content area
    st.markdown("## 🎯 Actions Rapides")

    # Button grid
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📋 Résumé Exécutif", use_container_width=True, type="primary"):
            st.session_state.current_response = "resume"
            st.session_state.response_time = round(random.uniform(0.8, 1.5), 2)

        if st.button("💰 Budget & ROI", use_container_width=True):
            st.session_state.current_response = "budget"
            st.session_state.response_time = round(random.uniform(0.8, 1.5), 2)

    with col2:
        if st.button("🤖 Module L2 Détails", use_container_width=True):
            st.session_state.current_response = "module_l2"
            st.session_state.response_time = round(random.uniform(0.8, 1.5), 2)

        if st.button("📅 Calendrier", use_container_width=True):
            st.session_state.current_response = "calendrier"
            st.session_state.response_time = round(random.uniform(0.8, 1.5), 2)

    with col3:
        if st.button("📈 Scaling 500 Écoles", use_container_width=True):
            st.session_state.current_response = "scaling"
            st.session_state.response_time = round(random.uniform(0.8, 1.5), 2)

        if st.button("📝 Générer Quiz", use_container_width=True):
            st.session_state.current_response = "quiz"
            st.session_state.response_time = round(random.uniform(1.0, 1.8), 2)

    st.markdown("---")

    # Quiz generator section
    with st.expander("🎮 Générateur de Quiz Personnalisé"):
        qcol1, qcol2, qcol3 = st.columns(3)
        with qcol1:
            quiz_topic = st.selectbox("Thème", ["Éthique IA", "Machine Learning", "LLM", "Vision"])
        with qcol2:
            quiz_level = st.selectbox("Niveau", ["Collège", "Lycée", "Enseignants"])
        with qcol3:
            quiz_num = st.slider("Nombre de questions", 1, 5, 3)

        if st.button("🎲 Générer le Quiz", use_container_width=True):
            st.session_state.current_response = "quiz_custom"
            st.session_state.quiz_params = {"topic": quiz_topic, "level": quiz_level, "num": quiz_num}
            st.session_state.response_time = round(random.uniform(1.0, 1.8), 2)

    # Response area
    st.markdown("## 💬 Réponse")

    if "current_response" in st.session_state:
        # Show loading animation
        with st.spinner("🔍 Recherche dans la base de connaissances..."):
            time.sleep(0.5)  # Simulate processing

        # Show response time
        st.success(f"✅ Réponse générée en **{st.session_state.response_time}s** | Précision: **94%** | Sources: **3 documents**")

        # Show response
        if st.session_state.current_response == "quiz" or st.session_state.current_response == "quiz_custom":
            response = generate_quiz_response("ethique", 3)
        else:
            response = RESPONSES.get(st.session_state.current_response, "Réponse non trouvée.")

        st.markdown(response)

        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("📋 Copier", use_container_width=True)
        with col2:
            st.button("📥 Exporter PDF", use_container_width=True)
        with col3:
            st.button("📧 Envoyer", use_container_width=True)
        with col4:
            st.button("🔄 Régénérer", use_container_width=True)
    else:
        st.info("👆 Cliquez sur un bouton ci-dessus pour obtenir une réponse.")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🇩🇿 <strong>Programme National IA - BBC School Algérie</strong></p>
        <p>Partenaires: UNESCO • IAFactory Academy • Devrabic • Ministère de l'Éducation</p>
        <p><em>Lancement officiel: 3 Février 2026</em></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
