# OneStSchooled - Système de Gestion Scolaire

**Version:** 2.0.0
**Basé sur:** BBC School Algeria
**Dernière mise à jour:** Décembre 2024

---

## Vue d'ensemble

OneStSchooled est un système complet de gestion scolaire conçu pour les établissements éducatifs algériens. Il offre une solution complète pour la gestion des étudiants, des enseignants, des cours, des examens et des communications avec les parents.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ONESTSCHOOLED PLATFORM                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │   ADMIN PANEL   │  │  TEACHER PORTAL │  │  PARENT PORTAL  │              │
│  │   ───────────   │  │   ───────────   │  │   ───────────   │              │
│  │ Configuration   │  │ Classes         │  │ Suivi enfants   │              │
│  │ Utilisateurs    │  │ Notes           │  │ Paiements       │              │
│  │ Rapports        │  │ Présences       │  │ Communications  │              │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘              │
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │ STUDENT PORTAL  │  │   ACCOUNTING    │  │   TRANSPORT     │              │
│  │   ───────────   │  │   ───────────   │  │   ───────────   │              │
│  │ Emploi du temps │  │ Frais scolarité │  │ Suivi véhicules │              │
│  │ Notes           │  │ Paiements       │  │ Trajets         │              │
│  │ Devoirs         │  │ Facturation     │  │ Notifications   │              │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Fonctionnalités Principales

### Gestion Académique
- **Étudiants:** Inscription, profils, historique académique
- **Enseignants:** Affectations, emplois du temps, évaluations
- **Classes:** Organisation par niveau, sections, groupes
- **Cours:** Matières, programmes, ressources pédagogiques
- **Examens:** Planification, notation, bulletins

### Gestion Administrative
- **Utilisateurs:** Rôles et permissions personnalisables
- **Présences:** Suivi quotidien, rapports d'absentéisme
- **Emplois du temps:** Génération automatique, conflits
- **Documents:** Certificats, attestations, bulletins

### Communication
- **Notifications:** SMS, Email, Push
- **Messagerie:** Interne entre parents/enseignants
- **Annonces:** Événements, réunions, informations

### Finances
- **Frais de scolarité:** Gestion des paiements
- **Facturation:** Génération automatique
- **Paiements:** Intégration Chargily (Algérie)
- **Rapports financiers:** Statistiques, exports

### Transport (Module optionnel)
- **Véhicules:** Gestion de flotte
- **Trajets:** Planification des itinéraires
- **Suivi GPS:** Localisation en temps réel
- **Notifications:** Alertes parents

---

## Stack Technologique

| Composant | Technologie | Version |
|-----------|-------------|---------|
| Backend | Laravel | 8.x+ |
| PHP | PHP | 7.4+ |
| Base de données | MySQL / PostgreSQL | 8.0 / 14 |
| Frontend | Blade Templates | - |
| CSS | Bootstrap | 4.x |
| JavaScript | jQuery | 3.x |
| Queue | Laravel Queue | - |
| Cache | Redis / File | - |

---

## Installation

### Prérequis

- PHP >= 7.4
- Composer
- MySQL >= 8.0 ou PostgreSQL >= 14
- Node.js >= 16 (pour les assets)
- Redis (optionnel, pour le cache)

### Installation Rapide

```bash
# Cloner le projet
git clone https://github.com/iafactory/onestschooled.git
cd onestschooled

# Installer les dépendances PHP
composer install

# Installer les dépendances JS
npm install
npm run dev

# Configurer l'environnement
cp .env.example .env
php artisan key:generate

# Éditer .env avec vos paramètres
nano .env
```

### Configuration Mode Single School

Pour une seule école (sans multi-tenant):

```bash
# Dans .env
APP_SAAS=false
CACHE_DRIVER=array

# Exécuter les migrations
php artisan migrate:fresh --seed --path=database/migrations/tenant
```

### Configuration Mode SaaS (Multi-Écoles)

Pour héberger plusieurs écoles:

```bash
# Dans .env
APP_SAAS=true
APP_MAIN_APP_URL=school-management.test

# Exécuter les migrations
php artisan migrate:fresh --path=modules/MainApp/database/migrations
php artisan module:seed MainApp
```

---

## Modules Disponibles

| Module | Description | Statut |
|--------|-------------|--------|
| MainApp | Module principal de gestion scolaire | Actif |
| VehicleTracker | Suivi des véhicules scolaires | Optionnel |
| Chargily | Paiements en ligne (Algérie) | Optionnel |
| SMS | Notifications SMS | Optionnel |

### Activer un Module

```bash
# 1. Modifier modules_statuses.json
{
    "MainApp": true,
    "VehicleTracker": true  # Changer false en true
}

# 2. Exécuter les migrations du module
php artisan module:migrate VehicleTracker
php artisan module:seed VehicleTracker
```

---

## Structure du Projet

```
onestschooled/
├── app/                      # Application Laravel
│   ├── Http/
│   │   ├── Controllers/     # Contrôleurs
│   │   ├── Middleware/      # Middleware
│   │   └── Requests/        # Form Requests
│   ├── Models/              # Modèles Eloquent
│   ├── Services/            # Services métier
│   └── Providers/           # Service Providers
│
├── Modules/                  # Modules nWidart
│   ├── MainApp/             # Module principal
│   │   ├── Config/
│   │   ├── Database/
│   │   ├── Http/
│   │   ├── Models/
│   │   ├── Resources/
│   │   └── Routes/
│   └── VehicleTracker/      # Module transport
│
├── config/                   # Configuration Laravel
├── database/
│   ├── migrations/          # Migrations générales
│   │   └── tenant/          # Migrations single-school
│   ├── seeders/             # Seeders
│   └── factories/           # Factories
│
├── resources/
│   ├── views/               # Vues Blade
│   ├── lang/                # Traductions (FR, AR, EN)
│   └── assets/              # Assets source
│
├── routes/
│   ├── web.php              # Routes web
│   └── api.php              # Routes API
│
├── public/                   # Assets publics
├── storage/                  # Fichiers uploadés
└── tests/                    # Tests
```

---

## Configuration des Langues

Le système supporte le multilingue avec support RTL pour l'arabe.

### Langues Disponibles

| Langue | Code | Direction |
|--------|------|-----------|
| Français | fr | LTR |
| Arabe | ar | RTL |
| Darija (Algérien) | dz | RTL |
| Anglais | en | LTR |

### Configurer la Langue par Défaut

```php
// config/app.php
'locale' => 'fr',
'fallback_locale' => 'en',

// Langues disponibles
'available_locales' => ['fr', 'ar', 'en', 'dz'],
```

### Forcer l'Arabe à 100%

Voir le document [ARABE_100_POURCENT.md](./docs/documentation/ARABE_100_POURCENT.md) pour une configuration complète en arabe.

---

## Rôles et Permissions

| Rôle | Description | Permissions |
|------|-------------|-------------|
| Super Admin | Administrateur système | Toutes |
| Admin École | Directeur/Administrateur | Gestion école |
| Enseignant | Professeur | Cours, Notes, Présences |
| Étudiant | Élève | Consultation, Devoirs |
| Parent | Tuteur | Suivi enfants, Paiements |
| Comptable | Finances | Paiements, Factures |
| Chauffeur | Transport | Trajets (si module actif) |

---

## API REST

L'application expose une API REST pour les intégrations mobiles.

### Authentification

```http
POST /api/login
Content-Type: application/json

{
    "email": "user@school.dz",
    "password": "password"
}
```

### Endpoints Principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | /api/students | Liste des étudiants |
| GET | /api/students/{id} | Détail étudiant |
| GET | /api/classes | Liste des classes |
| GET | /api/schedule/{class_id} | Emploi du temps |
| GET | /api/grades/{student_id} | Notes de l'étudiant |
| GET | /api/attendance/{class_id} | Présences |
| POST | /api/payments | Enregistrer un paiement |

---

## Paiements avec Chargily

Intégration native avec Chargily pour les paiements en Algérie.

### Configuration

```bash
# Dans .env
CHARGILY_APP_KEY=your-app-key
CHARGILY_APP_SECRET=your-app-secret
CHARGILY_MODE=live  # ou test
```

### Utilisation

```php
// Créer un paiement
$payment = Chargily::createPayment([
    'amount' => 5000,  // en centimes (50.00 DZD)
    'currency' => 'DZD',
    'description' => 'Frais de scolarité - Trimestre 1',
    'back_url' => route('payment.callback'),
    'webhook_url' => route('payment.webhook'),
]);
```

---

## Commandes Artisan Utiles

```bash
# Migrations
php artisan migrate                    # Appliquer les migrations
php artisan migrate:fresh --seed       # Reset + seed
php artisan module:migrate MainApp     # Migration d'un module

# Cache
php artisan cache:clear               # Vider le cache
php artisan config:clear              # Vider le cache config
php artisan view:clear                # Vider le cache des vues

# Modules
php artisan module:list               # Lister les modules
php artisan module:enable ModuleName  # Activer un module
php artisan module:disable ModuleName # Désactiver un module

# Génération
php artisan make:model ModelName -m   # Créer model + migration
php artisan make:controller Name      # Créer un contrôleur
```

---

## Environnements

### Développement

```bash
APP_ENV=local
APP_DEBUG=true
LOG_LEVEL=debug
```

### Production

```bash
APP_ENV=production
APP_DEBUG=false
LOG_LEVEL=error

# Optimisations
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

---

## Tests

```bash
# Tous les tests
php artisan test

# Tests spécifiques
php artisan test --filter=StudentTest

# Avec couverture
php artisan test --coverage
```

---

## Sauvegarde

```bash
# Backup base de données
php artisan backup:run

# Backup uniquement la DB
php artisan backup:run --only-db

# Lister les backups
php artisan backup:list
```

---

## Troubleshooting

### Erreurs Communes

| Erreur | Solution |
|--------|----------|
| SQLSTATE[HY000] | Vérifier les credentials DB dans .env |
| Class not found | Exécuter `composer dump-autoload` |
| View not found | Exécuter `php artisan view:clear` |
| Permission denied | `chmod -R 775 storage bootstrap/cache` |

### Logs

```bash
# Voir les logs Laravel
tail -f storage/logs/laravel.log

# Vider les logs
truncate -s 0 storage/logs/laravel.log
```

---

## Documentation Complémentaire

- [Installation détaillée](./docs/installation.md)
- [Configuration des modules](./docs/modules.md)
- [API Reference](./docs/api.md)
- [Guide utilisateur](./docs/user-guide.md)
- [Configuration Arabe](./docs/documentation/ARABE_100_POURCENT.md)
- [Base de connaissances Chatbot](./docs/documentation/BASE_CONNAISSANCES_CHATBOT.md)

---

## Support

- **Email:** support@iafactory.dz
- **Documentation:** [docs.iafactory.dz/onestschooled](https://docs.iafactory.dz/onestschooled)
- **Issues:** GitHub Issues

---

## Licence

Copyright (c) 2024 IAFactory. Tous droits réservés.
