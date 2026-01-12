#  IAFactory - SaaS Gateway IA Algérie

Gateway multi-providers IA + paiement monnaie locale pour marché algérien

**Marché** : 2M+ étudiants + PME + professions libérales

---

##  Quick Start

\\\ash
# Gateway
cd iafactory-gateway-python
docker-compose up -d

# Gateway : http://localhost:3001
# Docs : http://localhost:3001/docs
\\\

---

##  Architecture

### Gateway Python (Port 3001)
- FastAPI + PostgreSQL
- 9 providers IA : OpenAI , Anthropic, Groq, DeepSeek, Mistral, Gemini, Cohere, Together, OpenRouter
- Facturation automatique par token
- Webhook Chargily (paiements Algérie)

### Apps
- **Academy** (8200) : LMS
- **AI-Tools** (8003) : 7 outils IA
- **Video** (8240) : Génération vidéos

---

##  Status

- Gateway : Opérationnel
- OpenAI : Testé et validé
- Academy : E2E testé (19 tokens débités)
- Facturation : Automatique PostgreSQL

**Progression : 75%**

---

##  Reste à faire

- Clés prod 8 providers
- Tests E2E AI-Tools + Video
- RAG Academy (dépendances)

---

**Backup** : D:\\iafactorychatgpt\\

Voir FINAL-16H30.md pour détails session
