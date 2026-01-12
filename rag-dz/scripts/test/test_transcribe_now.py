#!/usr/bin/env python
"""Test transcription avec JWT"""
import requests
import json
import time
from pathlib import Path

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ2b2NhbC5kZW1vQGlhZmFjdG9yeS5keiIsInVzZXJfaWQiOjMsInRlbmFudF9pZCI6IjgxNGMxMzJhLTFjZGQtNGRiNi1iYzFmLTIxYWJkMjFlYzM3ZCIsImV4cCI6MTc2NTkxNTc4MSwiaWF0IjoxNzY1OTEzOTgxfQ.oj-ZnumGWywI_14W05mBxQMEfzMQ_UHL5rjHSuSvmHM"
AUDIO_FILE = r"C:\Users\bbens\Downloads\WhatsApp Audio 2025-12-16 at 20.05.22.mp4"

print("=" * 70)
print("TEST TRANSCRIPTION AGENT VOCAL")
print("=" * 70)

# Verify file exists
if not Path(AUDIO_FILE).exists():
    print(f"ERREUR: Fichier introuvable: {AUDIO_FILE}")
    exit(1)

file_size = Path(AUDIO_FILE).stat().st_size
print(f"Fichier: {Path(AUDIO_FILE).name}")
print(f"Taille: {file_size / 1024:.2f} KB")

# Start transcription
print("\nDemarrage transcription...")
start_time = time.time()

with open(AUDIO_FILE, "rb") as f:
    response = requests.post(
        "http://127.0.0.1:8001/api/voice-agent/transcribe",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "X-API-Key": "change-me-in-production"
        },
        files={"file": (Path(AUDIO_FILE).name, f, "audio/mp4")},
        data={"language": "fr"}
    )

end_time = time.time()
duration = end_time - start_time

print(f"Status HTTP: {response.status_code}")
print(f"Duree: {duration:.2f} secondes")

if response.status_code == 200:
    result = response.json()
    print("\n" + "=" * 70)
    print("TRANSCRIPTION REUSSIE")
    print("=" * 70)
    print(f"\nTexte transcrit:\n{result.get('text', 'N/A')}")
    print(f"\nLangue detectee: {result.get('language', 'N/A')}")
    print(f"Confiance: {result.get('language_probability', 0):.2%}")
    print(f"Duree audio: {result.get('duration', 0):.2f}s")

    # Save result
    with open("D:/IAFactory/rag-dz/transcription_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("\nResultat sauvegarde dans: transcription_result.json")
else:
    print(f"\nERREUR: {response.text}")
