# 🚀 OneStSchooled - Carte de Référence Rapide

## ⚡ Démarrage Quotidien

### Option 1: Ultra Rapide (Recommandé)
```
Double-clic sur: start-project.bat
```
**C'est tout!** Le script fait tout automatiquement.

### Option 2: Manuelle
1. Ouvrir **XAMPP Control Panel**
2. Start **Apache** + **MySQL**
3. Naviguer vers: **http://onestschooled.local**

---

## 🌐 URLs du Projet

| Type | URL |
|------|-----|
| **Application principale** | http://onestschooled.local |
| **Alternative** | http://www.onestschooled.local |
| **XAMPP Dashboard** | http://localhost |
| **phpMyAdmin** | http://localhost/phpmyadmin |

---

## 📂 Chemins Importants

| Description | Chemin |
|-------------|--------|
| **Projet Laravel** | `C:\xampp\htdocs\onestschooled-test\` |
| **Logs Apache** | `C:\xampp\apache\logs\` |
| **Logs du projet** | `C:\xampp\apache\logs\onestschooled-error.log` |
| **Config Apache** | `C:\xampp\apache\conf\extra\httpd-vhosts.conf` |
| **Fichier hosts** | `C:\Windows\System32\drivers\etc\hosts` |

---

## 🔧 Commandes Laravel Essentielles

### Navigation
```bash
cd /c/xampp/htdocs/onestschooled-test
```

### Base de Données
```bash
php artisan migrate              # Exécuter les migrations
php artisan migrate:fresh        # Reset + migrations
php artisan migrate:fresh --seed # Reset + migrations + seed
php artisan db:seed              # Peupler la base
```

### Cache
```bash
php artisan cache:clear    # Vider le cache application
php artisan config:clear   # Vider le cache config
php artisan route:clear    # Vider le cache routes
php artisan view:clear     # Vider le cache views
php artisan optimize:clear # Tout vider
```

### Autres
```bash
php artisan key:generate     # Générer APP_KEY
php artisan storage:link     # Lien symbolique storage
php artisan list             # Liste toutes les commandes
php artisan make:controller  # Créer un controller
php artisan make:model       # Créer un model
php artisan make:migration   # Créer une migration
```

---

## 🗄️ Configuration Base de Données

Fichier `.env`:
```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=votre_base_de_donnees
DB_USERNAME=root
DB_PASSWORD=
```

### Créer une nouvelle base de données:
1. Aller sur http://localhost/phpmyadmin
2. Cliquer sur "Nouvelle base de données"
3. Entrer le nom et créer
4. Mettre à jour `DB_DATABASE` dans `.env`
5. Exécuter `php artisan migrate`

---

## 🐛 Dépannage

### Le site ne charge pas
```bash
# 1. Vérifier qu'Apache tourne
tasklist | findstr httpd

# 2. Redémarrer Apache via XAMPP Control Panel
Stop → Start

# 3. Vérifier les logs
cat C:\xampp\apache\logs\onestschooled-error.log
```

### Erreur 403 Forbidden
```bash
# Vérifier les permissions
chmod -R 755 /c/xampp/htdocs/onestschooled-test/public
```

### Erreur 500
```bash
# Vérifier les permissions storage
chmod -R 775 /c/xampp/htdocs/onestschooled-test/storage
chmod -R 775 /c/xampp/htdocs/onestschooled-test/bootstrap/cache

# Vider les caches
php artisan optimize:clear
```

### Port déjà utilisé
```bash
# Trouver le processus qui utilise le port 80
netstat -ano | findstr :80

# Tuer le processus (remplacer PID)
taskkill /F /PID [numéro_du_processus]
```

### Laravel affiche une page blanche
```bash
# Activer le mode debug dans .env
APP_DEBUG=true

# Vérifier les logs Laravel
tail storage/logs/laravel.log
```

---

## ⚙️ Configuration Avancée

### Modifier le port d'Apache (si 80 est occupé)

1. Éditer `C:\xampp\apache\conf\httpd.conf`
2. Chercher: `Listen 80`
3. Remplacer par: `Listen 8080`
4. Éditer `C:\xampp\apache\conf\extra\httpd-vhosts.conf`
5. Remplacer `*:80` par `*:8080`
6. Redémarrer Apache
7. URL devient: http://onestschooled.local:8080

### Activer HTTPS (SSL)

Suivre le guide dans: `C:\xampp\apache\conf\extra\httpd-ssl.conf`

---

## 📚 Fichiers de Documentation

| Fichier | Description |
|---------|-------------|
| **DEMARRAGE-RAPIDE.txt** | Mémo simple en texte |
| **MEMO-DEMARRAGE.html** | Mémo visuel interactif |
| **INSTALLATION.md** | Guide d'installation complet |
| **CARTE-REFERENCE-RAPIDE.md** | Ce document |

---

## 🎯 Checklist Quotidienne

- [ ] Double-clic sur `start-project.bat` OU démarrer Apache/MySQL dans XAMPP
- [ ] Naviguer vers http://onestschooled.local
- [ ] Vérifier que la base de données est accessible
- [ ] Commencer à coder! 🎉

---

## ⚠️ À NE JAMAIS FAIRE

- ❌ **Ne jamais utiliser** `php artisan serve` (c'est Apache qui gère maintenant)
- ❌ **Ne jamais modifier** les fichiers dans `public/` directement
- ❌ **Ne jamais committer** le fichier `.env`
- ❌ **Ne jamais exposer** ce serveur sur Internet (XAMPP est pour le développement local uniquement)

---

## ✅ À TOUJOURS FAIRE

- ✅ Utiliser `start-project.bat` pour démarrer
- ✅ Vider les caches après modification de config
- ✅ Faire des migrations après modification de la base
- ✅ Vérifier les logs en cas d'erreur
- ✅ Sauvegarder régulièrement votre travail

---

## 📞 Aide Supplémentaire

- Documentation Laravel: https://laravel.com/docs
- Forum XAMPP: https://community.apachefriends.org
- Stack Overflow: https://stackoverflow.com/questions/tagged/laravel

---

**Dernière mise à jour:** 1 novembre 2025
**Version:** 1.0

*Imprimez cette page et gardez-la à portée de main!* 📄
