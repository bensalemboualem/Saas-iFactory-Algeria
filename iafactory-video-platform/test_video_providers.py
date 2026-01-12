#!/usr/bin/env python3
"""
Test script to verify video provider API keys
"""

import asyncio
import httpx
import os

# Load from .env
def load_env():
    env_path = "backend/.env"
    env = {}
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env[key] = value
    return env

async def test_fal(api_key):
    """Test FAL API key"""
    print("\n[FAL] Testing API key...")
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            # FAL health check - try a simple endpoint
            r = await client.get(
                "https://fal.run/fal-ai/fast-sdxl",
                headers={"Authorization": f"Key {api_key}"}
            )
            if r.status_code == 401:
                print("  [FAIL] 401 Unauthorized - API key is invalid or expired")
                return False
            elif r.status_code == 405:
                print("  [OK] API key seems valid (405 = method not allowed, but authenticated)")
                return True
            else:
                print(f"  [?] Status {r.status_code}")
                return r.status_code < 400
        except Exception as e:
            print(f"  [ERROR] {e}")
            return False

async def test_replicate(api_token):
    """Test Replicate API key"""
    print("\n[REPLICATE] Testing API key...")
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.get(
                "https://api.replicate.com/v1/account",
                headers={"Authorization": f"Bearer {api_token}"}
            )
            if r.status_code == 200:
                data = r.json()
                print(f"  [OK] Account: {data.get('username')}")

                # Check billing
                r2 = await client.get(
                    "https://api.replicate.com/v1/account",
                    headers={"Authorization": f"Bearer {api_token}"}
                )
                print(f"  [INFO] Note: Low credit accounts have rate limits")
                return True
            elif r.status_code == 401:
                print("  [FAIL] 401 Unauthorized - API key is invalid")
                return False
            else:
                print(f"  [?] Status {r.status_code}")
                return False
        except Exception as e:
            print(f"  [ERROR] {e}")
            return False

async def test_luma(api_key):
    """Test Luma API key"""
    print("\n[LUMA] Testing API key...")
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            # Check generations endpoint
            r = await client.get(
                "https://api.lumalabs.ai/dream-machine/v1/generations",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            if r.status_code == 200:
                print("  [OK] API key is valid")
                return True
            elif r.status_code == 401:
                print("  [FAIL] 401 Unauthorized - API key is invalid")
                return False
            elif r.status_code == 400:
                print("  [?] 400 Bad Request - might need different auth format")
                return False
            else:
                print(f"  [?] Status {r.status_code} - {r.text[:100]}")
                return False
        except Exception as e:
            print(f"  [ERROR] {e}")
            return False

async def test_runway(api_key):
    """Test Runway API key"""
    print("\n[RUNWAY] Testing API key...")
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            # Try to get user info or tasks
            r = await client.get(
                "https://api.runwayml.com/v1/tasks",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "X-Runway-Version": "2024-11-06"
                }
            )
            if r.status_code == 200:
                print("  [OK] API key is valid")
                return True
            elif r.status_code == 401:
                print(f"  [FAIL] 401 Unauthorized - {r.text[:100]}")
                return False
            else:
                print(f"  [?] Status {r.status_code} - {r.text[:100]}")
                return r.status_code < 400
        except Exception as e:
            print(f"  [ERROR] {e}")
            return False

async def test_kling(access_key, secret_key):
    """Test Kling API key"""
    print("\n[KLING] Testing API key...")
    print(f"  Access Key: {access_key[:8]}...")
    print(f"  Secret Key: {secret_key[:8]}...")
    print("  [INFO] Kling requires JWT generation - skipping direct test")
    return None

async def test_minimax(api_key):
    """Test MiniMax API key"""
    print("\n[MINIMAX] Testing API key...")
    if not api_key:
        print("  [SKIP] No API key configured")
        return None
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.get(
                "https://api.minimaxi.chat/v1/files",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            if r.status_code == 200:
                print("  [OK] API key is valid")
                return True
            elif r.status_code == 401:
                print("  [FAIL] 401 Unauthorized")
                return False
            else:
                print(f"  [?] Status {r.status_code}")
                return False
        except Exception as e:
            print(f"  [ERROR] {e}")
            return False

async def main():
    print("="*60)
    print("   VIDEO PROVIDER API KEY DIAGNOSTIC")
    print("="*60)

    env = load_env()

    results = {}

    # Test each provider
    if env.get("FAL_KEY"):
        results["FAL"] = await test_fal(env["FAL_KEY"])
    else:
        print("\n[FAL] No API key configured")
        results["FAL"] = None

    if env.get("REPLICATE_API_TOKEN"):
        results["REPLICATE"] = await test_replicate(env["REPLICATE_API_TOKEN"])
    else:
        print("\n[REPLICATE] No API key configured")
        results["REPLICATE"] = None

    if env.get("LUMA_API_KEY"):
        results["LUMA"] = await test_luma(env["LUMA_API_KEY"])
    else:
        print("\n[LUMA] No API key configured")
        results["LUMA"] = None

    if env.get("RUNWAY_API_KEY"):
        results["RUNWAY"] = await test_runway(env["RUNWAY_API_KEY"])
    else:
        print("\n[RUNWAY] No API key configured")
        results["RUNWAY"] = None

    if env.get("KLING_ACCESS_KEY") and env.get("KLING_SECRET_KEY"):
        results["KLING"] = await test_kling(env["KLING_ACCESS_KEY"], env["KLING_SECRET_KEY"])
    else:
        print("\n[KLING] No API key configured")
        results["KLING"] = None

    if env.get("MINIMAX_API_KEY"):
        results["MINIMAX"] = await test_minimax(env["MINIMAX_API_KEY"])
    else:
        print("\n[MINIMAX] No API key configured")
        results["MINIMAX"] = None

    # Summary
    print("\n" + "="*60)
    print("   SUMMARY")
    print("="*60)

    working = []
    failed = []
    unknown = []

    for provider, status in results.items():
        if status is True:
            working.append(provider)
            print(f"  [OK]   {provider}")
        elif status is False:
            failed.append(provider)
            print(f"  [FAIL] {provider}")
        else:
            unknown.append(provider)
            print(f"  [?]    {provider} (not configured or needs special auth)")

    print("\n" + "="*60)
    if working:
        print(f"  Working providers: {', '.join(working)}")
    else:
        print("  NO WORKING VIDEO PROVIDERS!")
        print("  ")
        print("  To fix this, you need valid API keys for at least one provider:")
        print("    - Replicate (replicate.com) - add credit to your account")
        print("    - FAL (fal.ai) - create new API key")
        print("    - Luma (lumalabs.ai) - get API access")
        print("    - Runway (runwayml.com) - get API access")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
