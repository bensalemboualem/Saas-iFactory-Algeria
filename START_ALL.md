# 🚀 Démarrage Complet de IA Factory

## ✅ Configuration Effectuée

La configuration a été complétée avec succès :

1. **Gateway** : Configuré avec SQLite sur port **5191**
2. **Base de données** : Créée avec 1000 crédits pour test
3. **API Key de test** : `iaf_test_key_12345`
4. **User de test** : `test@iafactory.dz`

---

## 🎯 Démarrage des Services

### Fermez TOUS les terminaux PowerShell ouverts

Avant de commencer, fermez tous les terminaux PowerShell/CMD pour libérer les processus.

### Ouvrez 4 nouveaux terminaux PowerShell

#### Terminal 1: Gateway (Port 5191)
```powershell
cd C:\Users\bbens\iafactorychatgpt_v2\apps\gateway
pnpm dev
```

Attendez de voir : `[INFO] IAFactory Gateway running on http://localhost:5191`

#### Terminal 2: Bolt-UI (Port 5190)
```powershell
cd C:\Users\bbens\iafactorychatgpt_v2\apps\bolt-ui
pnpm dev
```

Attendez de voir : `➜  Local:   http://localhost:5190/`

#### Terminal 3: Meta Orchestrator (Port 8100)
```powershell
cd C:\Users\bbens\iafactorychatgpt_v2\orchestrators\meta
uvicorn src.main:app --port 8100 --reload
```

#### Terminal 4: BMAD + Archon (déjà lancés)
Les orchestrateurs BMAD (8052), Archon (8051) et Bolt (8053) sont déjà actifs ✅

---

## 🧪 Test

### 1. Ouvrez votre navigateur

Accédez à : **http://localhost:5190**

### 2. Vérifiez le badge de crédits

Vous devriez voir un badge avec **1000.00 credits** en haut de l'interface Bolt-UI.

### 3. Test API (optionnel)

Dans PowerShell :

```powershell
curl http://localhost:5191/api/credits/balance `
  -H "Authorization: Bearer iaf_test_key_12345"
```

Devrait retourner : `{"balance":1000}`

---

## ⚠️ Troubleshooting

### Si le Gateway ne démarre pas
```powershell
cd apps/gateway
pnpm db:push
pnpm dev
```

### Si Bolt-UI a des erreurs d'icônes
Les warnings d'icônes sont normaux et n'empêchent pas le fonctionnement.

### Si les crédits affichent "Offline"
1. Vérifiez que le Gateway tourne sur port 5191
2. Vérifiez la console du navigateur pour les erreurs
3. Hard refresh (Ctrl+Shift+R)

---

## 📊 Services Actifs

| Service | Port | URL |
|---------|------|-----|
| Bolt-UI | 5190 | http://localhost:5190 |
| Gateway | 5191 | http://localhost:5191 |
| Meta | 8100 | http://localhost:8100 |
| Archon | 8051 | http://localhost:8051 |
| BMAD | 8052 | http://localhost:8052 |
| Bolt Orch. | 8053 | http://localhost:8053 |

---

## ✅ Succès !

Une fois tous les services démarrés :

1. **Bolt-UI** sera accessible sur http://localhost:5190
2. Le **badge de crédits** affichera 1000 crédits
3. Vous pourrez utiliser **Nexus Mode** avec tous les orchestrateurs

Bon développement ! 🎉
