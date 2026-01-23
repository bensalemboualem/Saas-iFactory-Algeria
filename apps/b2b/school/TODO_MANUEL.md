# TODO - Corrections Manuelles Requises

**Date:** 03/11/2025
**Statut:** En attente d'intervention manuelle

---

## ⚠️ PRIORITÉ CRITIQUE

### 1. Créer l'École Virtuelle dans la Base de Données

**Problème:** Table `schools` vide (0 enregistrements)

**Impact:**
- Modules dépendants peuvent échouer
- Dashboard peut afficher des erreurs
- Rapports ne peuvent pas être générés

**Solution:**

**Option A - Via Seeder:**
```bash
cd C:\xampp\htdocs\onestschooled-test
php artisan db:seed --class=SchoolSeeder
```

**Option B - Via Interface Admin:**
1. Se connecter en tant que Super Admin
2. Aller dans **Paramètres** > **Écoles**
3. Cliquer sur "Ajouter une École"
4. Remplir:
   - Nom: BBC School Algeria / مدرسة بي بي سي الجزائر
   - Code: BBC001
   - Email: contact@bbcschool.dz
   - Téléphone: +213 XXX XXX XXX
   - Adresse: Alger, Algérie
5. Upload du logo
6. Sauvegarder

**Option C - Via SQL Direct:**
```sql
INSERT INTO schools (name, code, email, phone, address, status, created_at, updated_at)
VALUES (
  'BBC School Algeria',
  'BBC001',
  'contact@bbcschool.dz',
  '+213XXXXXXXXX',
  'Alger, Algérie',
  1,
  NOW(),
  NOW()
);
```

**Vérification:**
```bash
php artisan tinker --execute="echo 'Écoles: ' . DB::table('schools')->count();"
```

---

## 🔴 PRIORITÉ HAUTE

### 2. Implémenter Date Picker Compatible RTL

**Fichiers affectés:**
- `resources/views/backend/student-info/student/create.blade.php` (ligne 160)
- `resources/views/backend/student-info/student/edit.blade.php` (ligne 160)
- `resources/views/frontend/online-admission.blade.php` (ligne 183)
- `resources/views/student-panel/profile/edit.blade.php` (ligne 160)
- ~12 autres fichiers

**Problème actuel:**
```blade
<input type="date" class="form-control" name="date_of_birth">
```
- Calendrier natif HTML5 ne supporte pas RTL
- Format MM/DD/YYYY au lieu du format arabe
- Icône calendrier du mauvais côté en arabe

**Solution recommandée:**

**Étape 1:** Installer un date picker JavaScript
```bash
npm install flatpickr
# OU
# Télécharger depuis https://flatpickr.js.org/
```

**Étape 2:** Ajouter dans `resources/views/backend/master.blade.php`:
```blade
@if (findDirectionOfLang() == 'rtl')
<link rel="stylesheet" href="{{ asset('backend/plugins/flatpickr/flatpickr-rtl.css') }}">
<script src="{{ asset('backend/plugins/flatpickr/flatpickr-ar.js') }}"></script>
@else
<link rel="stylesheet" href="{{ asset('backend/plugins/flatpickr/flatpickr.css') }}">
<script src="{{ asset('backend/plugins/flatpickr/flatpickr.js') }}"></script>
@endif
```

**Étape 3:** Remplacer dans les fichiers Blade:
```blade
{{-- Ancien --}}
<input type="date" class="form-control" name="date_of_birth">

{{-- Nouveau --}}
<input type="text" class="form-control flatpickr"
       name="date_of_birth"
       placeholder="{{ ___('common.select_date') }}"
       data-locale="{{ app()->getLocale() }}">
```

**Étape 4:** Initialiser JavaScript:
```javascript
document.addEventListener('DOMContentLoaded', function() {
    const locale = document.querySelector('.flatpickr').dataset.locale;
    flatpickr('.flatpickr', {
        dateFormat: 'Y-m-d',
        locale: locale,
        position: locale === 'ar' ? 'auto right' : 'auto left'
    });
});
```

**Fichiers à modifier:** 15 fichiers au total

---

### 3. Corriger les Templates PDF pour l'Arabe

**Fichiers affectés:**
- `resources/views/backend/certificate/printCertificate.blade.php`
- `resources/views/backend/attendance/reportPDF.blade.php`
- `resources/views/parent-panel/marksheet.blade.php`
- `resources/views/student-panel/marksheet.blade.php`

**Problèmes:**
1. Logo école mal positionné en arabe
2. Texte ne s'affiche pas de droite à gauche
3. Tableaux désalignés
4. Signatures à la mauvaise position

**Solution pour chaque fichier:**

**Exemple - printCertificate.blade.php:**

Ajouter au début du fichier:
```blade
@php
$isRTL = findDirectionOfLang() == 'rtl';
$textAlign = $isRTL ? 'right' : 'left';
$float = $isRTL ? 'right' : 'left';
@endphp

<style>
@if($isRTL)
.certificate-container {
    direction: rtl;
    text-align: right;
}
.logo-position {
    float: left !important;
}
.signature-section {
    text-align: left;
}
@endif
</style>
```

Modifier les classes:
```blade
{{-- Ancien --}}
<div class="header-logo">
    <img src="{{ $logo }}" />
</div>

{{-- Nouveau --}}
<div class="header-logo" style="text-align: {{ $textAlign }}">
    <img src="{{ $logo }}" />
</div>
```

**Action requise:** Réviser et tester chaque template PDF

---

## 🟡 PRIORITÉ MOYENNE

### 4. Créer les Fichiers de Traduction Manquants

**Modules non traduits:**

#### A) Fees (Frais Scolaires)
**Créer:** `resources/lang/{ar,fr,en}/fees.php`

**Clés requises:**
```php
// En anglais (fees.php)
return [
    'fees' => 'Fees',
    'fee_type' => 'Fee Type',
    'fee_amount' => 'Fee Amount',
    'due_date' => 'Due Date',
    'collect_fees' => 'Collect Fees',
    'fee_collection' => 'Fee Collection',
    'payment_method' => 'Payment Method',
    'cash' => 'Cash',
    'bank_transfer' => 'Bank Transfer',
    'online' => 'Online Payment',
    // ... ajouter plus
];
```

#### B) Examination (Examens)
**Créer:** `resources/lang/{ar,fr,en}/examination.php`

**Clés requises:**
```php
return [
    'examination' => 'Examination',
    'exam_name' => 'Exam Name',
    'exam_type' => 'Exam Type',
    'marks' => 'Marks',
    'grade' => 'Grade',
    'pass_marks' => 'Pass Marks',
    'exam_schedule' => 'Exam Schedule',
    'mark_sheet' => 'Mark Sheet',
    // ... ajouter plus
];
```

#### C) Communication (Communications)
**Créer:** `resources/lang/{ar,fr,en}/communication.php`

**Clés requises:**
```php
return [
    'notice' => 'Notice',
    'notice_board' => 'Notice Board',
    'send_sms' => 'Send SMS',
    'send_email' => 'Send Email',
    'message' => 'Message',
    'recipient' => 'Recipient',
    'subject' => 'Subject',
    // ... ajouter plus
];
```

#### D) Accounts (Comptabilité)
**Créer:** `resources/lang/{ar,fr,en}/accounts.php`

**Clés requises:**
```php
return [
    'income' => 'Income',
    'expense' => 'Expense',
    'account_head' => 'Account Head',
    'transaction' => 'Transaction',
    'balance' => 'Balance',
    'debit' => 'Debit',
    'credit' => 'Credit',
    // ... ajouter plus
];
```

**Action requise:** Créer ces 4 fichiers x 3 langues = 12 fichiers

---

### 5. Améliorer la Validation Côté Client JavaScript

**Fichier:** `public/js/bbc-script.js`

**Problème actuel (lignes 248-259):**
```javascript
// Validation ne respecte pas RTL
field.addEventListener('blur', function() {
    if (this.value.trim() === '') {
        this.style.borderColor = '#E84393';
    }
});
```

**Solution recommandée:**

Ajouter après la ligne 186:
```javascript
// RTL-aware validation
document.querySelectorAll('input[required], textarea[required], select[required]').forEach(field => {
    field.addEventListener('blur', function() {
        const isRTL = document.body.dir === 'rtl';
        if (this.value.trim() === '') {
            this.style.borderColor = '#E84393';
            this.style.boxShadow = '0 0 0 0.2rem rgba(232, 67, 147, 0.25)';

            // Message d'erreur RTL-aware
            if (!this.nextElementSibling || !this.nextElementSibling.classList.contains('error-message')) {
                const errorMsg = document.createElement('div');
                errorMsg.className = 'error-message invalid-feedback';
                errorMsg.style.display = 'block';
                errorMsg.style.textAlign = isRTL ? 'right' : 'left';
                errorMsg.textContent = isRTL ? 'هذا الحقل مطلوب' : 'This field is required';
                this.parentNode.insertBefore(errorMsg, this.nextSibling);
            }
        } else {
            this.style.borderColor = '';
            this.style.boxShadow = '';
            const errorMsg = this.nextElementSibling;
            if (errorMsg && errorMsg.classList.contains('error-message')) {
                errorMsg.remove();
            }
        }
    });
});
```

---

## 🟢 PRIORITÉ BASSE

### 6. Support d'Images Spécifiques par Langue

**Objectif:** Permettre l'upload de logos différents pour AR/FR/EN

**Fichier à modifier:** `app/Traits/FileUploadTrait.php`

**Changement requis:**

Modifier la méthode `uploadFile()` (ligne 66):
```php
// Ancien
$directory = "uploads/$path";

// Nouveau
$locale = app()->getLocale();
$directory = "uploads/$path/$locale";
```

**Impact:**
- Logos séparés pour chaque langue
- Bannières multilingues
- Images de contenu localisées

**Attention:** Nécessite une migration pour les images existantes

---

### 7. Améliorer le Nice Select Plugin pour RTL

**Fichier:** `public/backend/plugins/nice-select/nice-select.js`

**Problème:** Flèche du dropdown au mauvais endroit en RTL

**Solution:**

Ajouter dans le CSS (déjà fait en partie):
```css
*[dir=rtl] .nice-select::after {
    left: 12px;
    right: auto;
}
```

Mais aussi modifier le JavaScript pour ouvrir le dropdown dans la bonne direction:
```javascript
// Dans nice-select.js, ajouter:
var isRTL = document.body.dir === 'rtl';
if (isRTL) {
    dropdown.classList.add('rtl-dropdown');
}
```

---

### 8. Tests Automatisés Multilingues

**Créer:** `tests/Feature/MultilingualTest.php`

**Contenu suggéré:**
```php
<?php

namespace Tests\Feature;

use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;

class MultilingualTest extends TestCase
{
    /** @test */
    public function it_displays_login_form_in_arabic()
    {
        app()->setLocale('ar');
        $response = $this->get('/login');
        $response->assertSee('تسجيل الدخول');
    }

    /** @test */
    public function it_displays_login_form_in_french()
    {
        app()->setLocale('fr');
        $response = $this->get('/login');
        $response->assertSee('Connexion');
    }

    /** @test */
    public function it_validates_in_correct_language()
    {
        app()->setLocale('ar');
        $response = $this->post('/login', []);
        $response->assertSee('مطلوب'); // "required" en arabe
    }
}
```

**Action:** Créer des tests pour chaque module traduit

---

## 📊 Résumé des Actions Requises

| Action | Priorité | Temps estimé | Complexité |
|--------|----------|--------------|------------|
| Créer école virtuelle | CRITIQUE | 5 min | Facile |
| Date picker RTL | HAUTE | 2-3 heures | Moyenne |
| Templates PDF RTL | HAUTE | 4-6 heures | Difficile |
| Traductions manquantes | MOYENNE | 3-4 heures | Facile |
| Validation JS RTL | MOYENNE | 1-2 heures | Moyenne |
| Images par langue | BASSE | 3-4 heures | Difficile |
| Nice Select RTL | BASSE | 1 heure | Facile |
| Tests automatisés | BASSE | 2-3 heures | Moyenne |

**Total estimé:** 16-27 heures de travail

---

## ✅ Checklist de Validation

Après avoir complété ces corrections:

- [ ] École virtuelle créée et vérifiée
- [ ] Date pickers fonctionnent en AR/FR/EN
- [ ] PDFs générés correctement en arabe
- [ ] Tous les modules traduits (fees, exam, comm, accounts)
- [ ] Validation JavaScript multilingue
- [ ] Images spécifiques par langue (optionnel)
- [ ] Nice Select fonctionne en RTL
- [ ] Tests automatisés passent

---

## 📝 Notes de Développement

**Avant de commencer:**
1. Créer une branche Git: `git checkout -b fixes/multilingual-manual`
2. Faire un backup de la base de données
3. Tester chaque modification individuellement
4. Commiter régulièrement

**Pendant le développement:**
- Vider les caches après chaque modification
- Tester sur les 3 langues (AR/FR/EN)
- Vérifier la compatibilité mobile
- Documenter les changements

**Après les corrections:**
- Créer un pull request
- Demander une revue de code
- Tester en environnement de staging
- Mettre à jour la documentation

---

**Document créé:** 03/11/2025
**Dernière mise à jour:** 03/11/2025
**Responsable:** Équipe de développement
