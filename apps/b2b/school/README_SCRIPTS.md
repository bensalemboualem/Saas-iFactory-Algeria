# 🚀 SCRIPTS DE DÉMARRAGE AUTOMATIQUE - BBC SCHOOL ALGERIA

## 📁 FICHIERS CRÉÉS

### ✅ Scripts Principaux

1. **START_ONESTSCHOOL.bat**
   - Démarre Apache + MySQL
   - Nettoie les caches automatiquement
   - Ouvre le navigateur sur la page de connexion
   - 📍 Emplacement: `C:\xampp\htdocs\onestschooled-test\`

2. **STOP_ONESTSCHOOL.bat**
   - Arrête Apache et MySQL proprement
   - 📍 Emplacement: `C:\xampp\htdocs\onestschooled-test\`

3. **RESTART_ONESTSCHOOL.bat**
   - Redémarre tout (arrêt + démarrage)
   - 📍 Emplacement: `C:\xampp\htdocs\onestschooled-test\`

4. **BBC School - DEMARRER.bat**
   - Raccourci créé sur votre BUREAU
   - Double-clic pour tout démarrer
   - 📍 Emplacement: `Bureau Windows`

5. **DEMARRAGE_AUTO_WINDOWS.bat**
   - Configure le démarrage automatique au boot de Windows
   - 📍 Emplacement: `C:\xampp\htdocs\onestschooled-test\`

---

## 🎯 UTILISATION

### Pour Démarrer BBC School (OPTION 1)
**Double-cliquez sur le fichier sur votre Bureau:**
```
BBC School - DEMARRER.bat
```

### Pour Démarrer BBC School (OPTION 2)
**Dans le dossier du projet:**
```
C:\xampp\htdocs\onestschooled-test\START_ONESTSCHOOL.bat
```

### Pour Arrêter BBC School
```
C:\xampp\htdocs\onestschooled-test\STOP_ONESTSCHOOL.bat
```

### Pour Redémarrer BBC School
```
C:\xampp\htdocs\onestschooled-test\RESTART_ONESTSCHOOL.bat
```

### Pour Configurer le Démarrage Automatique au Boot Windows
```
C:\xampp\htdocs\onestschooled-test\DEMARRAGE_AUTO_WINDOWS.bat
```
Choisissez "O" pour activer le démarrage automatique.

---

## ⚙️ CE QUE FAIT LE SCRIPT DE DÉMARRAGE

1. ✅ Démarre Apache (serveur web)
2. ✅ Démarre MySQL (base de données)
3. ✅ Nettoie les caches Laravel (views, config, routes)
4. ✅ Vérifie que la base de données est accessible
5. ✅ Ouvre automatiquement le navigateur sur la page de connexion

**TEMPS TOTAL:** ~10 secondes

---

## 🎨 PERSONNALISATION

### Changer l'URL d'ouverture automatique
Éditez `START_ONESTSCHOOL.bat`, ligne 62:
```batch
start http://localhost/onestschooled-test/public/login
```

Remplacez par:
- `/dashboard` - Pour ouvrir directement le dashboard
- `/home` - Pour ouvrir le site public

---

## 🔧 DÉPANNAGE

### Si Apache ne démarre pas
1. Vérifiez qu'aucun autre programme n'utilise le port 80 (Skype, IIS, etc.)
2. Fermez XAMPP Control Panel s'il est ouvert
3. Exécutez le script en tant qu'Administrateur (clic droit → "Exécuter en tant qu'administrateur")

### Si MySQL ne démarre pas
1. Vérifiez qu'aucun autre MySQL n'est en cours d'exécution
2. Redémarrez Windows
3. Exécutez le script en tant qu'Administrateur

### Si le navigateur n'ouvre pas la bonne page
Patientez 5-10 secondes que les services démarrent complètement, puis actualisez la page.

---

## 🎯 AVANT LA PRÉSENTATION

**Exécutez ce script 5 minutes avant:**
```
RESTART_ONESTSCHOOL.bat
```

Cela garantit que tout est frais et fonctionne parfaitement.

---

## 📝 NOTES

- Les scripts sont silencieux (pas de fenêtres qui clignotent)
- Les caches sont automatiquement nettoyés à chaque démarrage
- Les services s'arrêtent proprement (pas de corruption de données)
- Compatible Windows 10/11

---

**Créé pour BBC School Algeria - Présentation Professionnelle** 🏫
