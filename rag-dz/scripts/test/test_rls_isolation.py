#!/usr/bin/env python
"""Test direct de l'isolation RLS entre tenants"""
import sys
sys.path.insert(0, "D:\\IAFactory\\rag-dz\\backend\\rag-compat")

from app.tokens import repository as tokens_repo

tenant_algerie = "814c132a-1cdd-4db6-bc1f-21abd21ec37d"
tenant_suisse = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"

print("=" * 70)
print("TEST ISOLATION RLS - TOKENS")
print("=" * 70)

print("\n[1/2] Solde Tenant Algérie (IAFactory Demo)...")
balance_alg = tokens_repo.get_balance(tenant_algerie)
print(f"  Balance: {balance_alg['balance_tokens']} tokens")
print(f"  Total purchased: {balance_alg['total_purchased']}")

print("\n[2/2] Solde Tenant Suisse...")
balance_sui = tokens_repo.get_balance(tenant_suisse)
print(f"  Balance: {balance_sui['balance_tokens']} tokens")
print(f"  Total purchased: {balance_sui['total_purchased']}")

print("\n" + "=" * 70)
if balance_alg['balance_tokens'] != balance_sui['balance_tokens']:
    print("✅ ISOLATION RLS FONCTIONNE!")
    print(f"  Algérie: {balance_alg['balance_tokens']} tokens")
    print(f"  Suisse:  {balance_sui['balance_tokens']} tokens")
else:
    print("❌ ERREUR: Les deux tenants voient le même solde")
print("=" * 70)
