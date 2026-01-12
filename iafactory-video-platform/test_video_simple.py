#!/usr/bin/env python3
"""
Simple test to create a video with FAL provider
"""

import asyncio
import httpx
import time

API_BASE = "http://localhost:8001/api/v1"

async def main():
    print("\n" + "="*60)
    print("   TEST VIDEO GENERATION WITH FAL PROVIDER")
    print("="*60 + "\n")

    async with httpx.AsyncClient(timeout=30) as client:
        # 1. Health check
        print("[1] Checking API health...")
        r = await client.get("http://localhost:8001/health")
        print(f"    Status: {r.json()}")

        # 2. Create project
        print("\n[2] Creating test project...")
        payload = {
            "title": "Test FAL Video",
            "user_prompt": "Create a 5 second video showing a beautiful sunset over the ocean with gentle waves.",
            "target_duration": "15s",
            "aspect_ratio": "16:9",
            "style": "cinematic",
            "language": "en",
            "target_platforms": ["youtube"]
        }
        r = await client.post(f"{API_BASE}/projects/", json=payload)
        if r.status_code != 201:
            print(f"    ERROR: {r.status_code} - {r.text}")
            return

        project = r.json()
        project_id = project["id"]
        print(f"    Project ID: {project_id}")

        # 3. Start pipeline
        print("\n[3] Starting pipeline...")
        r = await client.post(
            f"{API_BASE}/projects/{project_id}/start",
            json={"auto_publish": False, "priority": "high"}
        )
        print(f"    Response: {r.json()}")

        # 4. Monitor progress
        print("\n[4] Monitoring progress...")
        last_phase = ""
        for i in range(120):  # 10 minutes max
            await asyncio.sleep(5)
            r = await client.get(f"{API_BASE}/projects/{project_id}/status")
            status = r.json()

            phase = status.get("current_phase", "unknown")
            progress = status.get("progress", {}).get("overall", 0)
            project_status = status.get("status", "unknown")

            if phase != last_phase:
                print(f"    [{time.strftime('%H:%M:%S')}] Phase: {phase:20} | Progress: {progress:3}% | Status: {project_status}")
                last_phase = phase

            if project_status == "completed":
                print("\n    VIDEO GENERATION COMPLETED!")
                break
            elif project_status in ["failed", "error"]:
                print(f"\n    FAILED: {status.get('error_message')}")
                break

        # 5. Get final result
        print("\n[5] Getting final result...")
        r = await client.get(f"{API_BASE}/projects/{project_id}")
        project = r.json()
        video_url = project.get("video_url", "NONE")
        print(f"    Video URL: {video_url[:100]}..." if len(video_url) > 100 else f"    Video URL: {video_url}")

        if video_url and ".mp4" in video_url.lower():
            print("\n" + "="*60)
            print("   SUCCESS: VIDEO GENERATED!")
            print("="*60)
        elif video_url and any(ext in video_url.lower() for ext in [".png", ".jpg", ".webp"]):
            print("\n" + "="*60)
            print("   PARTIAL: Image fallback used (video provider failed)")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("   FAILED: No output generated")
            print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
