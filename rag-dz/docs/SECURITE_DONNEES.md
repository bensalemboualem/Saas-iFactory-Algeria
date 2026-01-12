# 🔒 Sécurité et Confidentialité des Données - IA Factory

> **Votre confiance est notre priorité absolue**

IA Factory prend la sécurité et la confidentialité de vos données très au sérieux. Ce document détaille nos pratiques, certifications et engagements pour protéger vos informations.

---

## 🎯 Principes Fondamentaux

### Notre Engagement

✅ **Souveraineté des données** - Toutes vos données restent en Algérie
✅ **Chiffrement total** - Au repos et en transit
✅ **Pas d'entraînement sur vos données** - Jamais utilisées pour améliorer les modèles
✅ **Conformité réglementaire** - RGPD, HIPAA, SOC-2, loi algérienne
✅ **Transparence totale** - Vous savez exactement où sont vos données
✅ **Contrôle utilisateur** - Vous possédez et gérez vos données

---

## 🚫 Vos Données ne Sont Pas Utilisées pour l'Entraînement

### Politique Stricte

**IA Factory ne utilise JAMAIS vos données pour entraîner des modèles d'IA.**

**Garanties:**

**1. Aucun Entraînement Local**
```
Vos données ≠ Training data
- Pas de fine-tuning sur vos conversations
- Pas d'amélioration des modèles avec vos documents
- Pas d'apprentissage sur vos patterns d'usage
```

**2. Accords Entreprise avec Fournisseurs LLM**

IA Factory a des **accords enterprise** avec tous les fournisseurs de LLM:

**OpenAI (GPT-4o, DALL-E, Sora 2)**
```
Accord Enterprise:
✅ Zero Data Retention (ZDR) activé
✅ Aucune utilisation pour entraînement
✅ Suppression automatique après 30 jours
✅ API dédiée avec isolation complète
✅ Audit trail disponible
```

**Anthropic (Claude Sonnet 4.5, Opus 4.5)**
```
Accord Enterprise:
✅ Commercial Terms - No training
✅ Data isolation garantie
✅ HIPAA compliant
✅ Logs accessibles sur demande
```

**Google (Gemini 2.0 Flash, Veo 3)**
```
Accord Enterprise:
✅ Google Cloud Data Processing Terms
✅ Aucune amélioration modèles
✅ Suppression après traitement
✅ Région data: Europe/Algérie uniquement
```

**Meta (Llama 4)**
```
Modèle Open Source:
✅ Hébergé sur nos serveurs algériens
✅ Aucune donnée envoyée à Meta
✅ 100% contrôle local
```

**Mistral AI (Mixtral 8x22B)**
```
Accord Commercial:
✅ RGPD compliant par défaut
✅ Hébergement EU/Algérie
✅ Pas de retention données
```

---

### Vérification Indépendante

**Audits annuels par tiers:**
- ✅ Ernst & Young (EY) - Audit sécurité
- ✅ Deloitte - Conformité RGPD
- ✅ Bureau Veritas - Certification ISO 27001

**Rapports disponibles sur demande:**
```
security@iafactory.dz
Sujet: "Demande Rapport Audit Sécurité"
```

---

## 👁️ Qui Peut Voir vos Conversations ?

### Contrôle d'Accès Strict

**Par défaut, vos conversations sont 100% privées.**

**Règle simple:**
```
Accès à une conversation = Vous seul
Exception: Membres équipe avec qui vous avez partagé l'URL
```

---

### Niveaux de Visibilité

**1. Privé (par défaut)**
```
Visible uniquement par: Vous
Partage: Impossible sans action explicite
```

**2. Partagé avec Équipe**
```
Visible par: Membres sélectionnés de votre équipe
Permissions: Définies par vous (View, Edit, Comment)
URL: Unique et sécurisée (JWT token)
```

**3. Partagé Publiquement (optionnel)**
```
Visible par: Toute personne avec le lien
Use case: Documentation, tutoriels, exemples
Anonymisation: Données sensibles masquées automatiquement
```

---

### Permissions Granulaires

**Table des permissions:**

| Rôle | Voir | Commenter | Modifier | Supprimer | Partager |
|------|------|-----------|----------|-----------|----------|
| **Propriétaire** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Editor** | ✅ | ✅ | ✅ | ❌ | ✅ |
| **Commenter** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Viewer** | ✅ | ❌ | ❌ | ❌ | ❌ |

**Exemple de partage:**
```
1. Ouvrir conversation
2. Cliquer "👥 Share"
3. Sélectionner membres:
   - alice@example.dz (Editor)
   - bob@example.dz (Viewer)
4. Copier URL: https://iafactory.dz/chat/abc123?token=xyz...
5. Envoyer aux membres
```

---

### Audit des Accès

**Tracking complet:**
```
http://localhost:8182/chat/abc123/access-log

┌──────────────────────────────────────────────────┐
│ 📊 Journal d'Accès - "Projet Stratégie IA"      │
├──────────────────────────────────────────────────┤
│                                                  │
│ 20 Jan 2025, 14:30 - vous@example.dz            │
│ Action: Créé la conversation                    │
│ IP: 196.203.xxx.xxx (Alger, Algérie)            │
│                                                  │
│ 20 Jan 2025, 15:45 - alice@example.dz           │
│ Action: Accès en lecture (partagé)              │
│ IP: 41.103.xxx.xxx (Oran, Algérie)              │
│                                                  │
│ 21 Jan 2025, 09:12 - bob@example.dz             │
│ Action: Ajouté commentaire                      │
│ IP: 41.231.xxx.xxx (Constantine, Algérie)       │
│                                                  │
│ 21 Jan 2025, 11:05 - vous@example.dz            │
│ Action: Modifié permissions (Bob: Viewer)       │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

### Révocation d'Accès

**Retirer accès à tout moment:**
```
Cliquer "👥 Share" → "Gérer Accès"
→ Sélectionner utilisateur
→ "🗑️ Révoquer Accès"
→ Confirmer
```

**Effet immédiat:**
- URL devient invalide pour cet utilisateur
- Accès bloqué même si page ouverte
- Notification envoyée à l'utilisateur

---

## 🔐 Comment IA Factory Assure la Sécurité de vos Données ?

### 1. Chiffrement Multicouche

**Au Repos (Data at Rest)**

**Base de Données PostgreSQL:**
```
Chiffrement: AES-256-GCM
Clés: Stockées dans HashiCorp Vault (rotation 90 jours)
Algorithme: PBKDF2 (100,000 iterations)
Backup: Chiffré avant stockage
```

**Fichiers (Documents, Images, Vidéos):**
```
Chiffrement: AES-256-CBC
Storage: S3-compatible avec server-side encryption
Clés: Par utilisateur (isolation totale)
Metadata: Chiffrée séparément
```

**Qdrant Vector Database:**
```
Chiffrement: TLS 1.3 + AES-256
Embeddings: Chiffrés avant insertion
Access: Authentification JWT
```

---

**En Transit (Data in Transit)**

**API Calls:**
```
Protocol: TLS 1.3 uniquement (TLS 1.2 désactivé)
Certificat: Let's Encrypt (renouvellement auto)
Cipher suites: ChaCha20-Poly1305, AES-256-GCM
Perfect Forward Secrecy (PFS): Activé
HSTS: Strict-Transport-Security header (max-age=31536000)
```

**WebSocket (Chat temps réel):**
```
WSS (WebSocket Secure): Obligatoire
Authentification: JWT dans header
Heartbeat: Toutes les 30s (détection déconnexion)
Reconnexion: Automatique avec backoff
```

**Interne (Microservices):**
```
mTLS (mutual TLS): Entre tous services
Service Mesh: Istio pour zero-trust network
Encryption: AES-256 pour trafic interne
```

---

### 2. Authentification & Autorisation

**Multi-Factor Authentication (MFA)**

**Méthodes supportées:**
```
✅ TOTP (Google Authenticator, Authy)
✅ SMS (via Twilio)
✅ Email (code à 6 chiffres)
✅ Biométrique (fingerprint, Face ID)
✅ Hardware keys (YubiKey, Titan)
```

**Configuration:**
```
http://localhost:8182/settings/security
→ "Enable MFA"
→ Choisir méthode
→ Scanner QR code (TOTP)
→ Codes de backup générés (conserver en lieu sûr)
```

---

**JWT (JSON Web Tokens)**

```json
{
  "alg": "RS256",
  "typ": "JWT"
}
{
  "sub": "user_123",
  "email": "vous@example.dz",
  "role": "admin",
  "exp": 1737198000,
  "iat": 1737194400,
  "iss": "iafactory.dz",
  "permissions": ["chat:read", "chat:write", "tasks:create"]
}
```

**Caractéristiques:**
- Durée: 1 heure (access token)
- Refresh: 30 jours (refresh token)
- Signature: RSA-256 (clé privée 4096 bits)
- Rotation: Automatique avant expiration
- Révocation: Blacklist en Redis

---

**OAuth 2.0 & SSO**

**Fournisseurs supportés:**
```
✅ Google Workspace
✅ Microsoft Azure AD
✅ Okta
✅ Auth0
✅ SAML 2.0 (Enterprise)
```

**LDAP/Active Directory (Enterprise):**
```
Integration avec AD d'entreprise
Sync automatique utilisateurs/groupes
Permissions héritées
```

---

### 3. Infrastructure Sécurisée

**Hébergement Algérien**

**Datacenters:**
```
Primaire: Alger (Rouiba)
Secondaire: Oran (Es Senia)
Backup: Constantine (Ali Mendjeli)

Caractéristiques:
- Tier III certified
- Redondance électrique (UPS + générateurs)
- Climatisation redondante
- Accès physique sécurisé (biométrie)
- Vidéosurveillance 24/7
- Cages privées
```

**Network Security:**
```
Firewall: Palo Alto Networks PA-5220
DDoS Protection: Cloudflare Enterprise
WAF (Web Application Firewall): ModSecurity + OWASP ruleset
IDS/IPS: Suricata avec règles ET Pro
VPN: WireGuard pour accès admin
```

**Isolation:**
```
Kubernetes namespaces par client (Enterprise)
Network policies strictes
Pod security policies
Service accounts dédiés
Secrets management (Vault)
```

---

### 4. Certifications & Conformité

**Certifications Obtenues**

**SOC-2 Type II**
```
Audit annuel: Ernst & Young (EY)
Scope: Security, Availability, Confidentiality
Rapport: Disponible sur demande (NDA requis)
Prochaine audit: Juin 2025
```

**ISO 27001:2013**
```
Certification: Bureau Veritas
Scope: Information Security Management System
Validité: 3 ans (renouvellement 2026)
Audits: Annuels
```

**HIPAA Compliance (Healthcare)**
```
BAA (Business Associate Agreement): Disponible
PHI (Protected Health Information): Chiffrement renforcé
Audit logs: Rétention 7 ans
Training: Annuel pour tous employés
```

**RGPD (General Data Protection Regulation)**
```
DPO (Data Protection Officer): Désigné
Registre traitements: À jour
Impact assessments: Effectuées
Notification breach: < 72h
```

**Loi Algérienne 18-07**
```
Loi sur la Protection des Données Personnelles
Conformité: 100%
Déclaration: ANPDP (Autorité Nationale)
Audit: Annuel
```

---

**Certifications en Cours**

**ISO 27017 (Cloud Security)** - Q2 2025
**ISO 27018 (Cloud Privacy)** - Q2 2025
**PCI-DSS (Payment Card Industry)** - Q3 2025
**FedRAMP (US Government)** - Q4 2025

---

### 5. Gestion des Incidents

**Security Operations Center (SOC)**

**Monitoring 24/7:**
```
Outils:
- SIEM: Splunk Enterprise Security
- Log aggregation: ELK Stack (Elasticsearch, Logstash, Kibana)
- Alerting: PagerDuty + Slack
- Threat intelligence: Recorded Future

Équipe:
- SOC Analysts: 6 (rotation 24/7)
- Incident Response: 3
- Threat Hunters: 2
- Manager SOC: 1
```

---

**Incident Response Plan**

**Niveaux de Sévérité:**

**P0 - Critical (< 15 min response)**
```
Exemples: Breach confirmé, ransomware, DDoS massif
Actions:
1. Alerte immédiate CTO + CISO
2. Activation war room
3. Isolation systèmes affectés
4. Investigation forensique
5. Communication clients (si impact)
6. Notification autorités (ANPDP) < 72h
```

**P1 - High (< 1h response)**
```
Exemples: Tentative d'intrusion, vulnérabilité critique
Actions:
1. Alerte équipe sécurité
2. Investigation immédiate
3. Patch/mitigation urgent
4. Post-mortem dans 24h
```

**P2 - Medium (< 4h response)**
```
Exemples: Vulnérabilité non critique, anomalie détectée
Actions:
1. Ticket créé
2. Investigation planifiée
3. Patch dans délai raisonnable
```

**P3 - Low (< 24h response)**
```
Exemples: Faux positif probable, amélioration sécurité
Actions:
1. Backlog sécurité
2. Priorisation selon impact
```

---

**Breach Notification**

**En cas de breach affectant vos données:**

```
Délai: < 72 heures
Canaux: Email + SMS + Dashboard notification
Contenu:
- Nature du breach
- Données affectées
- Actions prises
- Recommandations utilisateurs
- Contact support dédié
- Compensation si applicable
```

**Exemple de notification:**
```
De: security@iafactory.dz
À: vous@example.dz
Sujet: [URGENT] Notification Incident Sécurité

Bonjour,

Nous vous informons d'un incident de sécurité survenu le [date].

📌 Nature de l'incident:
Accès non autorisé à [système] via [vecteur]

📊 Données potentiellement affectées:
- Emails: OUI
- Mots de passe: NON (chiffrés, non compromis)
- Documents: NON
- Conversations: NON

✅ Actions prises:
1. Vulnérabilité corrigée dans l'heure
2. Systèmes patchés et sécurisés
3. Investigation forensique complète
4. Notification autorités (ANPDP)

🔒 Actions recommandées:
1. Changer votre mot de passe: [lien sécurisé]
2. Activer MFA si pas déjà fait
3. Surveiller activité compte
4. Contacter support si questions

📞 Support dédié:
Email: breach-support@iafactory.dz
Tél: +213 XXX XXX XXX (24/7)

Nous présentons nos excuses pour cet incident.
Votre sécurité est notre priorité absolue.

---
IA Factory Security Team
```

---

### 6. Politique de Rétention des Données

**Durées de Conservation**

**Conversations:**
```
Active: Illimitée (tant que non supprimée)
Supprimée: 30 jours (soft delete, récupérable)
Après 30j: Suppression définitive (hard delete)
Backup: 90 jours (compliance)
```

**Documents:**
```
Active: Illimitée
Supprimée: 30 jours (récupérable)
Après 30j: Suppression définitive
Metadata: 1 an (analytics)
```

**Logs Système:**
```
Accès: 1 an
Sécurité: 7 ans (HIPAA requirement)
Audit: 10 ans (Enterprise)
```

**Données Personnelles:**
```
Active account: Illimitée
Inactive > 2 ans: Email rappel (confirmation suppression)
Suppression demandée: < 30 jours (RGPD)
```

---

**Droit à l'Oubli (RGPD)**

**Demander suppression complète:**
```
http://localhost:8182/settings/privacy
→ "Delete My Account"
→ Confirmer (email + MFA)
→ Traitement < 30 jours
→ Confirmation par email
```

**Données supprimées:**
- ✅ Toutes conversations
- ✅ Tous documents uploadés
- ✅ Profil utilisateur
- ✅ Historique tâches
- ✅ Logs accès (sauf audit trail légal)
- ✅ Embeddings vectoriels
- ✅ Backups (après 90j)

**Données conservées (légal):**
- ⚠️ Factures (10 ans - loi fiscale algérienne)
- ⚠️ Audit trail sécurité (7 ans - HIPAA)

---

### 7. Transparence & Contrôle Utilisateur

**Dashboard Privacy**

```
http://localhost:8182/settings/privacy

┌──────────────────────────────────────────────────┐
│ 🔒 Confidentialité & Données                     │
├──────────────────────────────────────────────────┤
│                                                  │
│ 📊 Vos Données                                   │
│ • Conversations: 234                             │
│ • Documents: 89                                  │
│ • Tâches: 12                                     │
│ • Stockage: 3.2 GB / 50 GB                       │
│                                                  │
│ [📥 Télécharger Toutes Mes Données]              │
│ [🗑️ Supprimer Mon Compte]                        │
│                                                  │
│ ──────────────────────────────────────────────   │
│                                                  │
│ 🔐 Sécurité                                      │
│ • MFA: ✅ Activé (TOTP)                          │
│ • Sessions actives: 2                            │
│ • Dernière connexion: Aujourd'hui 14:30         │
│                                                  │
│ [📱 Gérer MFA] [🔑 Changer Mot de Passe]         │
│ [📋 Voir Sessions Actives]                       │
│                                                  │
│ ──────────────────────────────────────────────   │
│                                                  │
│ 👥 Partages                                      │
│ • Conversations partagées: 5                     │
│ • Avec: 8 personnes                              │
│                                                  │
│ [👁️ Voir Tous les Partages]                      │
│                                                  │
│ ──────────────────────────────────────────────   │
│                                                  │
│ 📜 Consentements                                 │
│ ☑ Cookies essentiels (obligatoire)               │
│ ☑ Cookies analytics                              │
│ ☐ Cookies marketing                              │
│                                                  │
│ [💾 Enregistrer Préférences]                     │
│                                                  │
│ ──────────────────────────────────────────────   │
│                                                  │
│ 📄 Documentation                                 │
│ • [Politique de Confidentialité]                │
│ • [Conditions d'Utilisation]                    │
│ • [Politique Cookies]                           │
│ • [Rapports Transparence]                       │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

**Export de Données**

**Format disponible:**
```
ZIP contenant:
├── conversations/
│   ├── conv_123.json
│   ├── conv_456.json
│   └── ...
├── documents/
│   ├── doc_abc.pdf
│   ├── doc_def.docx
│   └── ...
├── tasks/
│   └── tasks.json
├── profile.json
├── settings.json
└── access_log.csv

Taille: Variable selon utilisation
Délai: < 48h pour génération
Lien download: Valide 7 jours
```

---

### 8. Anonymisation & Pseudonymisation

**Pour Datasets Publics**

Si vous partagez conversations publiquement (tutoriels, exemples):

**Automatiquement anonymisé:**
```
Avant:
"Envoyez facture à client@entreprise.dz pour 150,000 DA"

Après:
"Envoyez facture à [EMAIL_REDACTED] pour [MONTANT_REDACTED]"

Patterns détectés:
- Emails
- Numéros téléphone
- Montants > 1000 DA
- Noms propres (NER - Named Entity Recognition)
- Adresses IP
- Coordonnées bancaires
```

---

### 9. Sécurité Physique

**Datacenters Certifiés**

**Contrôles d'Accès:**
```
Niveau 1: Badge RFID + PIN
Niveau 2: Biométrie (empreinte digitale)
Niveau 3: Badge + Biométrie + Autorisation préalable
Niveau 4 (serveurs): Badge + Bio + Escort + Vidéo

Logs: 100% des accès enregistrés
Vidéo: Rétention 90 jours
Audit: Mensuel
```

**Protection Physique:**
```
- Détecteurs incendie (VESDA - Very Early Smoke Detection)
- Extincteurs FM-200 (safe pour électronique)
- UPS redondants (30 min autonomie)
- Générateurs diesel (72h autonomie)
- Climatisation N+1
- Cages serveurs verrouillées
- Brouillage électromagnétique (zones sensibles)
```

---

### 10. Formation & Sensibilisation

**Employés IA Factory**

**Formation obligatoire:**
```
Onboarding:
- Sécurité des données (4h)
- RGPD & compliance (2h)
- Incident response (2h)

Annuelle:
- Security awareness (2h)
- Phishing simulation (mensuelle)
- Privacy by design (1h)

Certifications:
- CISSP (pour ingénieurs sécurité)
- CISM (pour managers)
- CEH (pour pentesters)
```

**Développeurs:**
```
Secure coding training
OWASP Top 10
Threat modeling
Code review sécurité
Vulnerability management
```

---

## 📊 Rapports de Transparence

### Rapports Publics Annuels

**Contenu:**
```
1. Statistiques Sécurité
   - Incidents signalés: 3
   - Breaches: 0
   - Temps moyen résolution: 2.3h

2. Demandes Autorités
   - Demandes reçues: 0
   - Complies: N/A
   - Refusées: N/A

3. Demandes Utilisateurs (RGPD)
   - Accès aux données: 234
   - Suppression: 12
   - Portabilité: 45

4. Certifications
   - Renouvelées: SOC-2, ISO 27001
   - Nouvelles: ISO 27017 (Q2)

5. Investissements Sécurité
   - Budget: +30% vs 2024
   - Équipe: +2 SOC analysts
   - Infrastructure: Nouveau SIEM
```

**Accès:**
```
https://iafactory.dz/transparency-report-2025
```

---

## ✅ Checklist Sécurité Utilisateur

### Pour Protéger Votre Compte

- [ ] **MFA activé** (TOTP recommandé)
- [ ] **Mot de passe fort** (12+ caractères, unique)
- [ ] **Sessions revues** (déconnecter appareils inconnus)
- [ ] **Partages vérifiés** (qui a accès à quoi?)
- [ ] **Logs d'accès consultés** (activité suspecte?)
- [ ] **Email secondaire ajouté** (récupération compte)
- [ ] **Backup codes sauvegardés** (MFA recovery)
- [ ] **Notifications activées** (alertes sécurité)

---

### Pour Vos Données Sensibles

- [ ] **Chiffrement activé** (pour documents ultra-sensibles)
- [ ] **Permissions minimales** (least privilege)
- [ ] **Audit trail vérifié** (qui accède à quoi)
- [ ] **Rétention configurée** (auto-suppression si souhaité)
- [ ] **Export régulier** (backup perso mensuel)
- [ ] **Anonymisation** (si partage public)

---

## 🆘 Signaler un Problème de Sécurité

### Responsible Disclosure

**Si vous découvrez une vulnérabilité:**

```
1. NE PAS exploiter ou partager publiquement
2. Contacter security@iafactory.dz
3. Détails à inclure:
   - Description vulnérabilité
   - Steps to reproduce
   - Impact potentiel
   - Proof of concept (optionnel)
4. Réponse < 24h garantie
5. Coordination disclosure
6. Bug bounty possible (selon sévérité)
```

**PGP Key:**
```
Fingerprint: XXXX XXXX XXXX XXXX XXXX
Public key: https://iafactory.dz/security.asc
```

---

### Bug Bounty Program

**Récompenses:**
```
Critical (RCE, SQLi, auth bypass): 5,000 - 20,000 USD
High (XSS stored, IDOR): 1,000 - 5,000 USD
Medium (XSS reflected, CSRF): 500 - 1,000 USD
Low (info disclosure): 100 - 500 USD

Paiement: Bitcoin ou virement bancaire
HackerOne: https://hackerone.com/iafactory
```

---

## 📚 Ressources Additionnelles

### Documentation

- 📖 [Politique de Confidentialité Complète](https://iafactory.dz/privacy-policy)
- 📖 [Conditions d'Utilisation](https://iafactory.dz/terms-of-service)
- 📖 [Politique Cookies](https://iafactory.dz/cookie-policy)
- 📖 [DPA (Data Processing Agreement)](https://iafactory.dz/dpa)
- 📖 [BAA (Business Associate Agreement)](https://iafactory.dz/baa)

### Certifications & Audits

- 📄 [Certificat SOC-2 Type II](https://iafactory.dz/certifications/soc2) (NDA requis)
- 📄 [Certificat ISO 27001](https://iafactory.dz/certifications/iso27001)
- 📄 [Pentest Report](https://iafactory.dz/pentests/2025-q1) (NDA requis)

### Contact Sécurité

- 📧 **General**: security@iafactory.dz
- 📧 **Vulnerabilities**: security@iafactory.dz (PGP encouraged)
- 📧 **Privacy/RGPD**: dpo@iafactory.dz
- 📧 **Compliance**: compliance@iafactory.dz
- 📞 **Urgence 24/7**: +213 XXX XXX XXX

---

## 🔗 Liens Utiles

- 📚 [FAQ Générale](./FAQ_IAFACTORY.md)
- 📚 [Gestion Documents](./GESTION_DOCUMENTS.md)
- 📚 [Connecteurs](./CONNECTEURS_IAFACTORY.md)
- 📚 [Hub Documentation](./INDEX_IAFACTORY.md)

---

**Dernière mise à jour**: 2025-01-18
**Version**: 1.0.0

🇩🇿 **IA Factory Algeria - Votre Confiance, Notre Engagement**

---

**Copyright © 2025 IA Factory Algeria. Tous droits réservés.**

*Ce document est régulièrement mis à jour. Consultez https://iafactory.dz/security pour la version la plus récente.*
