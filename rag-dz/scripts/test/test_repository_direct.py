#!/usr/bin/env python
"""Test direct du repository tokens pour voir ce qu'il retourne"""
import sys
sys.path.insert(0, "D:\\IAFactory\\rag-dz\\backend\\rag-compat")

from app.tokens import repository as tokens_repo
import json

tenant_id = "814c132a-1cdd-4db6-bc1f-21abd21ec37d"  # Tenant Algérie

print("Test direct repository get_balance...")
try:
    balance = tokens_repo.get_balance(tenant_id)
    print(f"\nType: {type(balance)}")
    print(f"Content: {balance}")

    # Essayer de sérialiser en JSON
    print("\nTest sérialisation JSON...")
    json_str = json.dumps(balance)
    print("SUCCESS! JSON:", json_str)

except Exception as e:
    print(f"\nERROR: {e}")
    print(f"Type error: {type(e)}")
    import traceback
    traceback.print_exc()
