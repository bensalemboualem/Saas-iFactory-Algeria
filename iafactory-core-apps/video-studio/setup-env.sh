#!/bin/bash

# ============================================
# 🔑 CONFIGURATION AUTOMATIQUE .ENV
# IAFactory Video Studio Pro
# ============================================

set -e

echo "🔑 Configuration automatique du fichier .env..."
echo ""

# Vérifier qu'on est dans le bon dossier
if [ ! -f ".env.ready" ]; then
    echo "❌ Fichier .env.ready non trouvé"
    echo "   Assurez-vous d'être dans le dossier video-studio/"
    exit 1
fi

# ============================================
# GÉNÉRER LES SECRETS
# ============================================
echo "🔐 Génération des secrets JWT..."

JWT_SECRET=$(openssl rand -base64 32)
NEXTAUTH_SECRET=$(openssl rand -base64 32)

echo "✅ Secrets générés:"
echo "   JWT_SECRET=$JWT_SECRET"
echo "   NEXTAUTH_SECRET=$NEXTAUTH_SECRET"
echo ""

# ============================================
# DEMANDER INFOS MANQUANTES
# ============================================
echo "📝 Configuration des derniers éléments..."
echo ""

# ElevenLabs
read -p "Clé ElevenLabs (ou 'skip' pour passer): " ELEVENLABS_KEY
if [ "$ELEVENLABS_KEY" = "skip" ]; then
    ELEVENLABS_KEY="AJOUTER_CLE_ELEVENLABS"
fi

echo ""

# Cloudflare R2
echo "🗄️  Configuration Cloudflare R2..."
read -p "Access Key R2 (ou 'skip'): " R2_ACCESS
read -p "Secret Key R2 (ou 'skip'): " R2_SECRET
read -p "Endpoint R2 (ex: https://xxxxx.r2.cloudflarestorage.com, ou 'skip'): " R2_ENDPOINT

if [ "$R2_ACCESS" = "skip" ]; then R2_ACCESS="AJOUTER_R2_ACCESS_KEY"; fi
if [ "$R2_SECRET" = "skip" ]; then R2_SECRET="AJOUTER_R2_SECRET_KEY"; fi
if [ "$R2_ENDPOINT" = "skip" ]; then R2_ENDPOINT="https://ACCOUNT_ID.r2.cloudflarestorage.com"; fi

echo ""

# Stripe
echo "💳 Configuration Stripe..."
read -p "Stripe Publishable Key (pk_live_xxx, ou 'skip'): " STRIPE_PUB
read -p "Stripe Secret Key (sk_live_xxx, ou 'skip'): " STRIPE_SEC
read -p "Stripe Webhook Secret (whsec_xxx, ou 'skip'): " STRIPE_HOOK

if [ "$STRIPE_PUB" = "skip" ]; then STRIPE_PUB="pk_live_AJOUTER_CLE"; fi
if [ "$STRIPE_SEC" = "skip" ]; then STRIPE_SEC="sk_live_AJOUTER_CLE"; fi
if [ "$STRIPE_HOOK" = "skip" ]; then STRIPE_HOOK="whsec_AJOUTER_SECRET"; fi

echo ""

# ============================================
# CRÉER LE FICHIER .ENV
# ============================================
echo "📄 Création du fichier .env..."

# Copier .env.ready vers .env
cp .env.ready .env

# Remplacer les valeurs
sed -i "s|GENERER_SECRET_JWT_ICI|$JWT_SECRET|g" .env
sed -i "s|GENERER_SECRET_NEXTAUTH_ICI|$NEXTAUTH_SECRET|g" .env
sed -i "s|VOTRE_CLE_ELEVENLABS_ICI|$ELEVENLABS_KEY|g" .env
sed -i "s|VOTRE_ACCESS_KEY_R2|$R2_ACCESS|g" .env
sed -i "s|VOTRE_SECRET_KEY_R2|$R2_SECRET|g" .env
sed -i "s|https://ACCOUNT_ID.r2.cloudflarestorage.com|$R2_ENDPOINT|g" .env
sed -i "s|pk_live_VOTRE_CLE|$STRIPE_PUB|g" .env
sed -i "s|sk_live_VOTRE_CLE|$STRIPE_SEC|g" .env
sed -i "s|whsec_VOTRE_SECRET|$STRIPE_HOOK|g" .env

echo "✅ Fichier .env créé!"
echo ""

# ============================================
# VÉRIFICATION
# ============================================
echo "🧪 Vérification du fichier .env..."

# Compter les clés configurées
TOTAL_KEYS=$(grep -c "_KEY\|_SECRET\|_TOKEN" .env || true)
MISSING_KEYS=$(grep -c "AJOUTER\|VOTRE_CLE\|GENERER" .env || true)

echo ""
echo "📊 Statistiques:"
echo "   Total de clés API: $TOTAL_KEYS"
echo "   Clés configurées: $((TOTAL_KEYS - MISSING_KEYS))"
echo "   Clés manquantes: $MISSING_KEYS"
echo ""

if [ "$MISSING_KEYS" -eq 0 ]; then
    echo "✅ Toutes les clés sont configurées!"
else
    echo "⚠️  Quelques clés restent à configurer:"
    grep -E "AJOUTER|VOTRE_CLE|GENERER" .env | head -5
    echo ""
    echo "   Vous pouvez éditer manuellement:"
    echo "   nano .env"
fi

echo ""

# ============================================
# SÉCURITÉ
# ============================================
echo "🔒 Sécurisation du fichier .env..."
chmod 600 .env
echo "✅ Permissions 600 appliquées (lecture/écriture propriétaire uniquement)"
echo ""

# ============================================
# RÉSUMÉ
# ============================================
echo "============================================"
echo "✅ CONFIGURATION TERMINÉE"
echo "============================================"
echo ""
echo "📁 Fichier créé: .env"
echo ""
echo "🔑 Secrets générés automatiquement:"
echo "   • JWT_SECRET"
echo "   • NEXTAUTH_SECRET"
echo ""
echo "✅ Clés API configurées:"
echo "   • Anthropic (Claude)"
echo "   • OpenAI"
echo "   • Groq, Gemini, Mistral, DeepSeek, Cohere"
echo "   • Kling AI, Luma AI, Runway ML, MiniMax, Pika"
echo "   • Replicate, Stability AI"
echo "   • Qwen (Alibaba Cloud)"
echo "   • Google Translate"
if [ "$ELEVENLABS_KEY" != "AJOUTER_CLE_ELEVENLABS" ]; then
    echo "   • ElevenLabs ✅"
else
    echo "   • ElevenLabs ⚠️  (à configurer)"
fi
if [ "$R2_ACCESS" != "AJOUTER_R2_ACCESS_KEY" ]; then
    echo "   • Cloudflare R2 ✅"
else
    echo "   • Cloudflare R2 ⚠️  (à configurer)"
fi
if [ "$STRIPE_PUB" != "pk_live_AJOUTER_CLE" ]; then
    echo "   • Stripe ✅"
else
    echo "   • Stripe ⚠️  (à configurer)"
fi
echo ""
echo "📝 Pour éditer le .env:"
echo "   nano .env"
echo ""
echo "🚀 Prochaine étape:"
echo "   docker-compose up -d --build"
echo ""
echo "============================================"
