# Dzir IA Video Studio Pro

Plateforme professionnelle de création vidéo IA avec 10 générateurs premium.

## 🚀 Fonctionnalités

- **Dashboard** - Vue d'ensemble avec statistiques et métriques
- **Studio** - Workflow de création en 5 étapes
  1. Sélection du générateur IA
  2. Configuration du prompt
  3. Paramètres avancés (durée, style, ratio)
  4. Génération avec suivi de progression
  5. Téléchargement du résultat
- **Bibliothèque** - Gestion de vos vidéos générées
- **Templates** - Modèles prédéfinis par catégorie
- **Analytics** - Statistiques d'utilisation détaillées
- **Settings** - Configuration complète

## 🎨 Générateurs Disponibles

### Premium (Haute qualité)
- **Runway Gen-4** - 95/100 qualité • 4K • 15s max
- **Luma AI Dream Machine** - 92/100 qualité • 1080p • 10s max

### Standard (Bon rapport qualité/prix)
- **Kling AI Pro** - 90/100 qualité • 1080p • 8s max
- **Alibaba Qwen Video** - 85/100 qualité • 1080p • 6s max

### Gratuit (Quotas journaliers)
- **Hailuo AI 2.3** - 88/100 qualité • 1080p • 10s • 30 vidéos/jour
- **Nano AI** - 72/100 qualité • 720p • 5s • 50 vidéos/jour

Et 4 autres générateurs : Pika Labs, Fal.ai, Stability AI, Together AI...

## 🛠️ Stack Technique

- **Frontend** : Next.js 14 (App Router) + TypeScript
- **UI** : shadcn/ui + Tailwind CSS v4
- **Icons** : Lucide React
- **Backend API** : FastAPI (dzirvideo)
- **Deployment** : Vercel / VPS Hetzner

## 📦 Installation

```bash
# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev

# Builder pour production
npm run build

# Lancer en production
npm start
```

Le serveur de développement sera accessible sur [http://localhost:3000](http://localhost:3000).

## 🌐 Configuration

Créer un fichier `.env.local` :

```env
NEXT_PUBLIC_API_URL=https://www.iafactoryalgeria.com/dzirvideo
```

Pour le développement local avec API backend locale :

```env
NEXT_PUBLIC_API_URL=http://localhost:9200
```

## 📁 Structure du Projet

```
video-studio/
├── app/
│   ├── layout.tsx           # Layout principal avec sidebar
│   ├── page.tsx             # Dashboard (page d'accueil)
│   ├── studio/              # Workflow de création
│   ├── library/             # Bibliothèque vidéos
│   ├── templates/           # Templates prédéfinis
│   ├── analytics/           # Statistiques
│   └── settings/            # Paramètres
├── components/
│   ├── ui/                  # Composants shadcn/ui
│   ├── app-sidebar.tsx      # Navigation latérale
│   └── app-header.tsx       # En-tête avec user menu
├── lib/
│   ├── utils.ts             # Utilitaires (cn)
│   └── api.ts               # Client API dzirvideo
└── public/                  # Assets statiques
```

## 🎨 Thème IAFactory

Le projet utilise les couleurs de marque IAFactory :

- **Primary** : Bleu IAFactory `oklch(0.6 0.15 250)`
- **Accent** : Vert IAFactory `oklch(0.55 0.15 150)`
- **Charts** : Palette coordonnée pour les graphiques

## 🔌 Intégration API

Le client API est disponible via `lib/api.ts` :

```typescript
import api from '@/lib/api'

// Lister les générateurs
const generators = await api.listGenerators()

// Générer une vidéo
const result = await api.generateVideo({
  generator_name: "RunwayGen4Generator",
  prompt: "Beautiful sunset over mountains",
  duration_seconds: 10
})

// Vérifier le statut
const status = await api.checkStatus(result.task_id)
```

## 📊 Quotas

- **6,100+ vidéos gratuites/jour** (total tous générateurs)
- **5,000+ images/jour** (Stability AI, Replicate, etc.)
- **Qualité moyenne** : 85/100
- **Temps moyen** : 90s par vidéo

## 🚀 Déploiement

### Vercel (Recommandé pour le frontend)

```bash
vercel deploy
```

### VPS (Production)

```bash
# Build
npm run build

# Déployer avec rsync
rsync -avz --delete .next/ user@vps:/var/www/video-studio/.next/
rsync -avz public/ user@vps:/var/www/video-studio/public/

# Restart PM2
pm2 restart video-studio
```

## 📝 Checklist

- [x] Layout avec sidebar navigation
- [x] Dashboard avec stats
- [x] Studio workflow 5 étapes
- [x] Bibliothèque vidéos
- [x] Templates par catégorie
- [x] Analytics & graphiques
- [x] Settings multi-tabs
- [x] Client API intégré
- [ ] Authentification utilisateur
- [ ] Real-time progress tracking (WebSocket)
- [ ] Upload de vidéos personnalisées
- [ ] Animations Framer Motion
- [ ] Tests E2E
- [ ] Responsive mobile optimisé

## 🤝 Support

- **Backend API** : https://www.iafactoryalgeria.com/dzirvideo/docs
- **Documentation** : https://www.iafactoryalgeria.com/dzirvideo/redoc
- **Contact** : contact@iafactory.pro

---

**Développé par IAFactory Algeria** 🇩🇿
