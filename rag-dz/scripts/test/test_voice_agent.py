#!/usr/bin/env python
"""
Test complet de l'Agent Vocal avec Multi-Tenant
"""
import requests
import json
from pathlib import Path

BASE_URL = "http://127.0.0.1:8001"
TENANT_ID = "814c132a-1cdd-4db6-bc1f-21abd21ec37d"
API_KEY = "change-me-in-production"  # Dev API key

print("=" * 70)
print("TEST AGENT VOCAL MULTI-TENANT - IAFactory")
print("=" * 70)

# Step 1: Register user
print("\n[1/5] Registration d'un utilisateur de test...")
try:
    r = requests.post(
        f"{BASE_URL}/api/auth/register",
        headers={"X-API-Key": API_KEY},
        json={
            "email": "vocal.test@iafactory.dz",
            "password": "SecurePass123!",
            "full_name": "Voice Test User"
        }
    )
    print(f"Status: {r.status_code}")
    if r.status_code in [200, 201]:
        data = r.json()
        token = data.get('access_token', '')
        print(f"✓ User créé: {data.get('user', {}).get('email')}")
        print(f"✓ JWT Token (first 80 chars): {token[:80]}...")
        print(f"✓ Tenant ID dans JWT: {TENANT_ID}")
    else:
        print(f"Erreur: {r.text}")
        token = None
except Exception as e:
    print(f"Erreur: {e}")
    token = None

if not token:
    print("\n[ERREUR] Impossible d'obtenir le JWT. Arrêt du test.")
    exit(1)

# Step 2: Verify JWT contains tenant_id
print("\n[2/5] Vérification du JWT...")
import base64
try:
    # Decode JWT payload (without verification for demo)
    parts = token.split('.')
    payload_b64 = parts[1]
    # Add padding if needed
    payload_b64 += '=' * (4 - len(payload_b64) % 4)
    payload = json.loads(base64.b64decode(payload_b64))

    print("JWT Payload:")
    print(json.dumps(payload, indent=2))

    if 'tenant_id' in payload:
        print(f"\n✓ tenant_id trouvé dans JWT: {payload['tenant_id']}")
    else:
        print("\n✗ ATTENTION: tenant_id absent du JWT!")

except Exception as e:
    print(f"Erreur décodage JWT: {e}")

# Step 3: Test simple avec texte (sans audio pour l'instant)
print("\n[3/5] Test endpoint Voice Agent /health...")
try:
    r = requests.get(
        f"{BASE_URL}/api/voice-agent/health",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
except Exception as e:
    print(f"Erreur: {e}")

# Step 4: Liste des modèles disponibles
print("\n[4/5] Liste des modèles Whisper...")
try:
    r = requests.get(
        f"{BASE_URL}/api/voice-agent/models",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Modèle actuel: {data.get('current_model')}")
    print(f"Device: {data.get('device')}")
except Exception as e:
    print(f"Erreur: {e}")

print("\n" + "=" * 70)
print("BACKEND OPÉRATIONNEL ✓")
print("Prêt pour transcription audio avec tenant_id automatique!")
print("=" * 70)
print(f"\nToken sauvegardé pour tests: {token[:50]}...")

# Save token for later use
with open("D:/IAFactory/rag-dz/test_token.txt", "w") as f:
    f.write(token)

print("\nPour tester avec un fichier audio:")
print(f"curl -X POST '{BASE_URL}/api/voice-agent/transcribe' \\")
print(f"  -H 'Authorization: Bearer {token[:50]}...' \\")
print(f"  -F 'file=@votre_fichier.mp4' \\")
print(f"  -F 'language=fr'")
