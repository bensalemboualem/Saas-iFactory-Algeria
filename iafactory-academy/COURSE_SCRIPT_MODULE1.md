# COURSE SCRIPT — MODULE 1 (RAG Fundamentals, ~30 min)

Usage: script mot-à-mot pour enregistrer le Module 1 du cours RAG. 4 leçons, 30 minutes total. Slides = suggestions; lis le script, garde l’énergie et le rythme.

## Leçon 1.1 — Introduction (5 min)
- Slide 1: Titre — "RAG Fundamentals" | Script: "Bienvenue, je suis Boualem. Ce cours te montre comment construire un RAG de A à Z."
- Slide 2: Objectifs — 3 bullets (comprendre RAG, assembler un pipeline, évaluer rapidement)
- Slide 3: Pour qui? — Dév/DS/PM technique; prérequis: Python, bases LLM
- Slide 4: Plan du cours — Modules: Fundamentals, Data prep, Retrieval, Orchestration, Eval/Prod
- Slide 5: Résultats attendus — "À la fin, tu déploies un RAG simple en prod"
- Slide 6: Matériel — Python, FastAPI, embeddings, vector DB (FAISS/Redis), OpenAI/LLM
- Slide 7: Conseils — Ship > perfection; tester chaque bloc; mesurer

## Leçon 1.2 — Qu'est-ce que RAG? (10 min)
- Slide 1: Problème LLM — hallucinations, fraîcheur des données
- Slide 2: RAG = Retrieve + Generate — schéma 2 blocs
- Slide 3: Flow simple — User query → Retriever → Context → LLM → Answer
- Slide 4: Use cases — FAQ interne, chat produit, support client, recherche doc
- Slide 5: Mini démo verbale — "Imagine un bot support docs internes" (expliquer input/output)
- Slide 6: Bénéfices — précision, contrôle, coûts réduits vs fine-tuning
- Slide 7: Points d’attention — qualité des docs, chunking, prompting clair

## Leçon 1.3 — RAG vs Fine-tuning (8 min)
- Slide 1: Définition fine-tuning — adapter les poids; utile pour style/format
- Slide 2: Tableau comparatif (RAG vs FT) — coûts, data besoin, fraîcheur, contrôle
- Slide 3: Quand RAG? — data vivante, docs internes, faible dataset, besoin de citations
- Slide 4: Quand FT? — style spécifique, tâches fermées, low-latency offline
- Slide 5: Combo — FT modèle + RAG pour contexte dynamique
- Slide 6: Règle pratique — commence RAG, passe FT si patterns stables

## Leçon 1.4 — Components d'un RAG (7 min)
- Slide 1: Les 4 blocs — Ingestion, Indexation, Retrieval, Generation
- Slide 2: Ingestion — collecte docs, formats, nettoyage
- Slide 3: Preprocessing — chunking, métadonnées, stopwords, langue
- Slide 4: Embeddings — modèle (OpenAI, Instructor, bge), dimension, coût
- Slide 5: Vector DB — FAISS/Chroma/Redis; critères: perf, coût, ops
- Slide 6: Prompt & LLM — template avec contexte, citations, guardrails
- Slide 7: Flow complet — schéma textuel: Docs → Preprocess → Embed → Store → Query → Retrieve k → Re-rank (option) → LLM → Answer

## Transitions & Timing
- Entre leçons: "Dans la prochaine section, on voit comment RAG se compare au fine-tuning." / "Ensuite, on détaille chaque composant."
- Garde un rythme 140-160 wpm; chaque slide ~30-45s.

## Checklist Enregistrement
Avant: micro testé, lumière face, fond propre, slides prêtes, eau.
Pendant: sourire, rythme constant, rappeler l’objectif par le résultat concret.
Après: sauvegarder bruts, noter timecodes pour montage, enregistrer B-roll (screens).