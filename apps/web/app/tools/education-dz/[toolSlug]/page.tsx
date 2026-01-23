'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { ArrowLeft, Sparkles, Loader2, Copy, Check, GraduationCap, BookOpen, ClipboardList, FileText, Languages, Compass } from 'lucide-react';
import { educationDzTools } from '@/lib/tools-data';

// Matieres du systeme educatif algerien
const MATIERES_BAC = [
  'Mathematiques', 'Physique', 'Sciences naturelles', 'Philosophie',
  'Histoire-Geographie', 'Francais', 'Anglais', 'Arabe',
  'Gestion', 'Economie', 'Comptabilite', 'Informatique'
];

const MATIERES_BEM = [
  'Mathematiques', 'Physique', 'Sciences naturelles',
  'Arabe', 'Francais', 'Anglais', 'Histoire-Geographie',
  'Education civique', 'Education islamique'
];

const MATIERES_5EME = [
  'Arabe', 'Francais', 'Mathematiques',
  'Education islamique', 'Education civique', 'Sciences'
];

const FILIERES_BAC = [
  'Sciences experimentales', 'Mathematiques', 'Technique mathematique',
  'Gestion et economie', 'Lettres et philosophie', 'Langues etrangeres'
];

// Configurations des formulaires pour chaque outil Education DZ
const toolFormConfigs: Record<string, { fields: any[], promptTemplate: string }> = {

  'revision-bac-algerie': {
    fields: [
      { name: 'filiere', type: 'select', label: 'Filiere', required: true, options: FILIERES_BAC },
      { name: 'matiere', type: 'select', label: 'Matiere', required: true, options: MATIERES_BAC },
      { name: 'chapitre', type: 'text', label: 'Chapitre ou theme', required: true, placeholder: 'Ex: Les suites numeriques, La Guerre d\'Algerie...' },
      { name: 'niveau', type: 'select', label: 'Niveau de revision', required: true, options: [
        'Debutant - Je decouvre', 'Intermediaire - Je revise', 'Avance - Je perfectionne'
      ]},
      { name: 'objectif', type: 'select', label: 'Objectif', options: [
        'Comprendre le cours', 'Preparer un controle', 'Revisions Bac blanc', 'Revisions Bac final'
      ]},
    ],
    promptTemplate: `Tu es un professeur expert du systeme educatif algerien, specialiste de la preparation au Baccalaureat.

FILIERE : {{filiere}}
MATIERE : {{matiere}}
CHAPITRE : {{chapitre}}
NIVEAU : {{niveau}}
{{#if objectif}}OBJECTIF : {{objectif}}{{/if}}

## Fiche de Revision - Bac Algerie

### 1. Resume du chapitre
[Resume structure des points essentiels]

### 2. Notions cles a retenir
| Notion | Definition | Exemple |
|--------|------------|---------|
| ... | ... | ... |

### 3. Formules / Dates / Citations importantes
[Selon la matiere]

### 4. Methodologie
- Comment aborder ce type de sujet au Bac
- Pieges a eviter
- Conseils pour maximiser les points

### 5. Exercice type Bac
[Un exercice repressentatif avec correction detaillee]

### 6. QCM de verification (5 questions)
1. [Question] - A) ... B) ... C) ... D) ...
[Reponses a la fin]

### 7. Pour aller plus loin
- Points de programme connexes
- Sujets des annees precedentes a consulter

### Reponses QCM
1. [Lettre] - Explication
...

Adapte au programme officiel algerien et au format d'examen du Baccalaureat.`
  },

  'preparation-bem-algerie': {
    fields: [
      { name: 'matiere', type: 'select', label: 'Matiere', required: true, options: MATIERES_BEM },
      { name: 'chapitre', type: 'text', label: 'Chapitre ou theme', required: true, placeholder: 'Ex: Les equations, Le present...' },
      { name: 'difficulte', type: 'select', label: 'Niveau', required: true, options: [
        'Facile', 'Moyen', 'Difficile'
      ]},
      { name: 'type_revision', type: 'select', label: 'Type de revision', options: [
        'Cours resume', 'Exercices corriges', 'Sujet type BEM', 'Tout'
      ]},
    ],
    promptTemplate: `Tu es un professeur specialise dans la preparation au BEM (Brevet d'Enseignement Moyen) en Algerie.

MATIERE : {{matiere}}
CHAPITRE : {{chapitre}}
NIVEAU : {{difficulte}}
TYPE : {{type_revision}}

## Preparation BEM - {{matiere}}

### 1. Points essentiels du cours
[Resume adapte au niveau 4eme annee moyenne]

### 2. Vocabulaire / Definitions
- **Terme 1** : Definition simple
- **Terme 2** : Definition simple
...

### 3. Methode a suivre
[Etapes claires pour resoudre ce type de probleme/exercice]

### 4. Exercices progressifs

#### Exercice 1 (Facile)
[Enonce]
**Correction :**
[Solution detaillee]

#### Exercice 2 (Moyen)
[Enonce]
**Correction :**
[Solution detaillee]

#### Exercice 3 (Difficile - Niveau BEM)
[Enonce]
**Correction :**
[Solution detaillee]

### 5. Conseils pour le jour J
- Gestion du temps
- Presentation de la copie
- Erreurs frequentes a eviter

Programme officiel algerien - Niveau 4AM`
  },

  'preparation-5eme-annee': {
    fields: [
      { name: 'matiere', type: 'select', label: 'Matiere', required: true, options: MATIERES_5EME },
      { name: 'theme', type: 'text', label: 'Theme ou lecon', required: true, placeholder: 'Ex: La phrase nominale, Les operations...' },
      { name: 'format', type: 'select', label: 'Format souhaite', options: [
        'Lecon illustree', 'Exercices avec correction', 'Dictee preparee', 'Tout'
      ]},
    ],
    promptTemplate: `Tu es un instituteur specialise dans la preparation a l'examen de 5eme annee primaire en Algerie.

MATIERE : {{matiere}}
THEME : {{theme}}
FORMAT : {{format}}

## Preparation Examen 5eme Annee - {{matiere}}

### 1. La lecon en bref
[Explication simple et claire, adaptee aux enfants de 10-11 ans]

### 2. Ce qu'il faut retenir
[Points cles en bullet points simples]

### 3. Exemples
[3-5 exemples concrets et faciles a comprendre]

### 4. Exercices d'entrainement

#### Exercice 1
[Consigne claire]

**Correction :**
[Solution]

#### Exercice 2
[Consigne claire]

**Correction :**
[Solution]

#### Exercice 3
[Consigne claire]

**Correction :**
[Solution]

### 5. Petit test
[5 questions courtes pour verifier la comprehension]

### 6. Astuce pour bien reussir
[Conseil pratique adapte aux enfants]

Conforme au programme algerien de 5eme annee primaire.`
  },

  'generateur-qcm-algerie': {
    fields: [
      { name: 'niveau', type: 'select', label: 'Niveau scolaire', required: true, options: [
        '5eme annee primaire', '4eme annee moyenne (BEM)', 'Bac - Sciences', 'Bac - Lettres', 'Bac - Gestion'
      ]},
      { name: 'matiere', type: 'select', label: 'Matiere', required: true, options: [
        'Mathematiques', 'Physique', 'Sciences naturelles', 'Arabe', 'Francais', 'Anglais',
        'Histoire', 'Geographie', 'Philosophie', 'Education islamique', 'Gestion', 'Economie'
      ]},
      { name: 'chapitre', type: 'text', label: 'Chapitre ou theme', required: true, placeholder: 'Precisez le chapitre...' },
      { name: 'nombre_questions', type: 'select', label: 'Nombre de questions', options: ['10', '15', '20', '30'] },
      { name: 'difficulte', type: 'select', label: 'Difficulte', options: ['Facile', 'Moyen', 'Difficile', 'Mixte'] },
    ],
    promptTemplate: `Tu es un enseignant algerien expert en creation de QCM pour les examens.

NIVEAU : {{niveau}}
MATIERE : {{matiere}}
CHAPITRE : {{chapitre}}
NOMBRE : {{nombre_questions}} questions
DIFFICULTE : {{difficulte}}

## QCM - {{matiere}} ({{niveau}})
### Theme : {{chapitre}}

---

**Question 1** [{{difficulte}}]
[Enonce de la question]

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

---

[Repeter pour le nombre de questions demande]

---

## CORRIGE

| Question | Reponse | Explication |
|----------|---------|-------------|
| 1 | [Lettre] | [Justification courte] |
| 2 | [Lettre] | [Justification courte] |
...

## Bareme suggere
- Chaque bonne reponse : 1 point
- Total : {{nombre_questions}} points
- Note sur 20 : (Points obtenus x 20) / {{nombre_questions}}

Conforme au programme officiel algerien.`
  },

  'fiches-cours-algerie': {
    fields: [
      { name: 'niveau', type: 'select', label: 'Niveau', required: true, options: [
        'Primaire', 'Moyen', 'Secondaire'
      ]},
      { name: 'classe', type: 'text', label: 'Classe', required: true, placeholder: 'Ex: 3AS, 4AM, 5AP...' },
      { name: 'matiere', type: 'select', label: 'Matiere', required: true, options: [
        'Mathematiques', 'Physique', 'Sciences', 'Arabe', 'Francais', 'Anglais',
        'Histoire', 'Geographie', 'Philosophie', 'Education islamique'
      ]},
      { name: 'chapitre', type: 'text', label: 'Titre du chapitre', required: true, placeholder: 'Titre exact du chapitre...' },
      { name: 'format', type: 'select', label: 'Format de fiche', options: [
        'Fiche resume', 'Fiche memoire (mind map)', 'Fiche formules', 'Fiche complete'
      ]},
    ],
    promptTemplate: `Tu es un enseignant algerien expert en creation de fiches de revision.

NIVEAU : {{niveau}}
CLASSE : {{classe}}
MATIERE : {{matiere}}
CHAPITRE : {{chapitre}}
FORMAT : {{format}}

## Fiche de Cours - {{matiere}}
### {{chapitre}}
**Classe : {{classe}} | Programme algerien**

---

### I. L'essentiel a retenir

[Points cles du chapitre en format structure]

### II. Definitions

| Terme | Definition |
|-------|------------|
| ... | ... |

### III. Formules / Regles / Dates
[Selon la matiere - presente de facon visuelle]

### IV. Schema / Mind Map
[Description d'un schema conceptuel]

### V. Exemples types
**Exemple 1 :**
[Enonce + Solution]

**Exemple 2 :**
[Enonce + Solution]

### VI. Erreurs a eviter
- Erreur 1 : ...
- Erreur 2 : ...

### VII. Liens avec d'autres chapitres
[Connexions avec le programme]

---
Fiche conforme au programme officiel algerien - {{classe}}`
  },

  'exercices-corriges-algerie': {
    fields: [
      { name: 'niveau', type: 'select', label: 'Niveau', required: true, options: [
        '5eme primaire', 'BEM', 'Bac'
      ]},
      { name: 'matiere', type: 'select', label: 'Matiere', required: true, options: [
        'Mathematiques', 'Physique', 'Sciences', 'Arabe', 'Francais', 'Anglais'
      ]},
      { name: 'chapitre', type: 'text', label: 'Chapitre', required: true, placeholder: 'Theme des exercices...' },
      { name: 'type_exercice', type: 'select', label: 'Type d\'exercice', options: [
        'Application directe', 'Exercice de synthese', 'Probleme', 'Sujet d\'examen'
      ]},
      { name: 'nombre', type: 'select', label: 'Nombre d\'exercices', options: ['3', '5', '10'] },
    ],
    promptTemplate: `Tu es un enseignant algerien specialise dans la creation d'exercices corriges.

NIVEAU : {{niveau}}
MATIERE : {{matiere}}
CHAPITRE : {{chapitre}}
TYPE : {{type_exercice}}
NOMBRE : {{nombre}}

## Exercices Corriges - {{matiere}}
### {{chapitre}} | Niveau {{niveau}}

---

### Exercice 1 [{{type_exercice}}]

**Enonce :**
[Enonce complet et clair]

**Correction detaillee :**

[Solution etape par etape avec explications]

**Points de methode :**
- [Ce qu'il faut retenir]

---

### Exercice 2 [{{type_exercice}}]
[Meme structure]

---

[Continuer jusqu'a {{nombre}} exercices]

---

## Recapitulatif des competences travaillees
- Competence 1 : ...
- Competence 2 : ...

## Conseils pour progresser
[Recommandations personnalisees]

Programme algerien - {{niveau}}`
  },

  'aide-dissertation-algerie': {
    fields: [
      { name: 'matiere', type: 'select', label: 'Matiere', required: true, options: [
        'Philosophie', 'Francais', 'Arabe', 'Histoire'
      ]},
      { name: 'sujet', type: 'textarea', label: 'Sujet de dissertation', required: true, placeholder: 'Copiez le sujet complet...', rows: 3 },
      { name: 'type', type: 'select', label: 'Type de dissertation', options: [
        'Dissertation dialectique', 'Dissertation analytique', 'Commentaire de texte', 'Essai'
      ]},
      { name: 'niveau_aide', type: 'select', label: 'Type d\'aide', options: [
        'Plan detaille seulement', 'Introduction + Plan', 'Dissertation complete'
      ]},
    ],
    promptTemplate: `Tu es un professeur de {{matiere}} specialise dans la methodologie de dissertation au Baccalaureat algerien.

MATIERE : {{matiere}}
SUJET : {{sujet}}
TYPE : {{type}}
AIDE DEMANDEE : {{niveau_aide}}

## Aide a la Dissertation - {{matiere}}

### Analyse du sujet

**Termes cles a definir :**
- Terme 1 : [Definition]
- Terme 2 : [Definition]

**Problematique :**
[La question centrale que pose le sujet]

**Type de sujet :** {{type}}

---

### Introduction
[Introduction complete : accroche + definition des termes + problematique + annonce du plan]

---

### Plan detaille

#### I. [Titre de la premiere partie]
A. [Argument 1]
   - Idee
   - Exemple/Reference

B. [Argument 2]
   - Idee
   - Exemple/Reference

[Transition]

#### II. [Titre de la deuxieme partie]
[Meme structure]

[Transition]

#### III. [Titre de la troisieme partie - synthese]
[Meme structure]

---

### Conclusion
[Bilan + Ouverture]

---

### References utiles
- Auteurs/Penseurs a citer
- Exemples historiques
- Citations appropriees

Methodologie conforme aux attentes du Bac algerien.`
  },

  'traducteur-academique-dz': {
    fields: [
      { name: 'direction', type: 'select', label: 'Direction de traduction', required: true, options: [
        'Francais vers Arabe', 'Arabe vers Francais', 'Francais vers Anglais', 'Anglais vers Francais'
      ]},
      { name: 'type_contenu', type: 'select', label: 'Type de contenu', required: true, options: [
        'Cours/Lecon', 'Exercice', 'Sujet d\'examen', 'Memoire/These', 'Document administratif scolaire'
      ]},
      { name: 'matiere', type: 'select', label: 'Matiere (optionnel)', options: [
        'General', 'Mathematiques', 'Sciences', 'Litterature', 'Histoire-Geo', 'Droit'
      ]},
      { name: 'texte', type: 'textarea', label: 'Texte a traduire', required: true, placeholder: 'Collez votre texte ici...', rows: 6 },
    ],
    promptTemplate: `Tu es un traducteur academique professionnel specialise dans le contexte educatif algerien.

DIRECTION : {{direction}}
TYPE DE CONTENU : {{type_contenu}}
MATIERE : {{matiere}}

TEXTE SOURCE :
{{texte}}

---

## Traduction Academique

### Traduction principale
[Traduction fidele et adaptee au contexte academique algerien]

### Notes de traduction
- [Termes techniques traduits avec leur equivalent]
- [Nuances importantes]

### Glossaire bilingue
| Terme source | Traduction | Note |
|--------------|------------|------|
| ... | ... | ... |

### Version alternative (si pertinent)
[Traduction avec formulation differente]

---

Traduction adaptee au systeme educatif algerien.`
  },

  'orientation-universitaire-dz': {
    fields: [
      { name: 'filiere_bac', type: 'select', label: 'Votre filiere au Bac', required: true, options: FILIERES_BAC },
      { name: 'moyenne', type: 'number', label: 'Moyenne estimee/obtenue au Bac', placeholder: 'Ex: 14.5' },
      { name: 'interets', type: 'text', label: 'Vos centres d\'interet', required: true, placeholder: 'Ex: informatique, medecine, commerce...' },
      { name: 'wilaya', type: 'text', label: 'Wilaya preferee pour etudes', placeholder: 'Ex: Alger, Oran, Constantine...' },
      { name: 'question', type: 'textarea', label: 'Question specifique (optionnel)', placeholder: 'Posez votre question...', rows: 2 },
    ],
    promptTemplate: `Tu es un conseiller d'orientation specialise dans le systeme universitaire algerien.

FILIERE BAC : {{filiere_bac}}
MOYENNE : {{moyenne}}
INTERETS : {{interets}}
WILAYA PREFEREE : {{wilaya}}
{{#if question}}QUESTION : {{question}}{{/if}}

## Guide d'Orientation Universitaire - Algerie

### 1. Analyse de votre profil
[Analyse basee sur la filiere et la moyenne]

### 2. Filieres recommandees

| Filiere | Moyenne requise | Debouches | Universites |
|---------|-----------------|-----------|-------------|
| ... | ... | ... | ... |

### 3. Top 5 des formations adaptees

#### 1. [Nom de la formation]
- **Type :** Licence / Master / Ecole
- **Duree :** X ans
- **Moyenne d'acces :** X
- **Universites :** [Liste]
- **Debouches :** [Metiers]

[Repeter pour les 5 formations]

### 4. Universites a {{wilaya}} ou proximite
[Liste des etablissements avec leurs specialites]

### 5. Calendrier d'orientation
- Inscription sur PROGRES : [Dates]
- Choix des voeux : [Conseils]
- Resultats d'affectation : [Dates]

### 6. Conseils personnalises
[Recommandations basees sur le profil]

### 7. Alternatives
- Formation professionnelle
- Ecoles privees agreees
- Etudes a l'etranger

Guide conforme au systeme LMD algerien et aux procedures MESRS.`
  },

  'preparation-concours-dz': {
    fields: [
      { name: 'type_concours', type: 'select', label: 'Type de concours', required: true, options: [
        'Concours d\'acces aux grandes ecoles', 'Concours de la Fonction publique',
        'Concours Doctorat', 'Concours enseignement', 'Concours police/armee',
        'Concours magistrature', 'Autre concours national'
      ]},
      { name: 'concours_specifique', type: 'text', label: 'Nom exact du concours', required: true, placeholder: 'Ex: ENS, EPAU, Douanes...' },
      { name: 'matieres', type: 'text', label: 'Matieres du concours', placeholder: 'Ex: Culture generale, Specialite...' },
      { name: 'duree_preparation', type: 'select', label: 'Temps de preparation', options: [
        'Moins d\'1 mois', '1-3 mois', '3-6 mois', 'Plus de 6 mois'
      ]},
      { name: 'niveau', type: 'select', label: 'Votre niveau actuel', options: [
        'Debutant', 'Intermediaire', 'Avance'
      ]},
    ],
    promptTemplate: `Tu es un specialiste de la preparation aux concours en Algerie.

TYPE : {{type_concours}}
CONCOURS : {{concours_specifique}}
MATIERES : {{matieres}}
TEMPS DE PREPARATION : {{duree_preparation}}
NIVEAU : {{niveau}}

## Programme de Preparation - {{concours_specifique}}

### 1. Presentation du concours
- Organisation/Ministere responsable
- Conditions d'acces
- Nombre de places (estimation)
- Date habituelle

### 2. Epreuves et coefficients

| Epreuve | Duree | Coefficient | Contenu |
|---------|-------|-------------|---------|
| ... | ... | ... | ... |

### 3. Programme de revision ({{duree_preparation}})

#### Semaine 1-2 :
[Planning detaille]

#### Semaine 3-4 :
[Planning detaille]

[Adapter selon la duree]

### 4. Ressources recommandees
- Manuels : [Liste]
- Sites web : [Liste]
- Anciens sujets : [Ou les trouver]

### 5. Methodologie par matiere

#### {{matieres}} :
- Points cles
- Methode de travail
- Pieges a eviter

### 6. Conseils le jour J
- Gestion du temps
- Presentation des copies
- Gestion du stress

### 7. Exemple de sujet
[Sujet type avec elements de correction]

### 8. Criteres de notation
[Ce que le jury attend]

Guide adapte aux specificites des concours algeriens.`
  },

};

// Icones par outil
const toolIcons: Record<string, any> = {
  'revision-bac-algerie': GraduationCap,
  'preparation-bem-algerie': BookOpen,
  'preparation-5eme-annee': BookOpen,
  'generateur-qcm-algerie': ClipboardList,
  'fiches-cours-algerie': FileText,
  'exercices-corriges-algerie': ClipboardList,
  'aide-dissertation-algerie': FileText,
  'traducteur-academique-dz': Languages,
  'orientation-universitaire-dz': Compass,
  'preparation-concours-dz': GraduationCap,
};

export default function EducationDzToolPage() {
  const params = useParams();
  const toolSlug = params.toolSlug as string;

  const [formData, setFormData] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const tool = educationDzTools.find(t => t.slug === toolSlug);
  const config = toolFormConfigs[toolSlug];
  const Icon = toolIcons[toolSlug] || GraduationCap;

  if (!tool || !config) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Outil non trouve</h1>
          <Link href="/tools/education-dz" className="text-teal-600 hover:underline">
            Retour aux outils Education DZ
          </Link>
        </div>
      </div>
    );
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // Simulation API call
    setTimeout(() => {
      setResult(`Resultat genere pour ${tool.name.fr}...\n\nContenu de demonstration base sur vos parametres.`);
      setIsLoading(false);
    }, 2000);
  };

  const handleCopy = () => {
    if (result) {
      navigator.clipboard.writeText(result);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/tools/education-dz" className="text-gray-400 hover:text-gray-600">
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <Link href="/" className="flex items-center gap-2">
              <span className="text-2xl font-bold text-green-600">IAFactory</span>
              <span className="text-sm bg-green-100 text-green-800 px-2 py-0.5 rounded">Algeria</span>
            </Link>
          </div>
          <div className="flex items-center gap-4">
            <div className="bg-gray-100 px-3 py-1.5 rounded-lg text-sm">
              <span className="text-gray-500">Credits:</span>
              <span className="font-semibold text-gray-900 ml-1">847</span>
            </div>
          </div>
        </nav>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Tool Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-teal-100 rounded-xl flex items-center justify-center">
              <Icon className="w-6 h-6 text-teal-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{tool.name.fr}</h1>
              <p className="text-gray-600">{tool.description.fr}</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="bg-teal-100 text-teal-700 px-3 py-1 rounded-full text-sm font-medium">
              {tool.credits} credits
            </span>
            <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-medium">
              Exclusif Algerie
            </span>
            {tool.priority === 'critical' && (
              <span className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm font-medium flex items-center gap-1">
                <Sparkles className="w-4 h-4" /> Populaire
              </span>
            )}
          </div>
        </div>

        {/* Form */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {config.fields.map((field: any) => (
              <div key={field.name}>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {field.label}
                  {field.required && <span className="text-red-500 ml-1">*</span>}
                </label>

                {field.type === 'text' && (
                  <input
                    type="text"
                    name={field.name}
                    placeholder={field.placeholder}
                    required={field.required}
                    value={formData[field.name] || ''}
                    onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  />
                )}

                {field.type === 'textarea' && (
                  <textarea
                    name={field.name}
                    placeholder={field.placeholder}
                    required={field.required}
                    rows={field.rows || 4}
                    value={formData[field.name] || ''}
                    onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  />
                )}

                {field.type === 'select' && (
                  <select
                    name={field.name}
                    required={field.required}
                    value={formData[field.name] || ''}
                    onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  >
                    <option value="">Selectionner...</option>
                    {field.options?.map((opt: string) => (
                      <option key={opt} value={opt}>{opt}</option>
                    ))}
                  </select>
                )}

                {field.type === 'number' && (
                  <input
                    type="number"
                    name={field.name}
                    placeholder={field.placeholder}
                    required={field.required}
                    value={formData[field.name] || ''}
                    onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  />
                )}
              </div>
            ))}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-teal-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-teal-700 transition flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Generation en cours...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  Generer ({tool.credits} credits)
                </>
              )}
            </button>
          </form>
        </div>

        {/* Result */}
        {result && (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Resultat</h3>
              <button
                onClick={handleCopy}
                className="flex items-center gap-2 text-gray-600 hover:text-gray-900"
              >
                {copied ? <Check className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4" />}
                {copied ? 'Copie!' : 'Copier'}
              </button>
            </div>
            <div className="bg-gray-50 rounded-lg p-4 whitespace-pre-wrap text-sm">
              {result}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 px-4 mt-12">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-gray-400">
            © 2026 IAFactory Algeria - Concu en Algerie
          </p>
        </div>
      </footer>
    </div>
  );
}
