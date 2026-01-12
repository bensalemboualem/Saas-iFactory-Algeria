# 📄 Upload de Documents - IA Factory

Guide complet pour uploader et interagir avec vos documents via l'interface de chat LLM.

---

## 📑 Table des Matières

1. [Introduction](#introduction)
2. [Méthodes d'Upload](#méthodes-dupload)
3. [Gestion de Vos Documents](#gestion-de-vos-documents)
4. [Limites d'Upload](#limites-dupload)
5. [Formats Supportés](#formats-supportés)
6. [Sécurité et Confidentialité](#sécurité-et-confidentialité)
7. [Traitement des Documents](#traitement-des-documents)
8. [Intégration RAG](#intégration-rag)
9. [Cas d'Usage](#cas-dusage)
10. [Dépannage](#dépannage)

---

## 🎯 Introduction

IA Factory vous permet d'**uploader et d'interagir avec vos documents** directement dans l'interface de chat. Le système utilise des techniques avancées de **RAG (Retrieval Augmented Generation)** pour extraire des informations pertinentes et répondre à vos questions avec précision.

### Avantages de l'Upload de Documents

✅ **Analyse Intelligente** : Les LLMs comprennent le contenu et répondent avec contexte
✅ **Multi-formats** : PDF, Word, Excel, CSV, images, vidéos, audio
✅ **Vectorisation Automatique** : Recherche sémantique instantanée
✅ **Sécurité Maximale** : Chiffrement AES-256-GCM, accès contrôlé
✅ **Multilingue** : Français, Arabe, Darija, Tamazight, Anglais

---

## 📤 Méthodes d'Upload

### 1️⃣ Upload via Interface Chat

**Méthode la plus simple pour uploader des fichiers individuels.**

```
Étapes :
1. Ouvrez une conversation dans Studio IA ou Hub IA
2. Cliquez sur l'icône 📎 (Attach) à côté du champ de saisie
3. Sélectionnez vos fichiers (ou glissez-déposez)
4. Le fichier s'upload automatiquement
5. Posez votre question directement
```

**Exemple d'utilisation :**

```
Vous : [Upload "contrat-bail-2024.pdf"]
      Résume ce contrat de bail et identifie les clauses importantes

IA : 📄 Contrat de Bail - Résumé

Type : Location commerciale
Durée : 3 ans (renouvelable)
Loyer : 150,000 DA/mois + charges
Dépôt de garantie : 450,000 DA (3 mois)

Clauses importantes :
1. Article 5 : Révision annuelle du loyer (+5% max)
2. Article 8 : Préavis de résiliation (6 mois)
3. Article 12 : Travaux à la charge du locataire
4. Article 15 : Clause pénale (50,000 DA/jour de retard)

⚠️ Points d'attention :
- Pas de sous-location autorisée (Article 9)
- Assurance obligatoire (Article 10)
```

---

### 2️⃣ Upload via Glisser-Déposer

**Méthode rapide pour uploader plusieurs fichiers.**

```
Étapes :
1. Ouvrez votre explorateur de fichiers
2. Sélectionnez un ou plusieurs fichiers
3. Glissez-les directement dans la fenêtre de chat
4. Les fichiers s'uploadent automatiquement
5. Attendez la confirmation ✅
```

**Indicateurs visuels :**

```
┌─────────────────────────────────────┐
│  📎 Fichiers en cours d'upload...   │
│                                     │
│  ⏳ rapport-2024.pdf (1.2 MB)       │
│  ⏳ factures.xlsx (450 KB)          │
│  ✅ contrat.docx (200 KB)           │
│                                     │
│  2/3 fichiers uploadés              │
└─────────────────────────────────────┘
```

---

### 3️⃣ Upload via Bibliothèque de Documents

**Méthode pour gérer une collection de documents.**

```
Navigation :
Hub IA → ⚙️ Paramètres → 📚 Bibliothèque de Documents → ➕ Ajouter
```

**Fonctionnalités de la Bibliothèque :**

| Fonctionnalité | Description |
|----------------|-------------|
| **Collections** | Organiser les documents par projet/client |
| **Tags** | Étiqueter pour retrouver facilement |
| **Recherche** | Recherche par nom, contenu, métadonnées |
| **Partage** | Partager avec équipe (Enterprise) |
| **Versions** | Historique des versions uploadées |

**Exemple de structure :**

```
📚 Bibliothèque de Documents
│
├── 📁 Projets Immobiliers
│   ├── 📄 Plan-Alger-Centre.pdf (12 MB)
│   ├── 📄 Étude-Marché-Oran.xlsx (2.5 MB)
│   └── 📄 Budget-Prévisionnel.xlsx (800 KB)
│
├── 📁 Contrats Clients
│   ├── 📄 Contrat-SonatrachLOI.pdf (1.5 MB)
│   ├── 📄 Contrat-Cevital.pdf (2 MB)
│   └── 📄 Conditions-Générales.docx (500 KB)
│
└── 📁 Ressources Humaines
    ├── 📄 Organigramme-2024.png (1 MB)
    ├── 📄 Salaires-Janvier.xlsx (350 KB)
    └── 📄 Règlement-Intérieur.pdf (3 MB)
```

---

### 4️⃣ Upload via API

**Méthode pour intégration automatisée.**

```http
POST /api/v1/documents/upload
Host: api.iafactory.dz
Content-Type: multipart/form-data
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="rapport.pdf"
Content-Type: application/pdf

[binary data]
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="collection"

Rapports Mensuels
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="tags"

rapport,finance,janvier-2024
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

**Réponse :**

```json
{
  "status": "success",
  "document_id": "doc_8f7d6e5c4b3a2910",
  "filename": "rapport.pdf",
  "size": 1258496,
  "pages": 24,
  "uploaded_at": "2024-01-15T09:30:45Z",
  "vectorized": true,
  "chunks": 187,
  "url": "https://docs.iafactory.dz/doc_8f7d6e5c4b3a2910"
}
```

**Exemple Python :**

```python
import requests

def upload_document(file_path, collection="Default", tags=[]):
    url = "https://api.iafactory.dz/api/v1/documents/upload"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    with open(file_path, 'rb') as f:
        files = {
            'file': (file_path.split('/')[-1], f, 'application/pdf')
        }
        data = {
            'collection': collection,
            'tags': ','.join(tags)
        }

        response = requests.post(url, headers=headers, files=files, data=data)
        return response.json()

# Utilisation
result = upload_document(
    'rapports/janvier-2024.pdf',
    collection='Rapports Mensuels',
    tags=['finance', 'janvier', '2024']
)

print(f"✅ Document uploadé : {result['document_id']}")
print(f"📊 {result['pages']} pages, {result['chunks']} chunks vectorisés")
```

---

## 🗂️ Gestion de Vos Documents

### Visualiser les Documents

**Interface de gestion :**

```
┌────────────────────────────────────────────────────────────────┐
│  📚 Mes Documents                                   🔍 Recherche │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  📄 Contrat-Bail-2024.pdf                         📅 15/01/2024│
│     📊 2.5 MB • 12 pages • 🔒 Privé                            │
│     🏷️ contrat, immobilier, alger                              │
│     [👁️ Voir] [💬 Chatter] [🗑️ Supprimer]                      │
│                                                                │
│  📊 Factures-Janvier.xlsx                         📅 10/01/2024│
│     📊 450 KB • 3 feuilles • 👥 Partagé (Équipe Finance)       │
│     🏷️ factures, comptabilité, 2024                           │
│     [👁️ Voir] [💬 Chatter] [🗑️ Supprimer]                      │
│                                                                │
│  📸 Plan-Projet-Oran.png                          📅 08/01/2024│
│     📊 1.2 MB • 1920x1080 • 🔒 Privé                           │
│     🏷️ architecture, oran, projet                             │
│     [👁️ Voir] [💬 Chatter] [🗑️ Supprimer]                      │
│                                                                │
│  🎥 Présentation-Produit.mp4                      📅 05/01/2024│
│     📊 85 MB • 12:35 min • 👥 Partagé (Marketing)              │
│     🏷️ marketing, produit, vidéo                              │
│     [👁️ Voir] [💬 Chatter] [🗑️ Supprimer]                      │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

### Actions Disponibles

#### 1. **Voir le Document**

```
Cliquez sur [👁️ Voir] pour :
- Prévisualiser le document (PDF, images, vidéos)
- Télécharger le fichier original
- Voir les métadonnées complètes
- Consulter l'historique de versions
```

**Exemple de prévisualisation :**

```
┌────────────────────────────────────────────┐
│  📄 Contrat-Bail-2024.pdf                  │
├────────────────────────────────────────────┤
│                                            │
│  [Aperçu du PDF - Page 1/12]               │
│                                            │
│  ℹ️ Métadonnées :                          │
│  • Titre : Contrat de Bail Commercial     │
│  • Auteur : Cabinet Juridique Alger       │
│  • Date création : 10/01/2024             │
│  • Langue : Français                       │
│  • Mots-clés : bail, commerce, 3 ans      │
│                                            │
│  📊 Statistiques :                         │
│  • Taille : 2.5 MB                         │
│  • Pages : 12                              │
│  • Mots : 4,582                            │
│  • Chunks vectorisés : 94                  │
│                                            │
│  [⬇️ Télécharger] [💬 Chatter] [🗑️ Suppr.]  │
└────────────────────────────────────────────┘
```

---

#### 2. **Chatter avec le Document**

```
Cliquez sur [💬 Chatter] pour :
- Poser des questions sur le contenu
- Résumer le document
- Extraire des informations spécifiques
- Traduire des sections
```

**Exemple de conversation :**

```
Vous : Quelle est la date de fin du contrat ?

IA : 📅 Date de fin du contrat : **31 décembre 2027**

Le contrat débute le 1er janvier 2025 pour une durée de 3 ans,
avec possibilité de renouvellement automatique pour 1 an
(Article 2, page 2).

⏰ Important : Le préavis de non-renouvellement doit être envoyé
6 mois avant l'échéance (avant le 30 juin 2027).
```

---

#### 3. **Supprimer le Document**

```
Cliquez sur [🗑️ Supprimer] pour :
- Supprimer définitivement le document
- Libérer de l'espace de stockage
- Respecter les règles de rétention RGPD
```

**Confirmation de suppression :**

```
┌────────────────────────────────────────────┐
│  ⚠️ Confirmer la suppression               │
├────────────────────────────────────────────┤
│                                            │
│  Vous êtes sur le point de supprimer :    │
│  📄 Contrat-Bail-2024.pdf                  │
│                                            │
│  ⚠️ Cette action est IRRÉVERSIBLE          │
│                                            │
│  Les données suivantes seront supprimées : │
│  • Fichier original (2.5 MB)              │
│  • 94 chunks vectorisés                    │
│  • Métadonnées et historique              │
│  • Conversations associées                 │
│                                            │
│  [❌ Annuler]  [🗑️ Supprimer définitivement] │
└────────────────────────────────────────────┘
```

---

## 📏 Limites d'Upload

Pour maintenir des **performances optimales**, IA Factory applique les limites suivantes :

### Limites par Type de Fichier

| Type de Fichier | Limite Maximale | Détails |
|-----------------|-----------------|---------|
| **📄 PDF** | 2,000 pages | Extracte texte + images |
| **📝 CSV/TXT** | 50 MB | Encodage UTF-8 recommandé |
| **📊 Excel** | 30 MB | Toutes feuilles analysées |
| **🖼️ Images** | 50 MB | PNG, JPG, WEBP, SVG |
| **🎥 Vidéos** | 100 MB | MP4, MOV, AVI (transcription audio) |
| **🎵 Audio** | 50 MB | MP3, WAV, M4A (transcription) |
| **📄 Word** | 30 MB | DOCX, DOC |
| **📊 PowerPoint** | 50 MB | PPTX, PPT |

---

### Limites par Plan

| Plan | Stockage Total | Fichiers/Mois | Taille/Fichier | Vectorisation |
|------|----------------|---------------|----------------|---------------|
| **Free** | 1 GB | 50 fichiers | Limites standard | ✅ Inclus |
| **Basic** | 10 GB | 500 fichiers | Limites standard | ✅ Inclus |
| **Pro** | 100 GB | Illimité | Limites standard | ✅ Inclus + prioritaire |
| **Enterprise** | Illimité | Illimité | Limites personnalisées | ✅ Inclus + dédié |

---

### Quota de Vectorisation

**La vectorisation consomme des crédits selon la taille du document.**

| Taille du Document | Crédits Consommés | Temps de Traitement |
|--------------------|-------------------|---------------------|
| < 1 MB | 0.5 crédits | < 10 secondes |
| 1-5 MB | 2 crédits | 10-30 secondes |
| 5-20 MB | 5 crédits | 30-90 secondes |
| 20-50 MB | 10 crédits | 1-3 minutes |
| > 50 MB | 20+ crédits | 3-10 minutes |

**💡 Astuce :** Compressez vos PDFs avant upload pour économiser des crédits !

---

### Gestion du Quota

**Vérifier votre utilisation :**

```
Hub IA → ⚙️ Paramètres → 📊 Utilisation → 📚 Documents
```

**Tableau de bord :**

```
┌────────────────────────────────────────────────────────┐
│  📊 Utilisation des Documents - Janvier 2024           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  💾 Stockage utilisé :  7.2 GB / 10 GB (72%)           │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░                              │
│                                                        │
│  📄 Fichiers uploadés : 342 / 500 (68%)                │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░                              │
│                                                        │
│  🔢 Crédits vectorisation : 1,245 crédits              │
│                                                        │
│  📈 Tendance : +15% vs mois dernier                    │
│                                                        │
│  💡 Suggestion : Supprimez les anciens documents       │
│     pour libérer 2.8 GB                                │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 📂 Formats Supportés

### Documents Texte

| Format | Extension | Extraction | Vectorisation |
|--------|-----------|------------|---------------|
| **PDF** | `.pdf` | Texte + Images (OCR) | ✅ Automatique |
| **Word** | `.docx`, `.doc` | Texte + métadonnées | ✅ Automatique |
| **Excel** | `.xlsx`, `.xls` | Toutes feuilles + formules | ✅ Automatique |
| **PowerPoint** | `.pptx`, `.ppt` | Texte + notes | ✅ Automatique |
| **CSV** | `.csv` | Structure tabulaire | ✅ Automatique |
| **Texte** | `.txt`, `.md` | Texte brut | ✅ Automatique |
| **RTF** | `.rtf` | Texte formaté | ✅ Automatique |

---

### Images

| Format | Extension | Traitement | Cas d'Usage |
|--------|-----------|------------|-------------|
| **PNG** | `.png` | OCR + Vision GPT-4o | Plans, screenshots, schémas |
| **JPEG** | `.jpg`, `.jpeg` | OCR + Vision GPT-4o | Photos, documents scannés |
| **WebP** | `.webp` | OCR + Vision GPT-4o | Images web modernes |
| **SVG** | `.svg` | Analyse vectorielle | Logos, diagrammes |
| **TIFF** | `.tiff`, `.tif` | OCR haute qualité | Documents professionnels |

**Exemple d'analyse d'image :**

```
Vous : [Upload "plan-appartement.png"]
      Analyse ce plan et donne les dimensions

IA : 🏠 Analyse du Plan d'Appartement

📐 Dimensions :
• Surface totale : 95 m²
• Salon/Séjour : 28 m² (6m x 4.5m)
• Chambre principale : 18 m² (4m x 4.5m)
• Chambre 2 : 12 m² (3m x 4m)
• Cuisine : 10 m² (2.5m x 4m)
• Salle de bain : 6 m² (2m x 3m)
• WC : 2 m² (1.5m x 1.3m)
• Couloir : 8 m²
• Balcon : 6 m²

🚪 Ouvertures :
• 5 portes intérieures
• 1 porte d'entrée blindée
• 3 fenêtres double vitrage
• 1 porte-fenêtre (balcon)

✅ Conformité :
• Surface habitable > 90 m² ✓
• Hauteur sous plafond : 3.0m ✓
• Ventilation naturelle : OK ✓
```

---

### Audio et Vidéo

| Format | Extension | Traitement | Durée Max |
|--------|-----------|------------|-----------|
| **MP4** | `.mp4` | Transcription + extraction frames | 60 min |
| **MOV** | `.mov` | Transcription + extraction frames | 60 min |
| **AVI** | `.avi` | Transcription + extraction frames | 60 min |
| **MP3** | `.mp3` | Transcription audio | 120 min |
| **WAV** | `.wav` | Transcription audio | 120 min |
| **M4A** | `.m4a` | Transcription audio | 120 min |

**Langues supportées pour transcription :**
- 🇫🇷 Français (dialecte algérien inclus)
- 🇩🇿 Arabe (Standard + Darija)
- 🇬🇧 Anglais
- 🇪🇸 Espagnol
- Tamazight (en développement)

**Exemple de transcription vidéo :**

```
Vous : [Upload "presentation-produit.mp4"]
      Résume cette vidéo de présentation

IA : 🎥 Résumé de la Vidéo (Durée : 12:35)

📋 Transcription complète disponible (3,240 mots)

🎯 Points Clés :

[00:00-02:30] Introduction du produit "SmartHome Algérie"
• Système domotique compatible WiFi et Zigbee
• Prix : 49,900 DA (pack de base)
• Installation en 2 heures

[02:30-06:15] Fonctionnalités principales
• Contrôle lumières (toutes les pièces)
• Gestion chauffage (économie 30%)
• Surveillance caméras (4 incluses)
• Application mobile iOS/Android

[06:15-09:45] Démonstration pratique
• Scénarios automatisés ("Je rentre", "Bonne nuit")
• Contrôle vocal (Arabe + Français)
• Intégration Google Home / Alexa

[09:45-12:35] Offre de lancement
• -20% jusqu'au 31/01/2024 (39,920 DA)
• Installation gratuite (valeur 5,000 DA)
• Support technique 24/7 en Arabe/Français

💬 Citations importantes :
"Notre système est le premier en Algérie à supporter
 les commandes vocales en dialecte algérien." (04:23)

📊 Statistiques mentionnées :
• 500+ installations à Alger
• 98% de satisfaction client
• Économie moyenne électricité : 4,500 DA/mois
```

---

## 🔒 Sécurité et Confidentialité

IA Factory accorde la **priorité absolue à la sécurité** de vos documents.

### Chiffrement

| Niveau | Technologie | Description |
|--------|-------------|-------------|
| **En transit** | TLS 1.3 | Chiffrement HTTPS de bout en bout |
| **Au repos** | AES-256-GCM | Stockage chiffré dans PostgreSQL |
| **Métadonnées** | Hachage SHA-256 | Noms de fichiers anonymisés |
| **Clés** | HashiCorp Vault | Rotation automatique (90 jours) |

---

### Contrôle d'Accès

```
Principe : "Least Privilege" (Moindre Privilège)

┌─────────────────────────────────────────┐
│  🔐 Qui peut accéder à vos documents ?  │
├─────────────────────────────────────────┤
│                                         │
│  ✅ VOUS (propriétaire)                 │
│     • Lecture, modification, suppression│
│     • Partage avec équipe (Enterprise)  │
│                                         │
│  ✅ LLMs d'IA Factory                   │
│     • Lecture UNIQUEMENT pendant chat   │
│     • Pas de stockage des embeddings    │
│     • Pas d'entraînement sur vos docs   │
│                                         │
│  ✅ Équipe (si partagé - Enterprise)    │
│     • Permissions configurables         │
│     • Lecture seule / Édition / Admin   │
│                                         │
│  ❌ JAMAIS                              │
│     • Autres utilisateurs IA Factory    │
│     • Fournisseurs de LLMs tiers        │
│     • Employés d'IA Factory             │
│     • Gouvernements / tiers             │
│                                         │
└─────────────────────────────────────────┘
```

---

### Conformité Réglementaire

| Réglementation | Statut | Mesures Appliquées |
|----------------|--------|-------------------|
| **RGPD** | ✅ Conforme | Droit à l'oubli, portabilité, consentement |
| **Loi 18-07 (DZ)** | ✅ Conforme | Hébergement local (Algérie Télécom) |
| **ISO 27001** | ✅ Certifié | Gestion sécurité de l'information |
| **SOC 2 Type II** | ✅ Certifié | Audits trimestriels indépendants |
| **HIPAA** | ✅ Conforme | Documents médicaux (hôpitaux algériens) |

---

### Politique de Rétention

```
📅 Durée de conservation des documents :

• Documents actifs : Tant que le compte est actif
• Après suppression manuelle : 0 jour (suppression immédiate)
• Après fermeture compte : 30 jours (puis suppression définitive)
• Sauvegardes chiffrées : 90 jours max

⚖️ Exceptions légales :
Si requis par la loi algérienne, conservation jusqu'à 10 ans
(ex: documents comptables, contrats commerciaux)
```

---

### Audit et Traçabilité

**Journaux d'audit complets pour toutes les actions :**

```
📊 Journal d'Audit - Contrat-Bail-2024.pdf

┌────────────────────────────────────────────────────────┐
│  📅 15/01/2024 09:30:45  👤 Benali Sarah (ID: 1234)    │
│  ✅ ACTION : Upload document                           │
│  📍 IP : 41.107.x.x (Alger, Algérie)                   │
│  🖥️ Device : Windows 11, Chrome 120                    │
│                                                        │
│  📅 15/01/2024 14:22:13  👤 Benali Sarah               │
│  ✅ ACTION : Lecture document (Chat)                   │
│  💬 Prompt : "Résume ce contrat"                       │
│  🤖 Modèle : GPT-4o                                    │
│                                                        │
│  📅 18/01/2024 10:15:30  👤 Benali Sarah               │
│  ✅ ACTION : Partage avec équipe (2 membres)           │
│  👥 Partagé avec : Ahmed K., Fatima B.                 │
│  🔐 Permissions : Lecture seule                        │
│                                                        │
│  📅 20/01/2024 16:45:00  👤 Ahmed Karim (ID: 5678)     │
│  ✅ ACTION : Lecture document (Chat)                   │
│  💬 Prompt : "Quelle est la durée du bail ?"          │
│  🤖 Modèle : Claude Sonnet 4.5                         │
└────────────────────────────────────────────────────────┘
```

---

### Protection Anti-Fuite

```
🛡️ Mesures de protection :

✅ Watermarking invisible
   • Chaque PDF téléchargé contient un watermark unique
   • Permet de tracer l'origine en cas de fuite

✅ DLP (Data Loss Prevention)
   • Détection automatique de données sensibles
   • Alertes si numéros de carte bancaire, mots de passe détectés

✅ Accès restreint par IP (Enterprise)
   • Whitelist d'adresses IP autorisées
   • Géolocalisation (accès uniquement depuis Algérie)

✅ 2FA obligatoire (Pro/Enterprise)
   • Authentification à deux facteurs pour accès documents sensibles
```

---

## ⚙️ Traitement des Documents

### Pipeline de Vectorisation

```
Étapes automatiques après upload :

1️⃣ EXTRACTION
   ↓
   • Texte extrait (PDF, Word, Excel)
   • OCR appliqué (images, scans)
   • Transcription audio/vidéo
   ↓
2️⃣ PREPROCESSING
   ↓
   • Nettoyage du texte (espaces, caractères spéciaux)
   • Détection de langue (FR, AR, EN)
   • Segmentation en phrases
   ↓
3️⃣ CHUNKING
   ↓
   • Découpage intelligent (500 tokens/chunk)
   • Overlap de 50 tokens (contexte)
   • Préservation de la structure (titres, listes)
   ↓
4️⃣ EMBEDDING
   ↓
   • Vectorisation avec text-embedding-3-large
   • Vecteurs de 3072 dimensions
   • Stockage dans PGVector
   ↓
5️⃣ INDEXATION
   ↓
   • Index HNSW pour recherche rapide
   • Métadonnées (titre, auteur, date, tags)
   • Prêt pour requêtes sémantiques
   ✅
```

---

### Qualité de l'Extraction

| Type de Document | Qualité Extraction | OCR Requis | Précision |
|------------------|-------------------|------------|-----------|
| **PDF natif** | ⭐⭐⭐⭐⭐ | Non | 99.9% |
| **PDF scanné** | ⭐⭐⭐⭐ | Oui | 95-98% |
| **Word/Excel** | ⭐⭐⭐⭐⭐ | Non | 99.9% |
| **Images (OCR)** | ⭐⭐⭐⭐ | Oui | 92-96% |
| **Vidéos (STT)** | ⭐⭐⭐⭐ | Transcription | 90-95% |
| **Audio (STT)** | ⭐⭐⭐⭐⭐ | Transcription | 95-98% |

**💡 Conseils pour meilleure extraction :**
- Utilisez des PDFs natifs (non scannés) quand possible
- Scans : résolution 300 DPI minimum
- Audio/Vidéo : évitez le bruit de fond
- Excel : nommez clairement vos feuilles et colonnes

---

### Recherche Sémantique

**Technologie utilisée : Recherche Vectorielle + Reranking**

```python
Exemple de recherche :

Question : "Quel est le montant du loyer ?"

Étape 1 : Vectorisation de la question
→ Vecteur [0.12, -0.45, 0.78, ..., 0.34]  # 3072 dimensions

Étape 2 : Recherche de similarité cosinus
→ Top 20 chunks les plus similaires

Étape 3 : Reranking avec Cohere Rerank
→ Top 5 chunks les plus pertinents

Étape 4 : Contexte envoyé au LLM
→ GPT-4o génère la réponse finale

Résultat :
"Le montant du loyer est de 150,000 DA par mois,
payable le 1er de chaque mois (Article 3, page 2)."
```

---

## 🔗 Intégration RAG

**Retrieval Augmented Generation : Combiner vos documents avec la puissance des LLMs**

### Configuration RAG

```
Hub IA → ⚙️ Paramètres → 🧠 RAG → ⚙️ Configuration
```

**Paramètres ajustables :**

| Paramètre | Valeur par Défaut | Description |
|-----------|-------------------|-------------|
| **Nombre de chunks** | 5 | Nombre de passages à récupérer |
| **Seuil de similarité** | 0.7 | Score minimum (0-1) |
| **Overlap** | 50 tokens | Chevauchement entre chunks |
| **Taille chunk** | 500 tokens | Longueur de chaque chunk |
| **Reranking** | Activé | Améliore pertinence (+15%) |
| **Citations** | Activé | Affiche sources (page, ligne) |

---

### Mode RAG Avancé

**Pour analyses complexes de multiples documents :**

```
Vous : @RAG Analyse les 5 contrats de bail et trouve
       les différences de tarification

IA : 📊 Analyse Comparative des Contrats de Bail

J'ai analysé les 5 documents uploadés :
✅ Contrat-Bail-Alger-Centre.pdf
✅ Contrat-Bail-Oran-Plateau.pdf
✅ Contrat-Bail-Constantine-Vieux.pdf
✅ Contrat-Bail-Annaba-Centre.pdf
✅ Contrat-Bail-Tlemcen-Mechouar.pdf

💰 Comparaison Tarifaire :

┌──────────────┬────────────┬─────────┬──────────┐
│ Ville        │ Loyer/mois │ Dépôt   │ DA/m²    │
├──────────────┼────────────┼─────────┼──────────┤
│ Alger Centre │ 150,000 DA │ 450k DA │ 1,500 DA │
│ Oran Plateau │ 120,000 DA │ 360k DA │ 1,200 DA │
│ Constantine  │  95,000 DA │ 285k DA │   950 DA │
│ Annaba       │  85,000 DA │ 255k DA │   850 DA │
│ Tlemcen      │  70,000 DA │ 210k DA │   700 DA │
└──────────────┴────────────┴─────────┴──────────┘

📈 Insights :
• Alger Centre = +114% vs Tlemcen (ville la plus chère)
• Dépôt = 3 mois pour tous les contrats (standard)
• Révision annuelle : +5% (Alger, Oran) vs +3% (autres villes)

⚖️ Clauses spécifiques :
• Alger : Assurance 50,000 DA obligatoire
• Oran : Travaux inclus dans le loyer
• Constantine : Préavis 3 mois (vs 6 mois ailleurs)

📍 Sources :
[1] Contrat-Bail-Alger-Centre.pdf, Article 3, p.2
[2] Contrat-Bail-Oran-Plateau.pdf, Article 3, p.2
[3] Contrat-Bail-Constantine-Vieux.pdf, Article 2, p.1
...
```

---

## 🎯 Cas d'Usage

### 1. **Analyse de Contrats**

```
Uploadez : Contrats, accords, conventions
Questions : Clauses importantes, dates, obligations, risques
```

**Exemple :**

```
Vous : [Upload 3 contrats de prestation]
      Compare ces contrats et trouve les clauses les plus favorables

IA : ⚖️ Analyse Comparative des Contrats

✅ Contrat A (Sonatrach) - LE PLUS AVANTAGEUX
• Paiement : 30 jours (vs 45-60 pour les autres)
• Révision prix : Annuelle +IPC (inflation)
• Clause de sortie : 3 mois de préavis
• Pénalités retard : 1%/jour (raisonnable)
• Bonus performance : Jusqu'à +15% si objectifs atteints

⚠️ Contrat B (Cevital) - CLAUSES RESTRICTIVES
• Paiement : 60 jours (délai long)
• Exclusivité : 2 ans (bloque autres clients)
• Pénalités : 5%/jour (très élevé !)
• Pas de clause de révision de prix

📊 Recommandation : Privilégier Contrat A, négocier Contrat B
```

---

### 2. **Recherche dans Documentation Technique**

```
Uploadez : Manuels, guides, spécifications
Questions : Procédures, troubleshooting, configurations
```

**Exemple :**

```
Vous : [Upload "Manuel-Installation-Climatisation.pdf"]
      Comment installer le système sur un toit plat ?

IA : 🔧 Procédure d'Installation - Toit Plat

📋 Prérequis (Section 3.2, p.18) :
• Surface plane et étanche
• Capacité portante : 150 kg/m² minimum
• Distance groupe extérieur / intérieur : max 15m
• Prise électrique 220V proche (3m max)

🛠️ Étapes d'Installation (Section 4.5, p.32-35) :

1. Préparation de la surface (30 min)
   • Nettoyer zone (2m x 1.5m)
   • Vérifier étanchéité
   • Marquer emplacements fixations

2. Installation supports (45 min)
   • Poser dalles béton 50x50cm (poids 15kg chacune)
   • Visser supports métalliques
   • Vérifier niveau horizontal (±2°)

3. Pose unité extérieure (20 min)
   • Déposer sur supports
   • Fixer avec 4 boulons M10
   • Laisser espace 60cm tout autour

4. Raccordement frigorifique (60 min)
   • Dérouler tubes cuivre (éviter coudes)
   • Raccorder avec clés dynamométriques
   • Étanchéité : test gaz azote 40 bars

⚠️ ATTENTION (p.35) :
"Ne jamais percer la membrane d'étanchéité du toit.
Utiliser UNIQUEMENT dalles béton lestées."

⏱️ Durée totale : 3-4 heures (2 techniciens)
💰 Coût installation : 15,000-20,000 DA

📞 Support : 0560 12 34 56 (7j/7, 8h-20h)
```

---

### 3. **Analyse Financière**

```
Uploadez : Bilans, rapports, factures, relevés bancaires
Questions : Tendances, anomalies, prévisions
```

**Exemple :**

```
Vous : [Upload "Factures-2024.xlsx"]
      Identifie les 3 principaux postes de dépenses

IA : 💰 Analyse des Dépenses 2024 (Jan-Mar)

📊 Top 3 Postes de Dépenses :

1. 🏢 LOYERS ET CHARGES (42% du total)
   • Total : 1,350,000 DA
   • Détail :
     - Bureau Alger : 450,000 DA (3 mois x 150k)
     - Entrepôt Blida : 300,000 DA (3 mois x 100k)
     - Électricité/Eau : 150,000 DA
     - Internet/Télécom : 45,000 DA

   📈 Évolution : +12% vs T1 2023
   💡 Suggestion : Renégocier bail Alger (tarif élevé)

2. 💼 MASSE SALARIALE (35% du total)
   • Total : 1,125,000 DA
   • Détail :
     - 8 employés permanents : 960,000 DA
     - 2 prestataires : 165,000 DA

   📈 Évolution : +8% vs T1 2023
   ✅ Conforme : Budget RH respecté

3. 🚗 DÉPLACEMENTS & TRANSPORT (15% du total)
   • Total : 482,000 DA
   • Détail :
     - Carburant : 285,000 DA
     - Péages autoroute : 45,000 DA
     - Déplacements équipe : 152,000 DA

   📈 Évolution : +25% vs T1 2023 ⚠️
   🚨 Alerte : Hausse importante, à analyser !

💡 Recommandations :
1. Optimiser déplacements (covoiturage, visio)
2. Négocier tarifs loyers (économie potentielle 15%)
3. Budgétiser 2,500,000 DA pour T2 2024

📍 Source : Factures-2024.xlsx, Feuille "Dépenses", Lignes 5-342
```

---

### 4. **Support Client**

```
Uploadez : FAQs, guides utilisateur, historique tickets
Questions : Résolution problèmes, réponses standards
```

**Exemple :**

```
Agent Support : [Upload "FAQ-Produit.pdf" + "Historique-Tickets-2024.xlsx"]
                Client demande : "Mon appareil ne s'allume plus"

IA : 🔧 Solution Problème : Appareil ne s'allume pas

📋 Checklist de Diagnostic (FAQ, p.12) :

✅ 1. Vérifier alimentation électrique
   • Prise murale fonctionne ? (tester autre appareil)
   • Câble d'alimentation bien branché ?
   • LED indicateur allumé ? (vert = OK, rouge = erreur)

✅ 2. Vérifier bouton Power
   • Appuyer 5 secondes (reset forcé)
   • Essayer bouton façade + télécommande

✅ 3. Vérifier fusible interne
   • Débrancher appareil
   • Ouvrir trappe fusible (arrière)
   • Remplacer si grillé (fusible 5A fourni)

📊 Historique Similar Cases (Tickets 2024) :

• 73% résolus par reset forcé (Étape 2)
• 18% fusible grillé après coupure électricité
• 9% nécessitent intervention technicien

🎯 Solution Recommandée :

"Bonjour,

Merci pour votre message. Essayons ensemble ces 3 étapes rapides :

1️⃣ Débranchez l'appareil 30 secondes, puis rebranchez
2️⃣ Appuyez sur le bouton Power 5 secondes (reset)
3️⃣ Si toujours rien, vérifiez le fusible (trappe arrière)

📹 Vidéo tutoriel : https://iafactory.dz/support/reset

Si le problème persiste, je programme une intervention
gratuite sous 48h à votre domicile.

Cordialement,
Support IA Factory"

⏱️ Temps résolution : < 5 minutes (90% des cas)
💰 Économie : Évite déplacement technicien (2,500 DA)
```

---

## 🛠️ Dépannage

### Problèmes d'Upload

#### ❌ "Fichier trop volumineux"

```
Solution :
1. Vérifiez les limites (voir section Limites d'Upload)
2. Compressez le PDF : https://www.ilovepdf.com/compress_pdf
3. Divisez le fichier en plusieurs parties
4. Passez au plan supérieur (Plus de stockage)
```

---

#### ❌ "Format non supporté"

```
Solution :
1. Convertissez au format supporté :
   • PDF pour documents
   • PNG/JPG pour images
   • MP4 pour vidéos

2. Outils de conversion gratuits :
   • https://convertio.co (tous formats)
   • LibreOffice (Word → PDF)
   • HandBrake (vidéos)
```

---

#### ❌ "Échec de vectorisation"

```
Solution :
1. Vérifiez que le document contient du texte extractible
2. Si scan, utilisez OCR d'abord : https://www.onlineocr.net
3. Essayez à nouveau après 5 minutes (timeout réseau)
4. Contactez support@iafactory.dz si persiste
```

---

### Problèmes de Qualité

#### 📉 "Réponses imprécises"

```
Solution :
1. Vérifiez que le bon document est sélectionné
2. Posez des questions plus spécifiques :
   ❌ "Parle-moi du contrat"
   ✅ "Quelle est la date de fin du contrat ?"

3. Augmentez le nombre de chunks (Paramètres RAG)
4. Activez le reranking (améliore pertinence +15%)
```

---

#### 🔍 "Document non trouvé"

```
Solution :
1. Attendez 30 secondes après upload (vectorisation)
2. Vérifiez que le document n'est pas supprimé
3. Rafraîchissez la page (F5)
4. Vérifiez les permissions (documents partagés)
```

---

#### 🌐 "OCR de mauvaise qualité"

```
Solution :
1. Uploadez des scans haute résolution (300 DPI min)
2. Évitez documents flous ou mal contrastés
3. Redressez les pages avant scan
4. Utilisez des PDFs natifs quand possible (99% précision)
```

---

## 📞 Support

### Obtenir de l'Aide

```
📧 Email : support@iafactory.dz
💬 Chat : Hub IA → 💬 Support (24/7)
📱 WhatsApp : +213 560 XX XX XX
📞 Téléphone : +213 21 XX XX XX (Lun-Ven 9h-18h)
```

### Documentation Complémentaire

- 📚 [Guide Complet RAG](GESTION_DOCUMENTS.md)
- 🔐 [Sécurité et Confidentialité](SECURITE_DONNEES.md)
- 🔌 [Connecteurs et MCP](CONNECTEURS_IAFACTORY.md)
- 💰 [Tarification et Crédits](FACTURATION_TARIFICATION.md)

---

**🇩🇿 IA Factory - L'Intelligence Artificielle Made in Algeria**

*Documentation mise à jour : Janvier 2025*
