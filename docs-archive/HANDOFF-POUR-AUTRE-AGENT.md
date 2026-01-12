#  HANDOFF IAFactory - Pour Agent Suivant

## CONTEXTE
Session 12h15 (4h-15h25) - Utilisateur fatigué - Reprendre ici

##  ÉTAT ACTUEL VALIDÉ

### Gateway Python - Port 3001 - OPÉRATIONNEL
- PostgreSQL connecté : 2 users, 3 transactions validées
- Crédits persistants : test-user a 9983 crédits
- Facturation auto : débite tokens à chaque appel LLM
- OpenAI testé et validé 
- 8 autres providers créés (pas testés)

Fichiers :
- D:\IAFactory\iafactory-gateway-python\
- Docker : docker-compose up -d (déjà lancé)

### Apps migrées (partiellement)
- Academy : 3 fichiers imports commentés (pas remplacés)
- AI-Tools : imports commentés
- Video : imports commentés

### Architecture
- 150+ fichiers restructurés
- Ports renumérotés
- 33 composants copiés (pas testés)

##  TODO PRIORITAIRE (ordre strict)

### IMMÉDIAT (2h)
1. Remplacer imports commentés par vrais appels httpx au gateway
   Fichiers : academy/llm_service.py, chatbot_pro.py, chatbot_rag.py
   
2. Tester 3 providers avec vraies clés :
   - Groq : gskmw3p2HWSQaJPUh4z25DlWGdyb3FYZhFyV2xl8rO8f5dr7
   - DeepSeek : sk-e2d7d2146009413c86f74bf80f4e0c7e
   - Anthropic : (dans .env)

### CRITIQUE (4h)
3. Tester 5 apps core avec gateway
4. Réactiver auth sur gateway
5. Tests end-to-end complets

### IMPORTANT (6h)
6. Migrer 10 apps restantes
7. Centraliser JWT
8. CLAUDE.md tous dossiers

##  COMMANDES UTILES

Lancer gateway :
cd D:\IAFactory\iafactory-gateway-python
docker-compose up -d

Test crédits :
curl http://localhost:3001/api/credits/test-user

Test LLM :
\{
    "messages":  [
                     {
                         "content":  "Hello",
                         "role":  "user"
                     }
                 ],
    "model":  "gpt-3.5-turbo",
    "max_tokens":  10
} = @{model=\"gpt-3.5-turbo\";messages=@(@{role=\"user\";content=\"Test\"})} | ConvertTo-Json -Depth 10
curl http://localhost:3001/api/llm/chat/completions -Method POST -Body \{
    "messages":  [
                     {
                         "content":  "Hello",
                         "role":  "user"
                     }
                 ],
    "model":  "gpt-3.5-turbo",
    "max_tokens":  10
} -ContentType \"application/json\" -UseBasicParsing

Logs :
docker logs iafactory-gateway-python-gateway-1 --tail 20

##  BACKUP
D:\IAFactory-backup-2025-01-11-04h00\

##  ATTENTION
Utilisateur a travaillé 12h15 - Vérifier logique fatigue avant gros changements

TOTAL RESTE : ~12h de travail
