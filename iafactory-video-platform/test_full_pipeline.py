#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IAFactory Video Platform - Test complet du pipeline avec estimation des couts
"""

import asyncio
import httpx
import time
import sys
import io
from datetime import datetime

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

API_BASE = "http://localhost:8001/api/v1"

# ============================================
# ESTIMATION DES COUTS PAR PROVIDER
# ============================================

COSTS = {
    # LLM (analyse + script) - par 1M tokens
    "groq": {"input": 0.05, "output": 0.10},  # Llama 3.3 70B
    "openai_gpt4": {"input": 10.00, "output": 30.00},  # GPT-4 Turbo

    # Images - par image
    "dalle3_standard": 0.040,  # DALL-E 3 Standard 1024x1024
    "dalle3_hd": 0.080,  # DALL-E 3 HD 1024x1792

    # Video - par generation (5s clip)
    "luma_ray2": 0.50,  # Luma Ray 2 - ~$0.50 par clip de 5s
    "replicate_ltx": 0.05,  # LTX Video sur Replicate
    "fal_kling": 0.15,  # FAL Kling

    # Audio TTS - par 1M caracteres
    "openai_tts": 15.00,  # OpenAI TTS
    "elevenlabs": 30.00,  # ElevenLabs
}

def estimate_video_cost(
    duration_seconds: int = 60,
    num_scenes: int = 6,
    llm_provider: str = "groq",
    image_provider: str = "dalle3_standard",
    video_provider: str = "luma_ray2",
    audio_provider: str = "openai_tts",
) -> dict:
    """Estime le cout de production d'une video"""

    costs = {
        "llm": 0,
        "images": 0,
        "video": 0,
        "audio": 0,
        "total": 0
    }

    # LLM: ~2000 tokens input, ~1000 tokens output pour analyse + script
    if llm_provider == "groq":
        costs["llm"] = (2000 * COSTS["groq"]["input"] + 1000 * COSTS["groq"]["output"]) / 1_000_000
    else:
        costs["llm"] = (2000 * COSTS["openai_gpt4"]["input"] + 1000 * COSTS["openai_gpt4"]["output"]) / 1_000_000

    # Images: 1 image par scene
    costs["images"] = num_scenes * COSTS[image_provider]

    # Video: 1 clip par scene (image-to-video)
    costs["video"] = num_scenes * COSTS[video_provider]

    # Audio: ~150 caracteres par seconde de narration
    chars_total = duration_seconds * 150
    costs["audio"] = (chars_total * COSTS[audio_provider]) / 1_000_000

    costs["total"] = sum([costs["llm"], costs["images"], costs["video"], costs["audio"]])

    return costs


def print_cost_estimate():
    """Affiche les estimations de couts pour differentes configurations"""

    print("\n" + "="*70)
    print("   ESTIMATION DES COUTS - IAFACTORY VIDEO PLATFORM")
    print("="*70)

    # Configuration actuelle (Groq + DALL-E + Luma + OpenAI TTS)
    print("\n[ACTUEL] Configuration: Groq + DALL-E 3 + Luma Ray 2 + OpenAI TTS")
    print("-" * 60)

    configs = [
        ("Video 15s (3 scenes)", 15, 3),
        ("Video 30s (6 scenes)", 30, 6),
        ("Video 60s (12 scenes)", 60, 12),
        ("Video 3min (36 scenes)", 180, 36),
    ]

    print(f"\n{'Type':<25} {'LLM':>8} {'Images':>8} {'Video':>8} {'Audio':>8} {'TOTAL':>10}")
    print("-" * 70)

    for name, duration, scenes in configs:
        costs = estimate_video_cost(
            duration_seconds=duration,
            num_scenes=scenes,
            llm_provider="groq",
            image_provider="dalle3_standard",
            video_provider="luma_ray2",
            audio_provider="openai_tts"
        )
        print(f"{name:<25} ${costs['llm']:>6.4f} ${costs['images']:>6.2f} ${costs['video']:>6.2f} ${costs['audio']:>6.4f} ${costs['total']:>8.2f}")

    # Configuration economique
    print("\n\n[ECO] Configuration economique: Groq + DALL-E 3 + Replicate LTX")
    print("-" * 60)

    print(f"\n{'Type':<25} {'LLM':>8} {'Images':>8} {'Video':>8} {'Audio':>8} {'TOTAL':>10}")
    print("-" * 70)

    for name, duration, scenes in configs:
        costs = estimate_video_cost(
            duration_seconds=duration,
            num_scenes=scenes,
            llm_provider="groq",
            image_provider="dalle3_standard",
            video_provider="replicate_ltx",
            audio_provider="openai_tts"
        )
        print(f"{name:<25} ${costs['llm']:>6.4f} ${costs['images']:>6.2f} ${costs['video']:>6.2f} ${costs['audio']:>6.4f} ${costs['total']:>8.2f}")

    # Resume
    print("\n\n" + "="*70)
    print("   PRIX UNITAIRES PAR COMPOSANT")
    print("="*70)
    print("""
  COMPOSANT                 PRIX                    NOTES
  -------------------------------------------------------------------------
  LLM (Groq Llama 3.3)      ~$0.0001/video          Quasi gratuit!
  LLM (OpenAI GPT-4)        ~$0.05/video            50x plus cher

  Image (DALL-E 3)          $0.04/image             Standard 1024x1024
  Image (DALL-E 3 HD)       $0.08/image             HD 1024x1792

  Video (Luma Ray 2)        ~$0.50/clip 5s          Haute qualite
  Video (Replicate LTX)     ~$0.05/clip             10x moins cher!
  Video (FAL Kling)         ~$0.15/clip             Milieu de gamme

  Audio (OpenAI TTS)        ~$0.002/video 60s       Tres economique
  Audio (ElevenLabs)        ~$0.004/video 60s       Voix premium
    """)

    print("="*70)
    print("   ANALYSE DES COUTS")
    print("="*70)
    print("""
  [!] COUT DOMINANT: Generation video (70-90% du cout total)

  Avec Luma Ray 2 ($0.50/clip):
    - Video 60s (12 scenes) = $6.00 en video + $0.48 images = ~$6.50 total

  Avec Replicate LTX ($0.05/clip):
    - Video 60s (12 scenes) = $0.60 en video + $0.48 images = ~$1.10 total

  [RECOMMANDATION]
    - Production: Utiliser Luma pour la qualite
    - Tests/Dev: Utiliser Replicate pour economiser
    - Budget serre: Replicate LTX offre 10x moins cher avec qualite correcte
    """)

    print("="*70)


async def test_pipeline():
    """Test le pipeline complet"""

    print("\n" + "="*70)
    print("   TEST DU PIPELINE DE GENERATION VIDEO")
    print("="*70)

    async with httpx.AsyncClient(timeout=30) as client:
        # 1. Health check
        print("\n[1/5] Verification de l'API...")
        r = await client.get("http://localhost:8001/health")
        if r.status_code != 200:
            print(f"  [FAIL] API non disponible: {r.status_code}")
            return
        print(f"  [OK] API: {r.json()['app']} v{r.json()['version']}")

        # 2. Creer un projet test
        print("\n[2/5] Creation du projet test...")
        payload = {
            "title": "Test - Coucher de soleil",
            "user_prompt": "Cree une video relaxante de 15 secondes montrant un magnifique coucher de soleil sur l'ocean avec des vagues douces. Style cinematique.",
            "target_duration": "15s",
            "aspect_ratio": "16:9",
            "style": "cinematic",
            "language": "fr",
            "target_platforms": ["youtube"]
        }

        r = await client.post(f"{API_BASE}/projects/", json=payload)
        if r.status_code != 201:
            print(f"  [FAIL] Erreur creation: {r.status_code} - {r.text}")
            return

        project = r.json()
        project_id = project["id"]
        print(f"  [OK] Projet cree: {project_id}")

        # Estimation du cout
        estimated = estimate_video_cost(duration_seconds=15, num_scenes=3)
        print(f"  [$$] Cout estime: ${estimated['total']:.2f}")

        # 3. Demarrer le pipeline
        print("\n[3/5] Demarrage du pipeline...")
        start_time = time.time()

        r = await client.post(
            f"{API_BASE}/projects/{project_id}/start",
            json={"auto_publish": False, "priority": "high"}
        )
        if r.status_code != 200:
            print(f"  [FAIL] Erreur demarrage: {r.status_code} - {r.text}")
            return
        print("  [OK] Pipeline demarre")

        # 4. Suivre la progression
        print("\n[4/5] Progression du pipeline...")
        print("  " + "-" * 55)

        last_phase = ""
        phase_times = {}

        for i in range(360):  # 30 minutes max
            await asyncio.sleep(5)

            r = await client.get(f"{API_BASE}/projects/{project_id}/status")
            if r.status_code != 200:
                continue

            status = r.json()
            phase = status.get("current_phase", "unknown")
            progress = status.get("progress", {}).get("overall", 0)
            project_status = status.get("status", "unknown")

            # Enregistrer le temps de chaque phase
            if phase != last_phase:
                now = time.time()
                if last_phase:
                    phase_times[last_phase] = now - phase_times.get(f"{last_phase}_start", start_time)
                phase_times[f"{phase}_start"] = now

                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"  [{timestamp}] {phase:15} | {progress:3}% | {project_status}")
                last_phase = phase

            if project_status == "completed":
                break
            elif project_status in ["failed", "error"]:
                print(f"  [FAIL] Pipeline echoue: {status.get('error_message')}")
                return

        elapsed = time.time() - start_time

        # 5. Resultat final
        print("\n[5/5] Resultat final...")
        print("  " + "-" * 55)

        r = await client.get(f"{API_BASE}/projects/{project_id}")
        project = r.json()
        video_url = project.get("video_url", "")

        if video_url and "luma" in video_url.lower():
            print(f"  [SUCCESS] VIDEO GENEREE!")
            print(f"  URL: {video_url[:80]}...")
        elif video_url and any(ext in video_url.lower() for ext in [".png", ".jpg", "dalle"]):
            print(f"  [WARN] Image generee (fallback - video a echoue)")
            print(f"  URL: {video_url[:80]}...")
        else:
            print(f"  [FAIL] Pas de sortie generee")

        # Statistiques
        print(f"\n  STATISTIQUES:")
        print(f"    Temps total: {elapsed:.1f}s ({elapsed/60:.1f} min)")
        print(f"    Cout estime: ${estimated['total']:.2f}")

        if video_url and "luma" in video_url.lower():
            print(f"\n  Pour telecharger la video:")
            print(f"    curl -o video.mp4 \"{video_url}\"")


async def main():
    # Afficher les estimations de couts
    print_cost_estimate()

    # Demander si on veut lancer le test
    print("\n" + "="*70)
    try:
        response = input("Voulez-vous lancer un test de generation video? (o/N): ")
        if response.lower() in ['o', 'oui', 'y', 'yes']:
            await test_pipeline()
        else:
            print("Test annule.")
    except EOFError:
        print("Mode non-interactif - affichage des couts uniquement.")

    print("\n")


if __name__ == "__main__":
    asyncio.run(main())
