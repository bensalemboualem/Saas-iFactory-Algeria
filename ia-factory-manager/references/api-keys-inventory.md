# 🔑 Inventaire Clés API - IA Factory

> ⚠️ **CE FICHIER NE CONTIENT PAS LES CLÉS** - Seulement leur emplacement
> Dernière mise à jour: 2026-01-28

## Règles de Gestion des Clés

1. **UNE clé par service par projet** - Ne JAMAIS réutiliser entre Algérie/Suisse
2. **Stockage sécurisé** - Fichier .env local + gestionnaire de secrets
3. **Rotation** - Changer les clés tous les 90 jours minimum
4. **Backup** - Noter les clés dans gestionnaire de mots de passe

---

## 🤖 LLM Providers

### OpenAI
| Projet | Variable Env | Où trouver | Status |
|--------|--------------|------------|--------|
| IA Factory Algeria | `OPENAI_API_KEY` | .env.algeria | ✅ Active |
| IA Factory Suisse | `OPENAI_API_KEY` | .env.suisse | ✅ Active |
| BOLT-PLUS IDE | `OPENAI_API_KEY` | .env.bolt | ⚠️ Vérifier |
| RAG System | `OPENAI_API_KEY` | .env.rag | ⚠️ Vérifier |
| Video Studio | `OPENAI_API_KEY` | .env.video | ⚠️ Vérifier |

**Où créer:** https://platform.openai.com/api-keys

### Anthropic (Claude)
| Projet | Variable Env | Où trouver | Status |
|--------|--------------|------------|--------|
| IA Factory Algeria | `ANTHROPIC_API_KEY` | .env.algeria | ✅ Active |
| IA Factory Suisse | `ANTHROPIC_API_KEY` | .env.suisse | ✅ Active |
| BOLT-PLUS IDE | `ANTHROPIC_API_KEY` | .env.bolt | ⚠️ Vérifier |
| Interview Agents | `ANTHROPIC_API_KEY` | .env.interview | ⚠️ Vérifier |

**Où créer:** https://console.anthropic.com/settings/keys

### Google AI (Gemini)
| Projet | Variable Env | Où trouver | Status |
|--------|--------------|------------|--------|
| IA Factory Algeria | `GOOGLE_AI_API_KEY` | .env.algeria | ✅ Active |
| IA Factory Suisse | `GOOGLE_AI_API_KEY` | .env.suisse | ✅ Active |

**Où créer:** https://aistudio.google.com/app/apikey

### Groq
| Projet | Variable Env | Où trouver | Status |
|--------|--------------|------------|--------|
| IA Factory Algeria | `GROQ_API_KEY` | .env.algeria | ✅ Active |

**Où créer:** https://console.groq.com/keys

---

## 💳 Payment Providers

### Chargily Pay (Algérie UNIQUEMENT 🇩🇿)
| Projet | Variable Env | Où trouver | Status |
|--------|--------------|------------|--------|
| IA Factory Algeria | `CHARGILY_API_KEY` | .env.algeria | ✅ Active |
| IA Factory Algeria | `CHARGILY_SECRET_KEY` | .env.algeria | ✅ Active |

**Où créer:** https://pay.chargily.com/dashboard
**Note:** NE JAMAIS utiliser dans projet Suisse

### Stripe (Suisse UNIQUEMENT 🇨🇭)
| Projet | Variable Env | Où trouver | Status |
|--------|--------------|------------|--------|
| IA Factory Suisse | `STRIPE_PUBLIC_KEY` | .env.suisse | ✅ Active |
| IA Factory Suisse | `STRIPE_SECRET_KEY` | .env.suisse | ✅ Active |
| IA Factory Suisse | `STRIPE_WEBHOOK_SECRET` | .env.suisse | ✅ Active |

**Où créer:** https://dashboard.stripe.com/apikeys
**Note:** NE JAMAIS utiliser dans projet Algérie

---

## 🎬 Media & Video

### Replicate
| Projet | Variable Env | Où trouver | Status |
|--------|--------------|------------|--------|
| Video Studio | `REPLICATE_API_TOKEN` | .env.video | ⚠️ Problèmes |

**Où créer:** https://replicate.com/account/api-tokens
**Modèles utilisés:** Wan 2.1, CogVideoX-5B

---

## 🗄️ Database & Vector DB

### Pinecone
| Projet | Variable Env | Où trouver | Status |
|--------|--------------|------------|--------|
| RAG System | `PINECONE_API_KEY` | .env.rag | ⚠️ Vérifier |
| RAG System | `PINECONE_ENVIRONMENT` | .env.rag | ⚠️ Vérifier |

**Où créer:** https://app.pinecone.io/

### Qdrant (Alternative)
| Projet | Variable Env | Où trouver | Status |
|--------|--------------|------------|--------|
| RAG System | `QDRANT_URL` | .env.rag | ❓ À configurer |
| RAG System | `QDRANT_API_KEY` | .env.rag | ❓ À configurer |

---

## 📧 Services Tiers

### Database (PostgreSQL/Supabase)
| Projet | Variable Env | Où trouver | Status |
|--------|--------------|------------|--------|
| IA Factory Algeria | `DATABASE_URL` | .env.algeria | ✅ Active |
| IA Factory Suisse | `DATABASE_URL` | .env.suisse | ✅ Active |

---

## ⚠️ Checklist Audit Clés

### À faire MAINTENANT:
- [ ] Vérifier toutes les clés marquées ⚠️
- [ ] Confirmer que Chargily N'EST PAS dans .env.suisse
- [ ] Confirmer que Stripe N'EST PAS dans .env.algeria
- [ ] Mettre à jour les chemins /path/to/ dans projects.json
- [ ] Sauvegarder toutes les clés actives dans gestionnaire de mots de passe

### Audit Mensuel:
- [ ] Vérifier les clés inutilisées
- [ ] Rotation des clés > 90 jours
- [ ] Supprimer les clés des projets abandonnés
- [ ] Mettre à jour ce document

---

## 🚨 En Cas de Fuite

1. **Révoquer immédiatement** la clé compromise
2. **Générer nouvelle clé** sur le dashboard du service
3. **Mettre à jour** le .env du projet concerné
4. **Vérifier logs** pour utilisation non autorisée
5. **Documenter** l'incident dans ce fichier
