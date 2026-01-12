# 🧪 Test des Agents BMAD - Guide Pratique

## ✅ Installation Complète!

Les agents BMAD sont maintenant disponibles dans Claude Code via slash commands.

---

## 🎯 3 Agents Installés

| Slash Command | Agent | Rôle |
|--------------|-------|------|
| `/bmad-pm` | John (Product Manager) | Requirements, PRD, prioritisation |
| `/bmad-architect` | Winston (Architect) | Architecture système, tech decisions |
| `/bmad-dev` | Developer | Implémentation, code review, refactoring |

---

## 🚀 Test 1: Conversation avec le Product Manager

### Lancer l'Agent
Dans Claude Code, tape:
```
/bmad-pm
```

### Scénario de Test
```
Toi: Je veux créer une application de gestion de tâches pour équipes distribuées

Réponse Attendue:
John (PM) va te poser des questions pour comprendre:
- Le problème réel (pourquoi les outils existants ne marchent pas?)
- Les utilisateurs (taille équipes, rôles)
- L'impact business (métriques de succès)
- Les contraintes (budget, timeline, tech)
```

### Continuer la Conversation
```
Toi: On a 50 équipes de 10 personnes, principalement des devs et PMs.
     Le problème c'est que les tools actuels sont trop lourds.

Réponse Attendue:
John va:
- Analyser le problème
- Proposer un MVP scope
- Suggérer de lancer *workflow-init ou *prd
```

### Workflows Disponibles
```
*workflow-init     → Initialisation projet guidée
*prd               → Créer Product Requirements Document
*quick-spec        → Spec rapide pour petites features
*workflow-status   → Voir où tu en es
*party-mode        → Collaboration multi-agents
```

---

## 🏗️ Test 2: Conversation avec l'Architecte

### Lancer l'Agent
```
/bmad-architect
```

### Scénario de Test
```
Toi: J'ai besoin d'une architecture pour une app de chat en temps réel avec 10K utilisateurs

Réponse Attendue:
Winston (Architect) va demander:
- Scale et performance (latence, concurrent users)
- Features core (1-to-1, groupes, audio/vidéo)
- Contraintes (cloud provider, budget, team size)
```

### Continuer la Conversation
```
Toi: Chat texte seulement, groupes jusqu'à 50 personnes, latence <200ms acceptable,
     team de 5 devs, budget AWS modéré

Réponse Attendue:
Winston va proposer:
- Architecture pragmatique (probablement monolithe avec WebSockets)
- Stack technique ("boring tech" - Django/Rails + Postgres + Redis)
- Justification business (pourquoi pas microservices pour cette échelle)
- Diagrammes d'architecture
```

### Workflows Disponibles
```
*create-architecture         → Créer architecture scale-adaptive
*validate-architecture       → Valider architecture existante
*implementation-readiness    → Vérifier readiness avant dev
*workflow-status             → Check status
*party-mode                  → Collaboration multi-agents
```

---

## 💻 Test 3: Conversation avec le Developer

### Lancer l'Agent
```
/bmad-dev
```

### Scénario de Test 1: Implémentation
```
Toi: Implémente l'authentification JWT pour mon API FastAPI

Réponse Attendue:
Le Developer va:
- Poser des questions (refresh tokens? durée? storage?)
- Proposer une approche claire
- **Montrer du code immédiatement** (auth_service.py exemple)
- Suggérer tests à écrire
```

### Scénario de Test 2: Code Review
```
Toi: Revue ce code:

def get_user(user_id):
    result = db.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return result[0] if result else None

Réponse Attendue:
Le Developer va identifier:
❌ SQL Injection vulnerability
❌ Pas de error handling
❌ Pas de type hints
✅ Proposer du code refactoré avec bonnes pratiques
```

### Scénario de Test 3: Refactoring
```
Toi: Ce code est trop complexe, peux-tu le simplifier?

[Paste du code avec beaucoup de if/else imbriqués]

Réponse Attendue:
Le Developer va:
- Calculer complexité cyclomatique
- Extract methods pour chaque responsabilité
- Utiliser patterns (Strategy, Factory)
- Montrer le code refactoré avec comparaison avant/après
```

### Workflows Disponibles
```
*dev-story          → Implémenter une user story complète
*code-review        → Revue de code détaillée
*refactor           → Refactoring guidé
*bug-fix            → Debug et correction
*test-generation    → Créer tests complets
*workflow-status    → Check status
```

---

## 🎭 Personnalités des Agents

### John (PM) 📋
**Phrases typiques:**
- "Quel est le WHY derrière cette feature?"
- "Comment mesurons-nous le succès?"
- "Quelle est la valeur business?"
- "Pouvons-nous faire plus simple pour le MVP?"

**Style:**
- Direct et analytique
- Data-driven
- Challenges les assumptions
- Prioritisation ruthless

### Winston (Architect) 🏗️
**Phrases typiques:**
- "Let's design simple solutions that scale when needed"
- "I prefer boring technology that works"
- "User journeys should drive technical decisions"
- "What's the business value of this complexity?"

**Style:**
- Pragmatique
- Balance idéalisme et réalité
- Focus ROI technique
- "Boring tech wins"

### Developer 💻
**Phrases typiques:**
- "Let me show you with code"
- "Here's a cleaner approach"
- "Let's write the test first"
- "YAGNI - we don't need that yet"

**Style:**
- Pratique et orienté code
- Montre plutôt qu'explique
- Quality-focused
- Refactoring mindset

---

## 🔄 Workflows Multi-Agents

### Scénario Complet: Du Concept au Code

**Étape 1: PM - Définir le Produit**
```
/bmad-pm

Toi: Je veux créer une app de gestion de tâches

John: [Pose questions WHY]
Toi: [Réponds aux questions]
John: Parfait! Lance *prd pour documenter

*prd
[John crée un PRD complet]
```

**Étape 2: Architect - Créer l'Architecture**
```
/bmad-architect

Toi: Crée l'architecture pour ce PRD

Winston: [Analyse le PRD]
Winston: [Pose questions techniques]
Toi: [Réponds sur scale, contraintes]
Winston: Lance *create-architecture

*create-architecture
[Winston crée architecture.md avec diagrammes]
```

**Étape 3: Developer - Implémenter**
```
/bmad-dev

Toi: Implémente la feature d'authentification

Developer: [Clarifie requirements]
Developer: [Montre du code]
Toi: Parfait, continue

*dev-story
[Developer implémente + tests]
```

---

## 🎪 Party Mode - Collaboration Multi-Agents

### Quand l'utiliser?
- Décisions complexes nécessitant multiple perspectives
- Design reviews (PM + Architect + Dev ensemble)
- Brainstorming de solutions
- Résolution de problèmes difficiles

### Comment l'activer?
```
Avec n'importe quel agent chargé:

*party-mode

Résultat:
Tous les agents BMAD rejoignent la conversation!
- PM apporte perspective business
- Architect apporte contraintes techniques
- Developer apporte faisabilité
→ Discussion collaborative riche
```

### Exemple d'Usage
```
/bmad-pm
*party-mode

Toi: On doit choisir entre MongoDB et PostgreSQL pour notre app

PM (John): "Quel est l'impact sur le time-to-market? Les devs connaissent quoi?"
Architect (Winston): "Pour du CRUD simple, Postgres. Relations complexes? Encore Postgres. NoSQL seulement si vraiment besoin de flexible schema."
Developer: "Postgres. Meilleur écosystème d'outils, migrations faciles, ACID guarantees. MongoDB seulement si on a vraiment besoin de documents imbriqués profonds."

→ Consensus: Postgres (boring tech wins!)
```

---

## ✅ Checklist de Validation

Teste chaque scénario et coche:

### Product Manager (John)
- [ ] `/bmad-pm` charge l'agent correctement
- [ ] John pose des questions WHY pertinentes
- [ ] John analyse en termes business/user value
- [ ] Workflows `*workflow-init`, `*prd` sont mentionnés
- [ ] Style direct et analytique

### Architect (Winston)
- [ ] `/bmad-architect` charge l'agent correctement
- [ ] Winston pose questions techniques (scale, contraintes)
- [ ] Winston propose solutions pragmatiques
- [ ] Préférence pour "boring tech"
- [ ] Workflows `*create-architecture` fonctionnent

### Developer
- [ ] `/bmad-dev` charge l'agent correctement
- [ ] Developer montre du code immédiatement
- [ ] Code reviews identifient vrais problèmes
- [ ] Refactoring améliore qualité
- [ ] Tests mentionnés systématiquement

### Collaboration
- [ ] `*party-mode` amène plusieurs agents
- [ ] Discussions multi-perspectives fonctionnent
- [ ] Consensus atteint sur décisions complexes

---

## 🐛 Troubleshooting

### Agent ne se charge pas
```bash
# Vérifier que les fichiers existent
ls C:\Users\bbens\rag-dz\.claude\commands\bmad\

# Devrait afficher:
# bmad-pm.md
# bmad-architect.md
# bmad-dev.md
```

### Slash command non reconnu
1. Redémarre Claude Code
2. Vérifie que le répertoire `.claude/commands/bmad/` existe
3. Essaie `/` pour voir les commandes disponibles

### Agent charge mais ne répond pas comme attendu
C'est normal! Les agents sont des prompts qui guident Claude.
La conversation sera naturelle mais suivra la personnalité définie.

---

## 📊 Métriques de Succès

**Installation Réussie si:**
- ✅ 3 slash commands visibles dans Claude Code
- ✅ Chaque agent a sa personnalité distincte
- ✅ Workflows mentionnés correctement
- ✅ Conversations naturelles et utiles

**Bonus:**
- ✅ Party mode fonctionne (multi-agents)
- ✅ Workflows générent des documents
- ✅ Agents s'adaptent à ton contexte

---

## 🎯 Prochaines Étapes

1. **Teste les 3 agents** avec les scénarios ci-dessus
2. **Utilise-les sur un vrai projet** (petit MVP)
3. **Expérimente party-mode** pour décisions complexes
4. **Partage ton feedback** sur ce qui marche/marche pas

---

## 📚 Ressources

- **Agents disponibles:** `.claude/commands/bmad/`
- **Documentation BMAD:** `bmad/README.md`
- **Guide conversation:** `GUIDE_CONVERSATION_BMAD.md`
- **Architecture écosystème:** `ECOSYSTEM_MCP_BMAD_ARCHON.md`

---

**Prêt à tester ! 🚀**

Commence par `/bmad-pm` et dis-lui ce que tu veux construire !
