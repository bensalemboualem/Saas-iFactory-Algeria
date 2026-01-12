# 🎮 Playground - IA Factory

> **Environnement interactif pour créer, tester et expérimenter avec l'IA**

Le Playground IA Factory est un espace sandbox où vous pouvez initialiser et expérimenter avec différents artefacts: prompts, modèles, conversations complètes, applications web, jeux, visualisations et bien plus.

---

## 🎯 Qu'est-ce que le Playground ?

Le **Playground IA Factory** est une fonctionnalité du Studio Créatif qui vous permet de:

✅ **Créer des artefacts interactifs** - Apps web, jeux, visualisations, outils
✅ **Tester différents modèles IA** - Comparer GPT-4o, Claude, Gemini, etc.
✅ **Expérimenter avec des prompts** - Itérer rapidement sur vos idées
✅ **Générer du code exécutable** - HTML, CSS, JavaScript, Python, SVG
✅ **Sauvegarder et partager** - Conserver vos créations pour référence future
✅ **Déployer en production** - Publier vos apps en un clic

**Environnement sandbox sécurisé:**
- Isolation complète
- Pas d'impact sur vos données production
- Exécution temps réel
- Preview instantané

---

## 🚀 Comment Accéder au Playground ?

### Méthode 1: Via le Studio Créatif

**Étapes:**

1. **Naviguer vers le Studio**
   ```
   http://localhost:8184/studio
   ```

2. **Se connecter ou créer un compte**
   - Si nouveau: Cliquer "Sign Up"
   - Si existant: Cliquer "Log In"

3. **Choisir le LLM**
   - Toolbar en haut
   - Sélectionner parmi:
     - GPT-4o (OpenAI) - Créativité maximale
     - Claude Sonnet 4.5 (Anthropic) - Raisonnement profond
     - Gemini 2.0 Flash (Google) - Rapide et multimodal
     - Llama 4 405B (Meta) - Open source puissant
     - DeepSeek V3 (DeepSeek) - Excellent pour code
     - Mixtral 8x22B (Mistral) - Français natif

4. **Écrire le prompt**
   ```
   "Créer un jeu de Snake en JavaScript avec HTML Canvas"
   ```

5. **Accéder au Playground**
   - Output inclura bouton "🎮 Show Playground"
   - Cliquer pour ouvrir
   - Code + Preview affichés côte à côte

---

### Méthode 2: Via Archon Hub

```
http://localhost:8182
→ Onglet "Playground"
→ Nouveau projet
```

---

### Méthode 3: Accès Direct

```
http://localhost:8184/playground
```

---

## 🎨 Types d'Artefacts Créables

### 1. Applications Web Interactives

**To-Do List App**
```
Prompt: "Créer une app to-do list avec React et Tailwind CSS"
```

**Fonctionnalités auto-générées:**
- ✅ Ajouter/supprimer tâches
- ✅ Marquer comme complété
- ✅ Filtrer (All/Active/Completed)
- ✅ Compteur de tâches
- ✅ LocalStorage pour persistance
- ✅ Design responsive

**Code généré:**
```jsx
import React, { useState, useEffect } from 'react';

function TodoApp() {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');
  const [filter, setFilter] = useState('all');

  // Load from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('todos');
    if (saved) setTodos(JSON.parse(saved));
  }, []);

  // Save to localStorage
  useEffect(() => {
    localStorage.setItem('todos', JSON.stringify(todos));
  }, [todos]);

  const addTodo = () => {
    if (input.trim()) {
      setTodos([...todos, { id: Date.now(), text: input, done: false }]);
      setInput('');
    }
  };

  const toggleTodo = (id) => {
    setTodos(todos.map(t => t.id === id ? {...t, done: !t.done} : t));
  };

  const deleteTodo = (id) => {
    setTodos(todos.filter(t => t.id !== id));
  };

  const filteredTodos = todos.filter(t => {
    if (filter === 'active') return !t.done;
    if (filter === 'completed') return t.done;
    return true;
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-500 to-pink-500 p-8">
      <div className="max-w-md mx-auto bg-white rounded-lg shadow-xl p-6">
        <h1 className="text-3xl font-bold text-center mb-6 text-purple-600">
          📝 Ma To-Do List
        </h1>

        {/* Input */}
        <div className="flex gap-2 mb-6">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && addTodo()}
            placeholder="Ajouter une tâche..."
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
          <button
            onClick={addTodo}
            className="bg-purple-500 text-white px-6 py-2 rounded-lg hover:bg-purple-600 transition"
          >
            Ajouter
          </button>
        </div>

        {/* Filters */}
        <div className="flex gap-2 mb-4">
          {['all', 'active', 'completed'].map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-1 rounded ${
                filter === f
                  ? 'bg-purple-500 text-white'
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>

        {/* Todos */}
        <div className="space-y-2">
          {filteredTodos.map(todo => (
            <div
              key={todo.id}
              className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
            >
              <input
                type="checkbox"
                checked={todo.done}
                onChange={() => toggleTodo(todo.id)}
                className="w-5 h-5"
              />
              <span className={`flex-1 ${todo.done ? 'line-through text-gray-400' : ''}`}>
                {todo.text}
              </span>
              <button
                onClick={() => deleteTodo(todo.id)}
                className="text-red-500 hover:text-red-700"
              >
                🗑️
              </button>
            </div>
          ))}
        </div>

        {/* Counter */}
        <div className="mt-4 text-center text-gray-600">
          {todos.filter(t => !t.done).length} tâche(s) restante(s)
        </div>
      </div>
    </div>
  );
}

export default TodoApp;
```

**Preview instantané** à droite du code.

---

### 2. Jeux Interactifs

**Snake Game**
```
Prompt: "Créer un jeu Snake classique avec HTML Canvas et JavaScript"
```

**Follow-up:**
```
"Ajouter un système de score et des obstacles qui apparaissent aléatoirement"
```

**Fonctionnalités:**
- 🎮 Contrôles clavier (flèches)
- 🍎 Nourriture qui apparaît aléatoirement
- 📊 Score et high score
- ⚠️ Détection de collision
- 🎨 Graphismes colorés
- 🔄 Restart automatique

---

**Bouncing Ball avec Obstacles**
```
Prompt: "Créer un SVG d'une balle qui rebondit"
```

**Follow-up:**
```
"Peux-tu créer un jeu où la balle doit éviter des obstacles en rebondissant?"
```

**Exemple de code SVG:**
```html
<!DOCTYPE html>
<html>
<head>
  <title>Bouncing Ball Game</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    svg {
      border: 3px solid white;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.1);
    }
    #score {
      position: absolute;
      top: 20px;
      color: white;
      font-size: 2rem;
      font-family: Arial;
    }
  </style>
</head>
<body>
  <div id="score">Score: 0</div>
  <svg id="game" width="600" height="400"></svg>

  <script>
    const svg = document.getElementById('game');
    const scoreEl = document.getElementById('score');
    let score = 0;

    // Ball
    const ball = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    ball.setAttribute('cx', 300);
    ball.setAttribute('cy', 200);
    ball.setAttribute('r', 15);
    ball.setAttribute('fill', '#ff6b6b');
    svg.appendChild(ball);

    let ballX = 300, ballY = 200;
    let ballVX = 3, ballVY = 3;

    // Obstacles
    const obstacles = [];
    function createObstacle() {
      const obstacle = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      obstacle.setAttribute('x', Math.random() * 560);
      obstacle.setAttribute('y', 0);
      obstacle.setAttribute('width', 40);
      obstacle.setAttribute('height', 40);
      obstacle.setAttribute('fill', '#4ecdc4');
      svg.appendChild(obstacle);
      obstacles.push({ el: obstacle, y: 0 });
    }

    // Spawn obstacles every 2 seconds
    setInterval(createObstacle, 2000);

    // Game loop
    function gameLoop() {
      // Move ball
      ballX += ballVX;
      ballY += ballVY;

      // Bounce off walls
      if (ballX <= 15 || ballX >= 585) ballVX *= -1;
      if (ballY <= 15 || ballY >= 385) ballVY *= -1;

      ball.setAttribute('cx', ballX);
      ball.setAttribute('cy', ballY);

      // Move obstacles
      obstacles.forEach((obs, i) => {
        obs.y += 2;
        obs.el.setAttribute('y', obs.y);

        // Check collision
        const obsX = parseFloat(obs.el.getAttribute('x'));
        if (
          ballX > obsX && ballX < obsX + 40 &&
          ballY > obs.y && ballY < obs.y + 40
        ) {
          alert('Game Over! Score: ' + score);
          location.reload();
        }

        // Remove if out of bounds
        if (obs.y > 400) {
          svg.removeChild(obs.el);
          obstacles.splice(i, 1);
          score += 10;
          scoreEl.textContent = 'Score: ' + score;
        }
      });

      requestAnimationFrame(gameLoop);
    }

    gameLoop();
  </script>
</body>
</html>
```

---

### 3. Visualisations de Données

**Dashboard Analytics**
```
Prompt: "Créer un dashboard analytics avec des graphiques interactifs pour visualiser des ventes mensuelles"
```

**Bibliothèques utilisées:**
- Chart.js pour graphiques
- D3.js pour visualisations avancées
- Recharts pour React

**Types de graphiques générés:**
- 📊 Bar charts (ventes par mois)
- 📈 Line charts (tendances)
- 🥧 Pie charts (répartition catégories)
- 📉 Area charts (évolution temporelle)

---

### 4. Outils Pratiques

**Calculatrice Scientifique**
```
Prompt: "Créer une calculatrice scientifique avec fonctions avancées"
```

**Convertisseur d'Unités**
```
Prompt: "App de conversion d'unités (longueur, poids, température, devise)"
```

**Générateur de QR Code**
```
Prompt: "Outil pour générer des QR codes personnalisés"
```

**Éditeur Markdown**
```
Prompt: "Éditeur Markdown avec preview en temps réel"
```

---

### 5. Designs & UI

**Landing Page**
```
Prompt: "Concevoir une landing page moderne pour une startup tech algérienne"
```

**Composants UI:**
```
Prompt: "Créer une bibliothèque de composants réutilisables: boutons, cards, modals, forms"
```

**Blog Template**
```
Prompt: "Design d'une page blog simple avec section commentaires"
```

**Portfolio**
```
Prompt: "Portfolio de développeur avec projets, skills et contact"
```

---

### 6. Applications Créatives

**Drawing App**
```
Prompt: "Développer une app de dessin où les utilisateurs peuvent créer et sauvegarder leurs croquis"
```

**Fonctionnalités:**
- 🎨 Palette de couleurs
- 🖌️ Différentes tailles de pinceau
- 🔄 Undo/Redo
- 💾 Sauvegarder en PNG
- 🗑️ Effacer tout

---

**Music Visualizer**
```
Prompt: "Créer un visualiseur de musique qui réagit au son"
```

---

### 7. Prompts Complexes

**Spaceship Asteroid Game**
```
Prompt: "Créer un SVG d'un vaisseau spatial"

Follow-up: "Peux-tu faire un jeu où je peux naviguer le vaisseau à travers un champ d'astéroïdes?"
```

**Résultat:**
- 🚀 Vaisseau contrôlable (flèches + espace pour tirer)
- ☄️ Astéroïdes générés aléatoirement
- 💥 Collisions détectées
- 🎯 Système de score
- 💖 Vies
- 🔊 Effets sonores (optionnel)

---

## 💾 Sauvegarder vos Artefacts

### Option 1: Sauvegarder dans IA Factory

**Étapes:**
1. Cliquer sur "💾 Save" en haut du Playground
2. Remplir formulaire:
   ```
   Nom: "To-Do List App v1"
   Description: "App de tâches avec React et Tailwind"
   Tags: "react", "todo", "webapp"
   Visibilité: Public / Private / Team
   ```
3. Confirmer

**Accès ultérieur:**
```
http://localhost:8182/playground/my-artifacts
→ Rechercher par nom/tags
→ Cliquer pour charger
→ Modifier ou dupliquer
```

---

### Option 2: Export Fichiers

**Formats disponibles:**
- 📄 **HTML** - Fichier unique standalone
- 📦 **ZIP** - Projet complet (HTML + CSS + JS)
- 📓 **Jupyter Notebook** - Pour code Python
- 🐙 **GitHub Gist** - Partage rapide

**Méthode:**
```
Bouton "📥 Export"
→ Sélectionner format
→ Télécharger
```

---

### Option 3: Push vers GitHub

**Workflow:**
```
1. Cliquer "🐙 Push to GitHub"
2. Autoriser IA Factory (OAuth)
3. Sélectionner repo (ou créer nouveau)
4. Choisir branch
5. Commit message: "Add bouncing ball game"
6. Push
```

**Structure générée:**
```
mon-repo/
├── index.html
├── style.css
├── script.js
├── README.md (auto-généré)
└── package.json (si applicable)
```

---

### Option 4: Déployer en Production

**Plateformes supportées:**
- ✅ **Vercel** - Gratuit, instantané
- ✅ **Netlify** - CI/CD automatique
- ✅ **GitHub Pages** - Hébergement statique
- ✅ **IA Factory Hosting** - Domaine personnalisé

**Processus:**
```
Cliquer "🚀 Deploy"
→ Choisir plateforme
→ Configurer domaine (optionnel)
→ Déployer (1-2 minutes)
→ URL live: https://mon-app.iafactory.dz
```

---

## 🧪 Tester Différents Modèles IA

### Comparaison de Modèles

**Le Playground permet de comparer les outputs de différents LLMs:**

**Exemple: Créer un jeu Snake**

**GPT-4o (OpenAI)**
- ✅ Code très structuré
- ✅ Commentaires détaillés
- ✅ Bonnes pratiques
- ⚠️ Parfois verbeux

**Claude Sonnet 4.5 (Anthropic)**
- ✅ Code élégant et concis
- ✅ Excellent raisonnement
- ✅ Gestion erreurs robuste
- ⚠️ Peut être conservateur

**Gemini 2.0 Flash (Google)**
- ✅ Très rapide
- ✅ Multimodal (images + code)
- ✅ Créatif
- ⚠️ Parfois imprévisible

**DeepSeek V3**
- ✅ Excellent pour code complexe
- ✅ Optimisations avancées
- ✅ Algorithmes efficaces
- ⚠️ Moins créatif design

**Mixtral 8x22B (Mistral)**
- ✅ Parfait pour français
- ✅ Commentaires bilingues FR/EN
- ✅ Bon équilibre
- ⚠️ Moins d'innovation

---

### Interface de Comparaison

**Mode Split Screen:**
```
┌─────────────────────┬─────────────────────┐
│   GPT-4o Output     │  Claude Output      │
├─────────────────────┼─────────────────────┤
│                     │                     │
│   [Code généré]     │   [Code généré]     │
│                     │                     │
├─────────────────────┼─────────────────────┤
│   [Preview]         │   [Preview]         │
└─────────────────────┴─────────────────────┘
```

**Voter pour le meilleur:**
```
👍 GPT-4o   ou   👍 Claude
```

Vos votes aident IA Factory à améliorer les recommandations de modèles.

---

## 🆘 Support & Aide

### Documentation Intégrée

**Bouton "❓ Help" dans Playground:**
- Quick tips
- Exemples de prompts
- Raccourcis clavier
- Troubleshooting

---

### Raccourcis Clavier

| Raccourci | Action |
|-----------|--------|
| `Ctrl + Enter` | Exécuter le code |
| `Ctrl + S` | Sauvegarder |
| `Ctrl + /` | Commenter/décommenter |
| `Ctrl + F` | Rechercher dans code |
| `Ctrl + H` | Remplacer |
| `Ctrl + Z` | Undo |
| `Ctrl + Shift + Z` | Redo |
| `F11` | Plein écran |

---

### Erreurs Communes

**1. Code ne s'exécute pas**
- Vérifier console (F12)
- Chercher erreurs de syntaxe
- Demander à IA de débugger: "Il y a une erreur, peux-tu corriger?"

**2. Preview ne s'affiche pas**
- Rafraîchir preview (bouton 🔄)
- Vérifier compatibilité navigateur
- Essayer mode incognito

**3. Performance lente**
- Optimiser le code (demander à IA)
- Réduire complexité
- Utiliser Web Workers si applicable

---

### Contacter le Support

**Si problème persiste:**
```
Bouton "🐛 Report Issue" dans Playground
→ Description du problème
→ Screenshot (auto-capturé)
→ Code (auto-attaché)
→ Envoyer
```

**Ou:**
- 📧 support@iafactory.dz
- 💬 Chat en direct: http://localhost:8182/support
- 📚 Documentation: [FAQ](./FAQ_IAFACTORY.md)

---

## 💼 Utilisation Commerciale

### Termes d'Utilisation

**Ce qui est permis:**
- ✅ Créer apps pour vos clients
- ✅ Utiliser dans produits commerciaux
- ✅ Modifier le code généré
- ✅ Déployer en production
- ✅ Vendre apps créées

**Ce qui est interdit:**
- ❌ Revendre accès Playground tel quel
- ❌ Scraper/copier massivement les prompts
- ❌ Utiliser pour spam/malware

**Licence du code généré:**
- Code généré = **votre propriété**
- Pas d'attribution requise
- Utilisation commerciale autorisée

**Plan Enterprise recommandé pour:**
- SLA garantis
- Support prioritaire
- API dédiée
- Quotas élevés

**Détails complets:**
```
http://localhost:8182/terms-of-service
```

---

## 🎓 Exemples de Prompts Avancés

### Prompts Créatifs

**Exemple 1: Animation SVG**
```
Prompt: "Créer une animation SVG d'un coucher de soleil sur le Sahara avec des dunes ondulantes"

Follow-up: "Ajouter des étoiles qui apparaissent progressivement et un chameau qui traverse"
```

---

**Exemple 2: Data Visualization**
```
Prompt: "Créer une visualisation interactive des statistiques COVID-19 en Algérie avec Chart.js"

Follow-up: "Ajouter un sélecteur de wilayas et un graphique comparatif"
```

---

**Exemple 3: E-commerce**
```
Prompt: "Développer un mini e-commerce de produits artisanaux algériens avec panier et checkout"

Follow-up: "Intégrer paiement CIB (Centre d'Impression Bancaire) et livraison Yalidine"
```

---

**Exemple 4: Educational**
```
Prompt: "Créer un quiz interactif sur l'histoire de l'Algérie avec score et explications"

Follow-up: "Ajouter des images historiques et un mode multijoueur"
```

---

**Exemple 5: Productivity**
```
Prompt: "Développer un timer Pomodoro avec statistiques de productivité"

Follow-up: "Ajouter intégration Google Calendar et notifications desktop"
```

---

**Exemple 6: Entertainment**
```
Prompt: "Créer un générateur de blagues algériennes avec text-to-speech en darija"

Follow-up: "Ajouter partage sur réseaux sociaux et vote meilleure blague"
```

---

**Exemple 7: Utilities**
```
Prompt: "Faire un convertisseur Dinar Algérien vers toutes devises avec taux en temps réel"

Follow-up: "Ajouter graphique historique des fluctuations et alertes de prix"
```

---

**Exemple 8: Social**
```
Prompt: "Développer un mur de messages anonymes type confession avec modération"

Follow-up: "Ajouter likes, comments, et filtre de contenu inapproprié"
```

---

## 📊 Analytics & Insights

### Métriques du Playground

**Accessible via:**
```
http://localhost:8182/playground/analytics
```

**Données affichées:**
- 📈 **Nombre d'artefacts créés** - Total et par type
- ⏱️ **Temps moyen de création** - De prompt à artefact final
- 🤖 **Modèles les plus utilisés** - Statistiques d'usage
- 🏆 **Artefacts les plus populaires** - Classement communautaire
- 💡 **Prompts les plus efficaces** - Ceux qui génèrent le meilleur code
- 🐛 **Taux d'erreur** - Par modèle et type d'artefact

---

### Insights Personnalisés

**Recommandations IA:**
```
"Basé sur vos créations, vous pourriez aimer:
- Créer un dashboard avec D3.js
- Essayer des animations Three.js
- Développer une PWA (Progressive Web App)"
```

---

## 🔐 Sécurité & Confidentialité

### Sandbox Sécurisé

**Le Playground exécute le code dans un environnement isolé:**
- ✅ Pas d'accès à vos fichiers locaux
- ✅ Pas d'accès réseau non autorisé
- ✅ Limites de CPU/RAM
- ✅ Timeout automatique (60s)

---

### Confidentialité du Code

**Vos artefacts sont:**
- 🔒 **Privés par défaut** - Visible uniquement par vous
- 🔐 **Chiffrés au repos** - AES-256
- 🌐 **Partageable sur demande** - Contrôle granulaire
- 🗑️ **Supprimable à tout moment** - Droit à l'oubli RGPD

---

### Bonnes Pratiques

**Ne jamais mettre dans le Playground:**
- ❌ API keys réelles
- ❌ Mots de passe
- ❌ Données personnelles sensibles
- ❌ Secrets d'entreprise

**À la place:**
- ✅ Utiliser des placeholders: `YOUR_API_KEY`
- ✅ Variables d'environnement
- ✅ Données de test/mock

---

## 🚀 Cas d'Usage Avancés

### 1. Prototypage Rapide

**Scénario:** Startup veut tester une idée d'app

**Workflow:**
```
1. Prompt: "Créer une app de covoiturage Alger-Oran"
2. Révision: Ajouter map, réservation, paiement
3. Test: Partager avec beta testeurs
4. Feedback: Itérer sur design/features
5. Production: Déployer version finale
```

**Temps total:** 2-4 heures (vs 2-4 semaines en dev classique)

---

### 2. Apprentissage Interactif

**Scénario:** Étudiant apprend React

**Workflow:**
```
1. Prompt: "Créer un compteur simple en React"
2. Analyse: Comprendre useState, props, events
3. Modification: Ajouter fonctionnalités (reset, incrémentation personnalisée)
4. Expérimentation: Essayer différents patterns (hooks, context)
5. Projet: Construire app complète
```

---

### 3. A/B Testing Design

**Scénario:** Designer teste 2 versions de landing page

**Workflow:**
```
1. Prompt A: "Landing page minimaliste startup tech"
2. Prompt B: "Landing page colorée et dynamique startup tech"
3. Comparaison: Afficher côte à côte
4. Test utilisateur: Partager liens avec audience
5. Analytics: Mesurer conversions
6. Décision: Choisir version gagnante
```

---

### 4. Génération de Templates

**Scénario:** Agence crée bibliothèque de templates

**Workflow:**
```
1. Créer 20+ templates (portfolio, e-commerce, blog, etc.)
2. Sauvegarder dans Playground
3. Personnaliser pour chaque client (couleurs, contenu)
4. Export et déploiement
5. Maintenance: Mise à jour centralisée
```

---

### 5. Formation Équipe

**Scénario:** CTO forme développeurs juniors

**Workflow:**
```
1. Créer série d'exercices interactifs
2. Partager via Playground
3. Développeurs modifient et expérimentent
4. Review de code par IA
5. Feedback personnalisé
6. Progression trackée
```

---

## 🔗 Intégrations

### Export vers n8n

**Automatiser déploiement:**
```
Playground → Export → n8n Workflow

Trigger: "Nouvel artefact créé"
→ Étape 1: Récupérer code
→ Étape 2: Push vers GitHub
→ Étape 3: Déclencher CI/CD (Vercel/Netlify)
→ Étape 4: Notifier sur Slack
→ Étape 5: Ajouter à portfolio
```

---

### API du Playground

**Endpoints disponibles:**

**Créer artefact:**
```http
POST /api/v1/playground/create
Content-Type: application/json
Authorization: Bearer <token>

{
  "prompt": "Créer un jeu Snake",
  "model": "gpt-4o",
  "language": "javascript",
  "framework": "vanilla"
}
```

**Response:**
```json
{
  "artifact_id": "art_abc123",
  "code": "// Code généré...",
  "preview_url": "http://localhost:8184/playground/preview/art_abc123",
  "created_at": "2025-01-18T10:00:00Z"
}
```

---

**Lister artefacts:**
```http
GET /api/v1/playground/artifacts
```

---

**Exécuter code:**
```http
POST /api/v1/playground/execute
Content-Type: application/json

{
  "artifact_id": "art_abc123",
  "input": {"data": "test"}
}
```

---

## ✅ Checklist Playground

### Pour Débutants

- [ ] Créer premier artefact simple (ex: bouton cliquable)
- [ ] Tester différents modèles IA
- [ ] Sauvegarder un artefact
- [ ] Partager avec un ami
- [ ] Exporter en HTML

### Pour Intermédiaires

- [ ] Créer app interactive (to-do list, calculatrice)
- [ ] Utiliser framework (React, Vue)
- [ ] Intégrer API externe
- [ ] Déployer sur Vercel/Netlify
- [ ] Créer 5+ artefacts variés

### Pour Avancés

- [ ] Builder app fullstack (frontend + backend)
- [ ] Implémenter auth & DB
- [ ] Optimiser performance
- [ ] Setup CI/CD
- [ ] Utiliser API Playground programmatiquement
- [ ] Contribuer templates à la communauté

---

## 🎯 Prochaines Fonctionnalités

### Q1-Q2 2025

**En développement:**
- 🔜 **Collaboration temps réel** - Coder ensemble comme Google Docs
- 🔜 **Templates marketplace** - Acheter/vendre templates
- 🔜 **Version history** - Git-like pour artefacts
- 🔜 **Mobile playground** - Créer depuis smartphone
- 🔜 **AI code review** - Suggestions automatiques
- 🔜 **Multi-file projects** - Projets complexes avec structure dossiers
- 🔜 **Backend playground** - Générer APIs Python/Node.js
- 🔜 **Database playground** - Tester requêtes SQL
- 🔜 **AI debugging** - IA identifie et corrige bugs automatiquement

---

## 📚 Ressources

### Documentation

- 📖 [FAQ Générale](./FAQ_IAFACTORY.md)
- 📖 [Studio Guide](./STUDIO_CREATIF_GUIDE.md)
- 📖 [Prompting Tips](./PROMPTING_TIPS_STUDIO.md)
- 📖 [API Reference](http://localhost:8180/docs)

### Tutoriels Vidéo

- 🎥 [Playground 101 - Introduction](./GUIDE_STUDIO_VIDEO.md)
- 🎥 [Créer votre premier jeu](./GUIDE_UTILISATION_BMAD.md)
- 🎥 [App React en 10 minutes](./QUICK_START.md)
- 🎥 [Déploiement Production](./DEPLOIEMENT_HETZNER.md)

### Exemples de Code

**GitHub Repository:**
```
https://github.com/iafactory/playground-examples
```

**Contient:**
- 100+ artefacts prêts à l'emploi
- Templates populaires
- Best practices
- Exercices interactifs

---

## 💬 Communauté

### Partager vos Créations

**Galerie Communautaire:**
```
http://localhost:8182/playground/gallery
```

**Catégories:**
- 🎮 Jeux
- 🎨 Design/UI
- 📊 Data Viz
- 🛠️ Outils
- 🎓 Éducation
- 💼 Business

**Système de votes:**
- ⭐ Note (1-5 étoiles)
- 💬 Commentaires
- 🔄 Forks/Remixes
- 📈 Analytics d'usage

---

## 🆘 Support

**Questions sur le Playground?**

📧 playground@iafactory.dz
💬 Chat: http://localhost:8182/support
📚 Docs: http://localhost:8183

---

**Version**: 1.0.0
**Dernière mise à jour**: 2025-01-18

🇩🇿 **IA Factory Algeria - Créez, Expérimentez, Innovez**

---

Copyright © 2025 IA Factory Algeria. Tous droits réservés.
