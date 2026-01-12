#!/usr/bin/env python
"""Execute migration 009 - Token System"""
import psycopg

# Read migration
with open("backend/rag-compat/migrations/009_token_system.sql", "r", encoding="utf-8") as f:
    sql = f.read()

# Execute
conn = psycopg.connect("postgresql://postgres:ragdz2024secure@localhost:6330/iafactory_dz")
try:
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()
    print("OK - Migration 009 executed successfully")
except Exception as e:
    print(f"ERROR: {e}")
    conn.rollback()
finally:
    conn.close()
