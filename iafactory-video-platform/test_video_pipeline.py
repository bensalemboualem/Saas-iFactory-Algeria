#!/usr/bin/env python3
"""
Test script for IAFactory Video Platform Pipeline
Tests each phase individually to identify issues
"""

import asyncio
import httpx
import json
import time
from datetime import datetime

API_BASE = "http://localhost:8001/api/v1"

def log(msg: str, level: str = "INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")

async def test_health():
    """Test API health"""
    log("Testing API health...")
    async with httpx.AsyncClient() as client:
        r = await client.get("http://localhost:8001/health")
        data = r.json()
        log(f"Health: {data['status']} - {data['app']} v{data['version']}")
        return r.status_code == 200

async def test_create_project():
    """Create a test project"""
    log("Creating test project...")

    payload = {
        "title": "Test Video - IA pour entreprises",
        "user_prompt": "Crée une vidéo de 30 secondes expliquant comment l'intelligence artificielle peut aider les petites entreprises algériennes à gagner du temps et être plus efficaces. Style professionnel et moderne.",
        "target_duration": "30s",
        "aspect_ratio": "16:9",
        "style": "professional",
        "language": "fr",
        "target_platforms": ["youtube"]
    }

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{API_BASE}/projects/", json=payload)
        if r.status_code == 201:
            project = r.json()
            log(f"Project created: {project['id']}")
            log(f"  Title: {project['title']}")
            log(f"  Status: {project['status']}")
            return project
        else:
            log(f"Failed to create project: {r.status_code} - {r.text}", "ERROR")
            return None

async def test_start_pipeline(project_id: str):
    """Start the pipeline"""
    log(f"Starting pipeline for project {project_id}...")

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            f"{API_BASE}/projects/{project_id}/start",
            json={"auto_publish": False, "priority": "high"}
        )
        if r.status_code == 200:
            result = r.json()
            log(f"Pipeline started: {result['status']}")
            return True
        else:
            log(f"Failed to start pipeline: {r.status_code} - {r.text}", "ERROR")
            return False

async def monitor_pipeline(project_id: str, max_wait: int = 600):
    """Monitor pipeline progress"""
    log(f"Monitoring pipeline (max {max_wait}s)...")

    start_time = time.time()
    last_phase = ""
    last_progress = -1

    async with httpx.AsyncClient(timeout=30) as client:
        while time.time() - start_time < max_wait:
            try:
                r = await client.get(f"{API_BASE}/projects/{project_id}/status")
                if r.status_code == 200:
                    status = r.json()
                    current_phase = status.get("current_phase", "unknown")
                    progress = status.get("progress", {}).get("overall", 0)
                    project_status = status.get("status", "unknown")

                    # Only log changes
                    if current_phase != last_phase or progress != last_progress:
                        log(f"Phase: {current_phase:20} | Progress: {progress:3}% | Status: {project_status}")
                        last_phase = current_phase
                        last_progress = progress

                    if project_status == "completed":
                        log("Pipeline COMPLETED!", "SUCCESS")
                        return True
                    elif project_status in ["failed", "error"]:
                        log(f"Pipeline FAILED: {status.get('error_message', 'Unknown error')}", "ERROR")
                        return False

            except Exception as e:
                log(f"Monitoring error: {e}", "WARN")

            await asyncio.sleep(3)

    log("Pipeline TIMEOUT", "ERROR")
    return False

async def get_final_project(project_id: str):
    """Get final project details"""
    log("Getting final project details...")

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(f"{API_BASE}/projects/{project_id}")
        if r.status_code == 200:
            project = r.json()
            log(f"Final Status: {project['status']}")
            log(f"Video URL: {project.get('video_url', 'NONE')}")

            # Check if it's an image or video
            video_url = project.get('video_url', '')
            if video_url:
                if any(ext in video_url.lower() for ext in ['.mp4', '.webm', '.mov', 'video']):
                    log("Output type: VIDEO", "SUCCESS")
                elif any(ext in video_url.lower() for ext in ['.png', '.jpg', '.jpeg', '.webp', 'image']):
                    log("Output type: IMAGE (fallback - video generation failed)", "WARN")
                else:
                    log(f"Output type: UNKNOWN - {video_url[:100]}", "WARN")

            return project
        else:
            log(f"Failed to get project: {r.status_code}", "ERROR")
            return None

async def test_video_providers():
    """Test which video providers are available"""
    log("Checking available video providers...")

    # This would require access to the backend, so we'll check via logs
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            # Check container logs for provider info
            log("Available providers depend on API keys in .env:")
            log("  - FAL_KEY -> FAL AI (Kling video)")
            log("  - LUMA_API_KEY -> Luma AI")
            log("  - RUNWAY_API_KEY -> Runway ML")
            log("  - REPLICATE_API_TOKEN -> Replicate (various models)")
        except Exception as e:
            log(f"Error checking providers: {e}", "WARN")

async def run_full_test():
    """Run complete pipeline test"""
    print("\n" + "="*60)
    print("   IAFACTORY VIDEO PLATFORM - PIPELINE TEST")
    print("="*60 + "\n")

    # Test health
    if not await test_health():
        log("API not healthy, aborting", "ERROR")
        return

    # Check providers
    await test_video_providers()
    print()

    # Create project
    project = await test_create_project()
    if not project:
        return

    project_id = project["id"]
    print()

    # Start pipeline
    if not await test_start_pipeline(project_id):
        return

    print()

    # Monitor
    success = await monitor_pipeline(project_id)
    print()

    # Get final result
    final = await get_final_project(project_id)

    print("\n" + "="*60)
    if success and final:
        video_url = final.get('video_url', '')
        if video_url and '.mp4' in video_url.lower():
            print("   TEST RESULT: SUCCESS - Video generated!")
        elif video_url:
            print("   TEST RESULT: PARTIAL - Image fallback used")
            print("   (Video provider failed, need valid API key)")
        else:
            print("   TEST RESULT: FAILED - No output")
    else:
        print("   TEST RESULT: FAILED")
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(run_full_test())
