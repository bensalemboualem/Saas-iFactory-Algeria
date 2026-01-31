# Configuration de PostgreSQL pour Gateway

## Option 1: Exécution Manuelle (Recommandé)

### 1. Ouvrir pgAdmin ou psql

Si vous utilisez **pgAdmin**:
1. Connectez-vous à votre serveur PostgreSQL
2. Faites un clic droit sur "Databases" → Create → Database
3. Nom: `iafactory_gateway`
4. Owner: `postgres`
5. Cliquez sur "Save"

Si vous utilisez **psql** (dans CMD ou PowerShell):
```powershell
# Trouvez le chemin de psql (généralement dans C:\Program Files\PostgreSQL\XX\bin)
# Ajoutez-le au PATH ou utilisez le chemin complet

# Exemple:
cd "C:\Program Files\PostgreSQL\16\bin"

# Créer la base de données
.\psql -U postgres -c "CREATE DATABASE iafactory_gateway;"
```

### 2. Mettre à jour les credentials dans .env

Ouvrez `apps/gateway/.env` et vérifiez la ligne DATABASE_URL:

```env
# Si vous utilisez l'utilisateur postgres par défaut:
DATABASE_URL=postgresql://postgres:VOTRE_MOT_DE_PASSE@localhost:5432/iafactory_gateway?schema=public

# Remplacez VOTRE_MOT_DE_PASSE par le mot de passe que vous avez défini lors de l'installation de PostgreSQL
```

### 3. Appliquer les migrations Prisma

```powershell
cd apps/gateway
pnpm db:push
pnpm db:seed
```

## Option 2: Utilisation de SQLite (Alternative Simple)

Si vous voulez éviter PostgreSQL pour le développement local:

### 1. Modifier le schema Prisma

Ouvrez `apps/gateway/prisma/schema.prisma` et changez:

```prisma
datasource db {
  provider = "sqlite"
  url      = "file:./dev.db"
}
```

### 2. Mettre à jour .env

```env
DATABASE_URL="file:./dev.db"
```

### 3. Regénérer Prisma

```powershell
pnpm db:generate
pnpm db:push
pnpm db:seed
```

## Vérification

Une fois configuré, redémarrez le Gateway:

```powershell
pnpm dev
```

Vous ne devriez plus voir d'erreurs de base de données ! ✅
