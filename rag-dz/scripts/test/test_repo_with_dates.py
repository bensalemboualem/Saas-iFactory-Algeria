#!/usr/bin/env python
"""Test repository avec des dates réelles"""
import psycopg
import json

DB_URL = "postgresql://postgres:postgres@localhost:5432/iafactory_dz"

tenant_id = "814c132a-1cdd-4db6-bc1f-21abd21ec37d"

print("Test direct psycopg...")
try:
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    balance_tokens, total_purchased, total_consumed,
                    last_purchase_at, last_usage_at
                FROM tenant_token_balances
                WHERE tenant_id = %s
            """, (tenant_id,))

            row = cur.fetchone()

            if row:
                print(f"\nRow data:")
                print(f"  row[0] (balance): {row[0]} - type: {type(row[0])}")
                print(f"  row[1] (purchased): {row[1]} - type: {type(row[1])}")
                print(f"  row[2] (consumed): {row[2]} - type: {type(row[2])}")
                print(f"  row[3] (last_purchase_at): {row[3]} - type: {type(row[3])}")
                print(f"  row[4] (last_usage_at): {row[4]} - type: {type(row[4])}")

                # Test isoformat()
                if row[3]:
                    print(f"\n  row[3].isoformat(): {row[3].isoformat()}")

                # Créer dict comme dans repository
                result = {
                    "balance_tokens": row[0],
                    "total_purchased": row[1],
                    "total_consumed": row[2],
                    "last_purchase_at": row[3].isoformat() if row[3] else None,
                    "last_usage_at": row[4].isoformat() if row[4] else None,
                }

                print(f"\nResult dict: {result}")
                print(f"  Type last_purchase_at: {type(result['last_purchase_at'])}")

                # Test JSON serialization
                print("\nTest JSON serialization...")
                json_str = json.dumps(result)
                print(f"SUCCESS! {json_str}")
            else:
                print("No row found")

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
