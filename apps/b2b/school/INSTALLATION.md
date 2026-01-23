# OneStSchooled - Guide d'Installation XAMPP

## Installation Automatique (RECOMMANDÉ)

### Étape 1: Configuration initiale

1. **Faites un clic droit** sur le fichier `setup-laravel-xampp.bat`
2. Sélectionnez **"Exécuter en tant qu'administrateur"**
3. Le script va automatiquement:
   - Configurer Apache Virtual Host
   - Modifier le fichier hosts Windows
   - Redémarrer Apache

### Étape 2: Démarrer le projet

Double-cliquez simplement sur **`start-project.bat`** (pas besoin de droits admin)

Le script va:
- Vérifier qu'Apache et MySQL sont démarrés
- Les démarrer automatiquement si nécessaire
- Ouvrir votre navigateur sur http://onestschooled.local

---

## Accès à l'application

Une fois configuré, votre application sera accessible à:

- **URL principale**: http://onestschooled.local
- **URL alternative**: http://www.onestschooled.local
- **XAMPP par défaut**: http://localhost

---

## Configuration Base de Données

Assurez-vous que votre fichier `.env` contient:

```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=votre_base_de_donnees
DB_USERNAME=root
DB_PASSWORD=
```

---

## Commandes Laravel Utiles

### Depuis le terminal XAMPP Shell:

```bash
cd /c/xampp/htdocs/onestschooled-test

# Migrations
php artisan migrate

# Seed
php artisan db:seed

# Cache
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear

# Créer un lien symbolique pour le storage
php artisan storage:link
```

---

## Dépannage

### Le site ne s'affiche pas

1. Vérifiez qu'Apache est démarré dans XAMPP Control Panel
2. Vérifiez que le fichier hosts contient bien:
   ```
   127.0.0.1 onestschooled.local
   ```
3. Essayez d'accéder à http://localhost pour vérifier qu'Apache fonctionne

### Erreur 403 Forbidden

Vérifiez les permissions du dossier `public/`:
```bash
chmod -R 755 /c/xampp/htdocs/onestschooled-test/public
```

### Erreur 500

Vérifiez les permissions de `storage/` et `bootstrap/cache/`:
```bash
chmod -R 775 /c/xampp/htdocs/onestschooled-test/storage
chmod -R 775 /c/xampp/htdocs/onestschooled-test/bootstrap/cache
```

---

## Installation Manuelle (Alternative)

Si vous préférez configurer manuellement:

### 1. Configurer Apache Virtual Host

Éditez `C:\xampp\apache\conf\extra\httpd-vhosts.conf` et ajoutez:

```apache
<VirtualHost *:80>
    ServerAdmin admin@onestschooled.local
    DocumentRoot "C:/xampp/htdocs/onestschooled-test/public"
    ServerName onestschooled.local
    ServerAlias www.onestschooled.local

    <Directory "C:/xampp/htdocs/onestschooled-test/public">
        Options Indexes FollowSymLinks MultiViews
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog "logs/onestschooled-error.log"
    CustomLog "logs/onestschooled-access.log" common
</VirtualHost>
```

### 2. Activer les Virtual Hosts

Éditez `C:\xampp\apache\conf\httpd.conf` et décommentez:

```apache
Include conf/extra/httpd-vhosts.conf
```

### 3. Modifier le fichier hosts

Éditez `C:\Windows\System32\drivers\etc\hosts` (en tant qu'administrateur) et ajoutez:

```
127.0.0.1 onestschooled.local
127.0.0.1 www.onestschooled.local
```

### 4. Redémarrer Apache

Dans XAMPP Control Panel, cliquez sur "Stop" puis "Start" pour Apache.

---

## Notes Importantes

- **Plus besoin de `php artisan serve`** - Apache gère tout!
- Les fichiers de logs sont dans `C:\xampp\apache\logs\`
- En cas de problème, consultez `C:\xampp\apache\logs\onestschooled-error.log`

---

## Support

Pour toute question ou problème:
1. Vérifiez les logs d'erreur Apache
2. Assurez-vous que tous les services XAMPP sont démarrés
3. Vérifiez que le fichier `.env` est correctement configuré
