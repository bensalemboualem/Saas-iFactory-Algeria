# 🤖 BASE DE CONNAISSANCES - CHATBOT D'AIDE BBC SCHOOL ALGERIA

## 📚 INFORMATIONS GÉNÉRALES

### À propos de BBC School Algeria

**Nom complet:** Best Bridge for Creation School Algeria
**Type:** École privée
**Pays:** 🇩🇿 Algérie
**Système:** OnestSchool - Système de gestion scolaire

**Niveaux d'enseignement:**
- ✅ Maternelle
- ✅ Primaire
- ✅ Cycle Moyen (jusqu'à la 4ème année moyenne)
- ❌ PAS de Baccalauréat (l'école s'arrête au cycle moyen)

### Établissements

**3 établissements à Alger:**

1. **Direction Générale**
   - Adresse: Bouchaoui, Alger
   - Téléphone: +213 23 35 28 74
   - Email: info@bbcschool.net

2. **École Principale**
   - Adresse: Ain Benian, Alger
   - Téléphone: +213 23 35 28 75
   - Email: info@bbcschool.net

3. **Annexe Maternelle**
   - Adresse: Chéraga, Alger
   - Téléphone: +213 23 35 28 76
   - Email: info@bbcschool.net

---

## 🌍 CONFIGURATION DES LANGUES

### Langue Par Défaut

**🇩🇿 Arabe (العربية)**
- Langue par défaut pour TOUS les utilisateurs
- Direction: RTL (droite à gauche)
- Interface 100% en arabe
- Tous les modules traduits

### Langues Disponibles

1. **🇩🇿 العربية (Arabe)** - Par défaut
2. **🇫🇷 Français** - Langue secondaire
3. **🇬🇧 English** - Langue technique (non recommandée)

### Comment Changer de Langue?

**Pour l'utilisateur:**
1. Cliquer sur le menu **اللغة** (Langue) dans le dashboard
2. Sélectionner la langue souhaitée
3. La page se recharge automatiquement

**Pour réinitialiser la langue par défaut:**
```bash
"C:/xampp/php/php.exe" set_default_language.php
```

---

## 📊 MODULES DISPONIBLES

### Module Dashboard (لوحة التحكم)
**Fonctionnalités:**
- Vue d'ensemble des statistiques
- Compteurs: Étudiants, Parents, Enseignants, Sessions
- Graphiques de revenus et dépenses
- Événements à venir
- Présence du jour

### Module Student Info (معلومات الطالب)
**Fonctionnalités:**
- Liste des étudiants
- Admission en ligne
- Promotion des étudiants
- Gestion des étudiants désactivés
- Génération de cartes d'identité
- Génération de certificats

### Module Academic (الأكاديمي)
**Fonctionnalités:**
- Gestion des classes (الصف)
- Gestion des sections (القسم)
- Gestion des matières (المادة)
- Affectation des enseignants
- Configuration des salles de classe
- Horaires de classe

### Module Attendance (الحضور)
**Fonctionnalités:**
- Présence quotidienne
- Présence par matière
- Rapports de présence
- Statistiques d'absence

### Module Leave (الإجازة)
**Fonctionnalités:**
- Demandes de congé
- Types de congé
- Approbation des congés
- Liste des congés

### Module Fees (الرسوم)
**Fonctionnalités:**
- Groupes de frais
- Types de frais
- Affectation des frais
- Collecte des frais
- Rapports financiers

### Module Examination (الامتحان)
**Fonctionnalités:**
- Configuration des examens
- Horaires d'examen
- Registre des notes
- Niveaux de notes
- Examens en ligne

### Module Library (المكتبة)
**Fonctionnalités:**
- Gestion des livres
- Catégories de livres
- Membres de la bibliothèque
- Prêt de livres

### Module Accounts (الحسابات)
**Fonctionnalités:**
- Gestion des revenus
- Gestion des dépenses
- Rapports comptables
- Soldes

### Module Report (التقرير)
**Fonctionnalités:**
- Rapports étudiants
- Rapports de présence
- Rapports de frais
- Bulletins de notes
- Listes de mérite

### Module Staff (الموظفون)
**Fonctionnalités:**
- Liste du personnel
- Ajout de personnel
- Gestion des rôles
- Gestion des permissions

### Module Settings (الإعدادات)
**Fonctionnalités:**
- Paramètres généraux
- Paramètres email
- Paramètres SMS
- Configuration du site web
- Galerie photos
- Forum
- Chat en direct

---

## 🔧 PROBLÈMES COURANTS ET SOLUTIONS

### Problème: Interface en Anglais

**Symptômes:**
- Menu en anglais
- Modules en anglais
- Dashboard en anglais

**Solutions:**
1. Se déconnecter du dashboard
2. Se reconnecter
3. Recharger la page avec Ctrl+Shift+R

**Si le problème persiste:**
```bash
"C:/xampp/php/php.exe" set_default_language.php
"C:/xampp/php/php.exe" CLEAR_ALL_CACHES_FINAL.php
```

### Problème: Compteurs Affichent de Mauvais Chiffres

**Exemple:** 804 au lieu de 4

**Solution:**
Les compteurs ont été corrigés. Si le problème persiste:
1. Nettoyer les caches
2. Recharger la page

**Chiffres corrects:**
- Étudiants: 4
- Parents: 304
- Enseignants: 54
- Sessions: 22

### Problème: Direction du Texte Incorrecte

**Symptômes:**
- Texte de gauche à droite au lieu de droite à gauche
- Texte arabe mal aligné

**Solution:**
Vérifier que RTL est activé:
```bash
"C:/xampp/php/php.exe" VERIFICATION_FINALE_ARABE.php
```

### Problème: Modules Partiellement Traduits

**Symptômes:**
- Certains éléments en anglais dans les modules

**Solution:**
Retraduire les modules:
```bash
"C:/xampp/php/php.exe" maintenance/traduire_tous_modules.php
"C:/xampp/php/php.exe" CLEAR_ALL_CACHES_FINAL.php
```

### Problème: Caches Non Nettoyés

**Symptômes:**
- Changements non visibles
- Ancienne interface affichée

**Solution:**
```bash
"C:/xampp/php/php.exe" CLEAR_ALL_CACHES_FINAL.php
```

Puis:
1. Se déconnecter
2. Se reconnecter
3. Recharger avec Ctrl+Shift+R

---

## 🚀 DÉMARRAGE DU SYSTÈME

### Démarrage Manuel

**1. Démarrer XAMPP:**
```
C:\xampp\xampp-control.exe
```

**2. Démarrer Apache et MySQL:**
- Cliquer sur "Start" pour Apache
- Cliquer sur "Start" pour MySQL

**3. Accéder au Dashboard:**
```
http://localhost/onestschooled-test/public/dashboard
```

### Démarrage Automatique

**Double-cliquer sur:**
```
START_ONESTSCHOOL.bat
```

Ce script:
- ✅ Démarre XAMPP automatiquement
- ✅ Attend 5 secondes
- ✅ Ouvre le navigateur sur le dashboard

---

## 👥 GESTION DES UTILISATEURS

### Types d'Utilisateurs

1. **Super Admin** (Administrateur Principal)
   - Accès complet au système
   - Gestion de tous les modules
   - Configuration système

2. **Admin** (Administrateur)
   - Gestion de l'école
   - Accès aux modules principaux
   - Pas d'accès aux paramètres système

3. **Teacher** (Enseignant)
   - Gestion des classes
   - Saisie des notes
   - Présence des étudiants
   - Devoirs

4. **Student** (Étudiant)
   - Consultation des notes
   - Horaires de cours
   - Devoirs
   - Présence

5. **Parent** (Parent)
   - Suivi de l'enfant
   - Consultation des notes
   - Messages avec les enseignants
   - Paiement des frais

### Connexion

**URL:**
```
http://localhost/onestschooled-test/public/login
```

**Identifiants Super Admin:**
- Email: (fourni par l'école)
- Mot de passe: (fourni par l'école)

---

## 💾 MAINTENANCE

### Scripts de Maintenance

**Localisation:** `maintenance/`

1. **scanner_modules_anglais.php**
   - Scan les modules pour trouver les termes en anglais
   - Usage:
   ```bash
   "C:/xampp/php/php.exe" maintenance/scanner_modules_anglais.php
   ```

2. **traduire_tous_modules.php**
   - Traduit tous les modules en arabe
   - Usage:
   ```bash
   "C:/xampp/php/php.exe" maintenance/traduire_tous_modules.php
   ```

3. **activer_francais.php**
   - Active/traduit le français
   - Usage:
   ```bash
   "C:/xampp/php/php.exe" maintenance/activer_francais.php
   ```

### Scripts Essentiels

**Localisation:** Racine du projet

1. **CLEAR_ALL_CACHES_FINAL.php**
   - Nettoie tous les caches
   - À utiliser après chaque modification

2. **VERIFICATION_FINALE_ARABE.php**
   - Vérifie la configuration arabe
   - Affiche l'état du système

3. **set_default_language.php**
   - Réinitialise la langue par défaut en arabe
   - À utiliser si la langue est incorrecte

---

## 📱 FONCTIONNALITÉS SPÉCIFIQUES

### Admission en Ligne

**Module:** Student Info → Online Admission

**Processus:**
1. Formulaire d'admission sur le site web
2. Validation par l'administration
3. Paiement des frais d'admission
4. Création du compte étudiant

### Génération de Cartes d'Identité

**Module:** Student Info → بطاقات الهوية (ID Cards)

**Processus:**
1. Sélectionner les étudiants
2. Choisir le modèle de carte
3. Générer les cartes (PDF)
4. Imprimer

### Génération de Certificats

**Module:** Student Info → الشهادات (Certificates)

**Processus:**
1. Sélectionner l'étudiant
2. Choisir le type de certificat
3. Générer le certificat (PDF)
4. Imprimer et signer

### Communication Parents-Enseignants

**Module:** التواصل (Communication)

**Fonctionnalités:**
- Messages directs
- Notifications SMS
- Notifications email
- Annonces générales
- Forum de discussion

### Paiement en Ligne

**Module:** Fees → Collect

**Méthodes:**
- Paiement en ligne (si configuré)
- Paiement en espèces (enregistrement)
- Paiement par chèque (enregistrement)
- Historique des paiements

---

## 🔐 SÉCURITÉ

### Permissions et Rôles

**Gestion:** Staff Manage → Roles & Permissions

**Rôles par défaut:**
- Super Admin: Toutes les permissions
- Admin: Gestion de l'école
- Teacher: Modules pédagogiques
- Student: Consultation uniquement
- Parent: Suivi de l'enfant

**Création d'un rôle personnalisé:**
1. Aller dans Staff Manage → Roles
2. Cliquer sur "Add Role"
3. Définir le nom du rôle
4. Sélectionner les permissions
5. Enregistrer

### Sauvegarde

**Important:** Sauvegarder régulièrement:

1. **Base de données:**
   - Aller dans phpMyAdmin
   - Sélectionner `onest_school`
   - Cliquer sur "Export"
   - Télécharger le fichier SQL

2. **Fichiers:**
   - Sauvegarder le dossier:
   ```
   C:\xampp\htdocs\onestschooled-test\
   ```

**Fréquence recommandée:** Quotidienne ou hebdomadaire

---

## 📞 SUPPORT

### Documentation

**Localisation:** `documentation/`

Fichiers disponibles:
1. **LANGUES_CONFIGURATION_FINALE.md** - Configuration des langues
2. **ARABE_100_POURCENT.md** - Configuration arabe détaillée
3. **STATUT_FINAL_BBC_SCHOOL_ALGERIA.md** - État du système
4. **TRADUCTION_COMPLETE_TERMINEE.txt** - Résumé des traductions
5. **LIRE_MOI_ARABE.txt** - Instructions simples
6. **ARABE_PAR_DEFAUT.md** - Configuration arabe par défaut

### Contact BBC School

**Email:** info@bbcschool.net
**Téléphones:**
- Direction Générale: +213 23 35 28 74
- École Principale: +213 23 35 28 75
- Annexe Maternelle: +213 23 35 28 76

### Support Technique OnestSchool

**Site web:** www.onesttech.com
**Documentation:** docs.onesttech.com

---

## ❓ FAQ - QUESTIONS FRÉQUENTES

### Q1: Comment ajouter un nouvel étudiant?

**R:**
1. Aller dans Student Info → Student List
2. Cliquer sur "Add Student"
3. Remplir le formulaire
4. Enregistrer

### Q2: Comment générer un bulletin de notes?

**R:**
1. Aller dans Report → Marksheet
2. Sélectionner la classe et l'examen
3. Sélectionner l'étudiant
4. Cliquer sur "Generate"
5. Télécharger le PDF

### Q3: Comment enregistrer la présence?

**R:**
1. Aller dans Attendance → Daily Attendance
2. Sélectionner la date et la classe
3. Marquer présent/absent pour chaque étudiant
4. Enregistrer

### Q4: Comment collecter les frais?

**R:**
1. Aller dans Fees → Collect Fees
2. Sélectionner l'étudiant
3. Saisir le montant payé
4. Sélectionner le mode de paiement
5. Enregistrer

### Q5: Comment créer un examen?

**R:**
1. Aller dans Examination → Exam Setup
2. Cliquer sur "Add Exam"
3. Définir le nom, la date, la classe
4. Ajouter les matières
5. Enregistrer

### Q6: Comment changer mon mot de passe?

**R:**
1. Cliquer sur votre nom (en haut à droite)
2. Sélectionner "Update Password"
3. Saisir l'ancien mot de passe
4. Saisir le nouveau mot de passe
5. Confirmer et enregistrer

### Q7: Comment ajouter un enseignant?

**R:**
1. Aller dans Staff Manage → Staff List
2. Cliquer sur "Add Staff"
3. Remplir les informations
4. Sélectionner le rôle "Teacher"
5. Enregistrer

### Q8: Comment configurer les horaires?

**R:**
1. Aller dans Routines → Class Routine
2. Sélectionner la classe
3. Ajouter les cours par jour
4. Définir les horaires
5. Enregistrer

### Q9: Comment envoyer une notification?

**R:**
1. Aller dans Communication → Notice Board
2. Cliquer sur "Add Notice"
3. Rédiger le message
4. Sélectionner les destinataires
5. Publier

### Q10: Comment générer un rapport?

**R:**
1. Aller dans Report
2. Sélectionner le type de rapport
3. Choisir les critères (date, classe, etc.)
4. Cliquer sur "Generate"
5. Télécharger le PDF

---

## 🎓 GLOSSAIRE

### Termes Arabes Courants

| Arabe | Français | Anglais |
|-------|----------|---------|
| لوحة التحكم | Tableau de bord | Dashboard |
| الطالب | Étudiant | Student |
| ولي الأمر | Parent | Parent |
| المعلم | Enseignant | Teacher |
| الصف | Classe | Class |
| القسم | Section | Section |
| المادة | Matière | Subject |
| الحضور | Présence | Attendance |
| الإجازة | Congé | Leave |
| الرسوم | Frais | Fees |
| الامتحان | Examen | Examination |
| المكتبة | Bibliothèque | Library |
| الحسابات | Comptes | Accounts |
| التقرير | Rapport | Report |
| الموظفون | Personnel | Staff |
| الإعدادات | Paramètres | Settings |

---

**Dernière mise à jour:** Aujourd'hui
**Version:** 2.0
**Système:** OnestSchool pour BBC School Algeria
**Langue:** Arabe (par défaut) + Français (secondaire)
