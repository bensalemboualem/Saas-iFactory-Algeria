# /prp:execute [PRP-XXX]

Exécute un PRP (Product Requirement Plan) spécifique.

## Usage

```
/prp:execute PRP-001
/prp:execute PRP-002
...
```

## Workflow

1. **Lire le PRP**
   - Ouvrir `PRPs/[PRP-XXX]-*.md`
   - Comprendre l'objectif
   - Identifier les tâches (T1, T2, ...)

2. **Exécuter séquentiellement**
   - Pour chaque tâche Ti:
     - Lire les instructions
     - Exécuter le code/commandes
     - Valider selon les critères
     - Marquer DONE

3. **Commits**
   - Format: `feat(PRP-XXX): description`
   - Un commit par tâche complétée

4. **Blocage?**
   - Créer `questions/[date]-question.md`
   - Décrire le problème
   - Proposer des solutions

## Règles

- NE JAMAIS skip une tâche
- NE JAMAIS continuer si validation échoue
- TOUJOURS committer après chaque tâche
- RESPECTER l'ordre T1 → T2 → T3 → ...

## Exemple

```
Exécution PRP-001...

T1: Vérification Environnement
   ✅ Docker 24.0.7
   ✅ Node 20.10.0
   ✅ Python 3.11.6
   → DONE

T2: Structure Monorepo
   [création des dossiers...]
   → DONE
   
[commit] feat(PRP-001): T2 structure monorepo

...
```

## Après complétion

1. Vérifier tous les critères cochés
2. Commit final si nécessaire
3. Passer au PRP suivant
