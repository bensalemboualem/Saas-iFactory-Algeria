# 🎯 Guide d'intégration BMAD dans Bolt.DIY

## ✅ Composants créés

### 1. **AgentSelector.tsx** - Sélecteur d'agents BMAD
- **Localisation**: `bolt-diy/app/components/chat/AgentSelector.tsx`
- **Fonctionnalité**:
  - Charge dynamiquement les 19 agents BMAD depuis l'API
  - Affiche dropdown avec nom, rôle, catégorie et description
  - Code couleur par catégorie (strategic, technical, operational, specialized)
  - Mode "No Agent" pour utiliser Bolt par défaut

### 2. **bmad-client.ts** - Client API BMAD
- **Localisation**: `bolt-diy/app/lib/bmad-client.ts`
- **Fonctions**:
  - `fetchBMADAgents()`: Récupère liste des agents
  - `sendMessageToBMADAgent()`: Envoie message à un agent spécifique
  - `analyzeConversation()`: Analyse si conversation = projet
  - `createProjectFromConversation()`: Crée projet Archon automatiquement
  - `isConversationLikelyAProject()`: Détection locale projet
  - `extractAgentsUsed()`: Extrait agents utilisés depuis historique

### 3. **CreateArchonProjectButton.tsx** - Création projet automatique
- **Localisation**: `bolt-diy/app/components/chat/CreateArchonProjectButton.tsx`
- **Composants**:
  - `CreateArchonProjectButton`: Bouton apparaît après 5+ messages si projet détecté
  - `ProjectCreatedNotification`: Notification succès avec liens projet

## 📝 Intégration dans BaseChat.tsx

### Étape 1: Imports

Ajoutez ces imports en haut de `bolt-diy/app/components/chat/BaseChat.tsx`:

```typescript
import { AgentSelector } from './AgentSelector';
import { CreateArchonProjectButton, ProjectCreatedNotification } from './CreateArchonProjectButton';
import { sendMessageToBMADAgent, extractAgentsUsed, type BMADAgent, type BMADMessage } from '~/lib/bmad-client';
```

### Étape 2: State Management

Ajoutez ces states dans le composant `BaseChat`:

```typescript
const [selectedBMADAgent, setSelectedBMADAgent] = useState<BMADAgent | null>(null);
const [bmadConversationHistory, setBmadConversationHistory] = useState<BMADMessage[]>([]);
const [createdProject, setCreatedProject] = useState<{
  projectId: string;
  boltUrl: string;
  archonUrl?: string;
} | null>(null);
```

### Étape 3: Modifier handleSendMessage

Remplacez la fonction `handleSendMessage` pour router vers BMAD si agent sélectionné:

```typescript
const handleSendMessage = async (event: React.UIEvent, messageInput?: string) => {
  const message = messageInput || input;

  // Si un agent BMAD est sélectionné, router vers BMAD
  if (selectedBMADAgent) {
    try {
      // Ajouter message utilisateur à l'historique BMAD
      const userMessage: BMADMessage = {
        role: 'user',
        content: message,
        agent: 'User',
      };

      const newHistory = [...bmadConversationHistory, userMessage];
      setBmadConversationHistory(newHistory);

      // Envoyer à l'agent BMAD
      const response = await sendMessageToBMADAgent(
        selectedBMADAgent.id,
        message,
        newHistory
      );

      // Ajouter réponse agent à l'historique
      const agentMessage: BMADMessage = {
        role: 'assistant',
        content: response,
        agent: selectedBMADAgent.id,
      };

      setBmadConversationHistory([...newHistory, agentMessage]);

      // Afficher dans l'UI Bolt (convertir en format Message)
      if (append) {
        append({
          id: Date.now().toString(),
          role: 'assistant',
          content: `**[${selectedBMADAgent.name}]**\n\n${response}`,
        });
      }
    } catch (error) {
      console.error('Error sending message to BMAD agent:', error);
      // Afficher erreur dans UI
    }

    // Clear input
    if (handleInputChange) {
      const syntheticEvent = {
        target: { value: '' },
      } as React.ChangeEvent<HTMLTextAreaElement>;
      handleInputChange(syntheticEvent);
    }

    return;
  }

  // Sinon, utiliser Bolt par défaut
  if (sendMessage) {
    sendMessage(event, messageInput);
    setSelectedElement?.(null);

    if (recognition) {
      recognition.abort();
      setTranscript('');
      setIsListening(false);

      if (handleInputChange) {
        const syntheticEvent = {
          target: { value: '' },
        } as React.ChangeEvent<HTMLTextAreaElement>;
        handleInputChange(syntheticEvent);
      }
    }
  }
};
```

### Étape 4: Ajouter AgentSelector dans l'UI

Dans la section du chat (avant ChatBox), ajoutez:

```typescript
<div className="flex flex-col gap-2">
  {/* BMAD Agent Selector */}
  <div className="flex items-center justify-between">
    <AgentSelector
      selectedAgent={selectedBMADAgent}
      onAgentSelect={(agent) => {
        setSelectedBMADAgent(agent);
        console.log('Selected BMAD Agent:', agent);
      }}
      className="flex-1"
    />
  </div>

  {/* Create Project Button - apparaît après 5+ messages */}
  {bmadConversationHistory.length >= 5 && !createdProject && (
    <CreateArchonProjectButton
      messages={bmadConversationHistory}
      agentsUsed={extractAgentsUsed(bmadConversationHistory)}
      onProjectCreated={(projectId, boltUrl) => {
        setCreatedProject({
          projectId,
          boltUrl,
          archonUrl: `http://localhost:8180/projects/${projectId}`,
        });
      }}
    />
  )}

  {/* Project Created Notification */}
  {createdProject && (
    <ProjectCreatedNotification
      projectId={createdProject.projectId}
      boltUrl={createdProject.boltUrl}
      archonUrl={createdProject.archonUrl}
      onDismiss={() => setCreatedProject(null)}
    />
  )}

  {/* Existing ChatBox */}
  <ChatBox
    // ... existing props
  />
</div>
```

## 🔧 Variables d'environnement

Vérifiez que `.env.local` contient:

```bash
# Backend RAG.dz
VITE_ARCHON_API_URL=http://localhost:8180
VITE_MCP_SERVER_URL=http://localhost:8051

# BMAD Agents
VITE_BMAD_AGENTS_URL=http://localhost:8180/api/bmad/agents
VITE_BMAD_CHAT_URL=http://localhost:8180/api/bmad/chat
VITE_COORDINATION_URL=http://localhost:8180/api/coordination

# DeepSeek pour agents BMAD
DEEPSEEK_API_KEY=sk-e2d7d214600946479856ffafbe1ce392
```

## 🧪 Test de l'intégration

### Test 1: Sélection d'agent

1. Ouvrir Bolt.DIY: http://localhost:5173
2. Cliquer sur le sélecteur "Select BMAD Agent"
3. Vérifier que 19 agents apparaissent avec icônes et descriptions
4. Sélectionner "Winston - Architect"
5. Vérifier que le nom s'affiche dans le bouton

### Test 2: Conversation avec agent BMAD

1. Avec Winston sélectionné, envoyer: "Je veux créer une app de chat temps réel"
2. Vérifier que la réponse vient de Winston avec son style architectural
3. Continuer la conversation sur plusieurs messages
4. Changer d'agent (ex: Amelia - Developer)
5. Vérifier que le style de réponse change

### Test 3: Création automatique de projet

1. Avoir une conversation de 5+ messages sur un projet
2. Le bouton "Créer projet Archon" devrait apparaître
3. Cliquer sur le bouton
4. Vérifier:
   - Notification de succès
   - Project ID affiché
   - Lien "Voir dans Archon" fonctionne
   - Projet créé dans backend Archon

### Test 4: Mode hybride

1. Démarrer avec agent BMAD (Winston)
2. Cliquer sur "No Agent (Bolt Default)"
3. Vérifier que les messages suivants utilisent Bolt
4. Re-sélectionner un agent BMAD
5. Vérifier retour au mode BMAD

## 📊 Workflow complet utilisateur

```
1. Utilisateur ouvre Bolt.DIY
   ↓
2. Sélectionne "Winston - Architect" dans dropdown
   ↓
3. "Je veux créer une plateforme e-learning"
   ↓
4. Winston répond avec architecture proposée
   ↓
5. Continue conversation avec différents agents
   (Product Manager, Developer, etc.)
   ↓
6. Après 5+ messages → Bouton "Créer projet Archon" apparaît
   ↓
7. Clic sur bouton
   ↓
8. Backend analyse conversation
   ↓
9. Crée projet dans Archon avec:
   - Métadonnées (nom, technologies)
   - Knowledge base depuis transcript
   - Context technique
   ↓
10. Notification succès avec liens
   ↓
11. Peut continuer à coder dans Bolt avec contexte projet
```

## 🎨 Personnalisation UI

### Couleurs par catégorie d'agent

Les catégories utilisent ces couleurs:

- **Strategic** (CEO, Product Manager, etc.): Purple
- **Technical** (Architect, Developer, etc.): Blue
- **Operational** (QA, DevOps, etc.): Green
- **Specialized** (Security, ML, etc.): Orange

### Icons personnalisés

Modifiez dans `AgentSelector.tsx` pour utiliser vos propres icônes:

```typescript
<span className="text-2xl">{agent.icon || '🤖'}</span>
```

## 🚀 Prochaines améliorations possibles

1. **Streaming responses** pour les agents BMAD
2. **Context window management** pour longues conversations
3. **Agent auto-selection** basée sur le contenu du message
4. **Multi-agent orchestration** automatique
5. **RAG search** intégré dans les réponses agents
6. **Project templates** basés sur conversations types
7. **Export conversation** vers Markdown/JSON
8. **Collaborative sessions** multi-utilisateurs

## 📄 Fichiers créés

```
bolt-diy/
├── app/
│   ├── components/
│   │   └── chat/
│   │       ├── AgentSelector.tsx              ✅ Nouveau
│   │       └── CreateArchonProjectButton.tsx  ✅ Nouveau
│   └── lib/
│       └── bmad-client.ts                     ✅ Nouveau
└── .env.local                                 ✅ Configuré
```

## ✅ Checklist intégration

- [x] Créer AgentSelector.tsx
- [x] Créer bmad-client.ts
- [x] Créer CreateArchonProjectButton.tsx
- [ ] Modifier BaseChat.tsx (imports)
- [ ] Ajouter state management
- [ ] Modifier handleSendMessage
- [ ] Ajouter composants dans UI
- [ ] Tester sélection agent
- [ ] Tester conversation BMAD
- [ ] Tester création projet
- [ ] Vérifier liens Archon

## 🔗 Ressources

- Backend coordination: http://localhost:8180/api/coordination/health
- Agents BMAD: http://localhost:8180/api/bmad/agents
- Archon MCP: http://localhost:8051
- Bolt.DIY: http://localhost:5173

---

**Status**: Composants créés ✅ | Intégration BaseChat ⏳ | Tests ⏳
