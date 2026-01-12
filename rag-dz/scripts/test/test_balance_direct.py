#!/usr/bin/env python
"""Test direct de l'endpoint balance pour voir l'erreur exacte"""
import requests
import json

BASE_URL = "http://127.0.0.1:8002"

# Login
print("Login...")
login_resp = requests.post(
    f"{BASE_URL}/api/auth/login/json",
    headers={"Content-Type": "application/json", "X-API-Key": "change-me-in-production"},
    json={"email": "vocal.demo@iafactory.dz", "password": "SecurePass123!"}
)

if login_resp.status_code == 200:
    TOKEN = login_resp.json()["access_token"]
    print(f"Token obtenu: {TOKEN[:30]}...")

    # Test balance
    print("\nTest balance...")
    balance_resp = requests.get(
        f"{BASE_URL}/api/tokens/balance",
        headers={"Authorization": f"Bearer {TOKEN}", "X-API-Key": "change-me-in-production"}
    )

    print(f"Status: {balance_resp.status_code}")
    print(f"Headers: {balance_resp.headers}")
    print(f"Content: {balance_resp.text[:500]}")

    if balance_resp.status_code == 200:
        print("\nSUCCESS!")
        print(json.dumps(balance_resp.json(), indent=2))
    else:
        print("\nERROR!")
        print(balance_resp.text)
else:
    print(f"Login failed: {login_resp.text}")
