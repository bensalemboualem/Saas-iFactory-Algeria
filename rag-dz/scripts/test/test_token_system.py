#!/usr/bin/env python
"""Test complet du système de Tokens (Carburant) avec isolation multi-tenant"""
import requests
import json

BASE_URL = "http://127.0.0.1:8002"

print("=" * 70)
print("TEST SYSTÈME TOKENS (CARBURANT) - MULTI-TENANT")
print("=" * 70)

# ============================================================
# Test 1: Login Tenant Algérie
# ============================================================
print("\n[1/7] Login Tenant Algérie...")
login_resp = requests.post(
    f"{BASE_URL}/api/auth/login/json",
    headers={
        "Content-Type": "application/json",
        "X-API-Key": "change-me-in-production"
    },
    json={
        "email": "vocal.demo@iafactory.dz",
        "password": "SecurePass123!"
    }
)

if login_resp.status_code != 200:
    print(f"ERREUR Login: {login_resp.text}")
    exit(1)

TOKEN_ALGERIE = login_resp.json()["access_token"]
print(f"Token Algérie obtenu: {TOKEN_ALGERIE[:30]}...")

# ============================================================
# Test 2: Consulter solde AVANT redeem (doit être 0)
# ============================================================
print("\n[2/7] Consulter solde AVANT redeem...")
balance_resp = requests.get(
    f"{BASE_URL}/api/tokens/balance",
    headers={
        "Authorization": f"Bearer {TOKEN_ALGERIE}",
        "X-API-Key": "change-me-in-production"
    }
)

if balance_resp.status_code == 200:
    balance = balance_resp.json()
    print(f"Solde initial: {balance['balance_tokens']} tokens")
    print(f"  Total acheté: {balance['total_purchased']}")
    print(f"  Total consommé: {balance['total_consumed']}")
else:
    print(f"ERREUR balance: {balance_resp.text}")

# ============================================================
# Test 3: Redeem code ALGERIE-STARTER-500
# ============================================================
print("\n[3/7] Redeem code: ALGERIE-STARTER-500...")
redeem_resp = requests.post(
    f"{BASE_URL}/api/tokens/redeem",
    headers={
        "Authorization": f"Bearer {TOKEN_ALGERIE}",
        "X-API-Key": "change-me-in-production",
        "Content-Type": "application/json"
    },
    json={"code": "ALGERIE-STARTER-500"}
)

if redeem_resp.status_code == 200:
    result = redeem_resp.json()
    print(f"SUCCESS: Code activé!")
    print(f"  Tokens crédités: +{result['tokens_credited']}")
    print(f"  Nouveau solde: {result['new_balance']}")
else:
    print(f"ERREUR redeem: {redeem_resp.text}")

# ============================================================
# Test 4: Vérifier solde APRÈS redeem
# ============================================================
print("\n[4/7] Vérifier solde APRÈS redeem...")
balance_resp2 = requests.get(
    f"{BASE_URL}/api/tokens/balance",
    headers={
        "Authorization": f"Bearer {TOKEN_ALGERIE}",
        "X-API-Key": "change-me-in-production"
    }
)

if balance_resp2.status_code == 200:
    balance2 = balance_resp2.json()
    print(f"Nouveau solde: {balance2['balance_tokens']} tokens")
    print(f"  Total acheté: {balance2['total_purchased']}")
else:
    print(f"ERREUR balance: {balance_resp2.text}")

# ============================================================
# Test 5: Login Tenant Suisse (isolation test)
# ============================================================
print("\n[5/7] Login Tenant Suisse (isolation test)...")
login_suisse_resp = requests.post(
    f"{BASE_URL}/api/auth/login/json",
    headers={
        "Content-Type": "application/json",
        "X-API-Key": "change-me-in-production"
    },
    json={
        "email": "test@suisse.ch",
        "password": "SecurePass123!"
    }
)

if login_suisse_resp.status_code == 200:
    TOKEN_SUISSE = login_suisse_resp.json()["access_token"]
    print(f"Token Suisse obtenu: {TOKEN_SUISSE[:30]}...")
else:
    # Créer utilisateur Suisse si inexistant
    print("Création utilisateur Suisse...")
    register_resp = requests.post(
        f"{BASE_URL}/api/auth/register",
        headers={
            "Content-Type": "application/json",
            "X-API-Key": "change-me-in-production"
        },
        json={
            "email": "test@suisse.ch",
            "password": "SecurePass123!",
            "full_name": "Test Suisse"
        }
    )

    if register_resp.status_code == 200:
        TOKEN_SUISSE = register_resp.json()["access_token"]
        print(f"Token Suisse créé: {TOKEN_SUISSE[:30]}...")
    else:
        print(f"ERREUR register: {register_resp.text}")
        TOKEN_SUISSE = None

# ============================================================
# Test 6: Solde Tenant Suisse (doit être 0 - isolation RLS)
# ============================================================
if TOKEN_SUISSE:
    print("\n[6/7] Consulter solde Tenant Suisse...")
    balance_suisse_resp = requests.get(
        f"{BASE_URL}/api/tokens/balance",
        headers={
            "Authorization": f"Bearer {TOKEN_SUISSE}",
            "X-API-Key": "change-me-in-production"
        }
    )

    if balance_suisse_resp.status_code == 200:
        balance_suisse = balance_suisse_resp.json()
        print(f"Solde Tenant Suisse: {balance_suisse['balance_tokens']} tokens")

        if balance_suisse['balance_tokens'] == 0:
            print("  => ISOLATION RLS OK! Tenant Suisse ne voit PAS les tokens d'Algérie")
        else:
            print("  => ERREUR: Tenant Suisse voit les tokens d'Algérie!")
    else:
        print(f"ERREUR balance Suisse: {balance_suisse_resp.text}")

# ============================================================
# Test 7: Historique d'utilisation
# ============================================================
print("\n[7/7] Consulter historique Tenant Algérie...")
history_resp = requests.get(
    f"{BASE_URL}/api/tokens/history?limit=5",
    headers={
        "Authorization": f"Bearer {TOKEN_ALGERIE}",
        "X-API-Key": "change-me-in-production"
    }
)

if history_resp.status_code == 200:
    history = history_resp.json()
    print(f"Historique: {history['count']} entrées")
    for log in history['history']:
        print(f"  - {log['provider']}/{log['model']}: {log['tokens_total']} tokens "
              f"(input: {log['tokens_input']}, output: {log['tokens_output']})")
else:
    print(f"ERREUR history: {history_resp.text}")

print("\n" + "=" * 70)
print("TEST TERMINE")
print("=" * 70)
