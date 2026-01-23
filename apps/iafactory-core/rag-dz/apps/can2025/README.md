# 🏆 CAN 2025 - Application de Suivi

Application web pour suivre la Coupe d'Afrique des Nations 2025 au Maroc, avec un focus particulier sur l'équipe d'Algérie 🇩🇿.

## 🌟 Fonctionnalités

### ✅ Phase 1 - MVP (Terminé)

- ✅ **Countdown en temps réel** jusqu'au début de la CAN et au 1er match de l'Algérie
- ✅ **Hub Algérie complet**: Matchs, effectif, palmarès, statistiques
- ✅ **6 Groupes**: Classements détaillés pour tous les groupes (A-F)
- ✅ **Calendrier complet**: Tous les matchs de la phase de groupes
- ✅ **Design responsive**: Mobile-first, dark mode natif
- ✅ **Données complètes**: 24 équipes, tous les matchs, stades

### 🚧 Phase 2 - À venir

- [ ] Scores en temps réel (API à connecter)
- [ ] PWA avec notifications push
- [ ] Mode offline
- [ ] Partage social (matchs, résultats)
- [ ] Statistiques avancées (possession, tirs, cartons)
- [ ] Prédictions communautaires

## 🚀 Démarrage Rapide

### Installation

```bash
cd D:\IAFactory\rag-dz\apps\can2025

# Installer les dépendances
npm install

# Copier le fichier d'environnement
copy .env.local.example .env.local

# Lancer en développement
npm run dev
```

L'app sera accessible sur **http://localhost:3002**

### Build Production

```bash
npm run build
npm start
```

## 📁 Structure du Projet

```
can2025/
├── app/
│   ├── page.tsx                 # Homepage (Countdown + Matchs Algérie)
│   ├── algerie/page.tsx         # Hub Algérie complet
│   ├── groupes/page.tsx         # Tous les groupes & classements
│   ├── calendrier/page.tsx      # Calendrier complet
│   ├── components/
│   │   └── Countdown.tsx        # Composant countdown temps réel
│   ├── layout.tsx               # Layout global (header, footer)
│   └── globals.css              # Styles globaux
├── data/
│   └── can2025-data.ts          # Données CAN (équipes, matchs, groupes)
├── public/                      # Assets statiques
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── README.md
```

## 🎨 Design System

### Couleurs Principales

- **Primary (Vert Algérie)**: `#007A3D`
- **Secondary (Rouge Algérie)**: `#CE1126`
- **Accent (Or Trophée)**: `#FFD700`

### Composants

- **Cards**: Style uniformisé avec `.card`, `.card-hover`
- **Buttons**: `.btn-primary`, `.btn-secondary`, `.btn-outline`
- **Badges**: `.badge-primary`, `.badge-secondary`, `.badge-accent`
- **Countdown**: Composant animé avec mise à jour chaque seconde

## 📊 Données

### Source des Données

Actuellement, toutes les données sont **statiques** et définies dans `data/can2025-data.ts`:

- 24 équipes avec drapeaux, groupes
- 3 matchs de l'Algérie (phase de groupes)
- Calendrier complet des matchs
- Effectif Algérie (coach, joueurs clés)
- Palmarès historique

### Intégration Future

Pour la Phase 2, prévoir intégration avec:
- API scores en temps réel (à définir)
- Base de données pour classements dynamiques
- WebSocket pour live updates

## 🇩🇿 Focus Algérie

### Groupe E

L'Algérie est dans le **Groupe E** avec:
- 🇧🇫 Burkina Faso
- 🇬🇶 Guinée équatoriale
- 🇸🇩 Soudan

### Matchs de l'Algérie

1. **24 décembre 2025, 17:00** - Algérie vs Guinée équatoriale (Rabat)
2. **28 décembre 2025, 20:00** - Algérie vs Burkina Faso (Rabat)
3. **31 décembre 2025, 20:00** - Algérie vs Soudan (Rabat)

### Objectif

🏆 **3ème étoile** - L'Algérie vise un troisième titre après 1990 et 2019!

## 🛠️ Technologies

- **Next.js 14** (App Router)
- **React 18**
- **TypeScript**
- **Tailwind CSS**
- **date-fns** (manipulation dates)

## 📱 PWA (Phase 2)

La version PWA permettra:
- Installation sur mobile/desktop
- Notifications push pour les matchs de l'Algérie
- Mode offline
- Icône sur l'écran d'accueil

Configuration à venir dans `manifest.json` et `next.config.js`.

## 📈 Roadmap

### Phase 1 ✅ (Terminée - 15 Dec 2025)
- MVP avec toutes les pages essentielles
- Design complet et responsive
- Countdown fonctionnel
- Données statiques complètes

### Phase 2 🚧 (Avant 21 Dec 2025)
- [ ] Scores en temps réel
- [ ] PWA + notifications
- [ ] Tests E2E
- [ ] Déploiement VPS

### Phase 3 (Janvier 2026)
- [ ] Statistiques avancées
- [ ] Mode prédictions
- [ ] Partage social
- [ ] Historique matchs

## 🚀 Déploiement

### VPS/Production

```bash
# Build
npm run build

# Lancer avec PM2
pm2 start npm --name "can2025" -- start

# Nginx config (proxy port 3002)
# Voir fichier nginx.conf dans le repo
```

### Variables d'environnement

Aucune clé API requise pour la version MVP!

## 🎯 Métriques à Tracker

- Visiteurs uniques/jour
- Pages vues par session
- Taux de rebond
- Device breakdown (mobile/desktop)
- Pages les plus visitées

## 🤝 Contribution

Pour ajouter des données ou corriger des bugs:

1. Modifier `data/can2025-data.ts`
2. Tester localement avec `npm run dev`
3. Vérifier responsive + dark mode
4. Créer une PR

## 📄 Licence

© 2025 IA Factory - Made with ❤️ in Algeria 🇩🇿

---

## 🔥 Allez Les Fennecs! 🦊🇩🇿
