# ROADMAP RÉPARATION ACADEMY

## DIAGNOSTIC
Academy backend : Crash sur import chromadb/langchain
Build échoue : conflit pydantic-settings 2.1.0 vs >=2.4.0

## PLAN EXÉCUTION (ordre strict)

### ÉTAPE 1 : Restaurer requirements.txt qui marchait (5 min)
Objectif : Copier requirements.txt depuis backup
Action : Copy-Item D:\iafactorychatgpt\apps\academy\backend\requirements.txt
Validation : Build réussit

### ÉTAPE 2 : Désactiver RAG dans code (5 min)
Objectif : Commenter imports RAG sans casser syntaxe
Fichier : app/main.py ligne 15 + lignes 239-240
Action : Édition manuelle ou restauration
Validation : Backend démarre, health 200

### ÉTAPE 3 : Rebuild + test (5 min)
Objectif : Backend UP
Action : docker-compose build backend && up
Validation : curl health 200

### ÉTAPE 4 : Test E2E Academy  DeepSeek (5 min)
Objectif : Chatbot fonctionne
Action : python chatbot_deepseek.py
Validation : Tokens débités

TOTAL : 20 min

## ACTIONS MAINTENANT (dans l'ordre)

1. Copier requirements.txt backup
2. Éditer main.py (supprimer 3 lignes RAG)
3. Rebuild
4. Test

Pas de choix. Exécution directe.
