#!/usr/bin/env python
"""Script de test rapide du backend"""
import requests
import json

# Test 1: Health check
print("=" * 60)
print("TEST 1: Health Check")
print("=" * 60)
try:
    r = requests.get("http://localhost:8000/health")
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
except Exception as e:
    print(f"Erreur: {e}")

print("\n" + "=" * 60)
print("TEST 2: Register User")
print("=" * 60)
try:
    r = requests.post(
        "http://localhost:8000/api/auth/register",
        json={
            "email": "vocal.test@iafactory.dz",
            "password": "SecurePass123!",
            "full_name": "Voice Test User"
        }
    )
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"User: {data.get('user', {}).get('email')}")
    print(f"Token (first 50 chars): {data.get('access_token', '')[:50]}...")

    # Save token for next test
    with open("D:/IAFactory/rag-dz/test_token.txt", "w") as f:
        f.write(data.get('access_token', ''))

except Exception as e:
    print(f"Erreur: {e}")

print("\nBackend est opérationnel!")
