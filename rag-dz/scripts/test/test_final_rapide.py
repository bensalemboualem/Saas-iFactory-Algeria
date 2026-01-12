#!/usr/bin/env python
"""Test transcription rapide avec modèle base"""
import requests
import json
import time
from pathlib import Path

AUDIO_FILE = r"C:\Users\bbens\Downloads\WhatsApp Audio 2025-12-16 at 20.05.22.mp4"

print("=" * 70)
print("TEST TRANSCRIPTION RAPIDE - MODELE BASE")
print("=" * 70)

# 1. Login pour obtenir nouveau JWT
print("\n[1/3] Login...")
login_resp = requests.post(
    "http://127.0.0.1:8001/api/auth/login/json",
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

TOKEN = login_resp.json()["access_token"]
print(f"Token obtenu: {TOKEN[:50]}...")

# 2. Verifier fichier
print("\n[2/3] Verification fichier...")
if not Path(AUDIO_FILE).exists():
    print(f"ERREUR: Fichier introuvable: {AUDIO_FILE}")
    exit(1)

file_size = Path(AUDIO_FILE).stat().st_size
print(f"Fichier: {Path(AUDIO_FILE).name} ({file_size / 1024:.1f} KB)")

# 3. Transcription
print("\n[3/3] Transcription en cours (modèle base - rapide)...")
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

print(f"\nStatus HTTP: {response.status_code}")
print(f"Duree totale: {duration:.2f}s")

if response.status_code == 200:
    result = response.json()
    print("\n" + "=" * 70)
    print("TRANSCRIPTION REUSSIE")
    print("=" * 70)
    print(f"\nTexte transcrit:\n{result.get('text', 'N/A')}")
    print(f"\nLangue: {result.get('language', 'N/A')}")
    print(f"Confiance: {result.get('language_probability', 0):.2%}")
    print(f"Duree audio: {result.get('duration', 0):.2f}s")

    # Calcul vitesse transcription
    audio_duration = result.get('duration', 0)
    if audio_duration > 0:
        ratio = audio_duration / duration
        print(f"\nPerformance: {ratio:.2f}x temps réel")
        if ratio < 1:
            print(f"  => Plus lent que temps réel ({duration:.1f}s pour {audio_duration:.1f}s audio)")
        else:
            print(f"  => Plus rapide que temps réel!")

    # Save
    with open("D:/IAFactory/rag-dz/transcription_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("\nResultat sauvegarde: transcription_result.json")
else:
    print(f"\nERREUR: {response.text}")
