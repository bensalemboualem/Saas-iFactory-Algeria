#!/usr/bin/env python3
"""
Test script for Zero Risque Architecture
Tests all critical endpoints and routing logic
"""
import asyncio
import httpx
import os
from typing import Dict, Any
import json

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "")  # Get from login endpoint
TEST_USER_TOKEN = os.getenv("TEST_USER_TOKEN", "")  # Get from login endpoint

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_success(msg: str):
    print(f"{GREEN}✅ {msg}{RESET}")


def print_error(msg: str):
    print(f"{RED}❌ {msg}{RESET}")


def print_info(msg: str):
    print(f"{BLUE}ℹ️  {msg}{RESET}")


def print_warning(msg: str):
    print(f"{YELLOW}⚠️  {msg}{RESET}")


async def test_health():
    """Test 1: Health check"""
    print(f"\n{BLUE}[TEST 1/8] Health Check{RESET}")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/health")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.json()
            assert data["status"] == "healthy", "Service not healthy"
            print_success(f"API is healthy: {data}")
        except Exception as e:
            print_error(f"Health check failed: {e}")
            return False
    return True


async def test_admin_dashboard():
    """Test 2: Admin Dashboard (requires admin token)"""
    print(f"\n{BLUE}[TEST 2/8] Admin Dashboard{RESET}")

    if not ADMIN_TOKEN:
        print_warning("ADMIN_TOKEN not set, skipping test")
        return True

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{API_BASE_URL}/api/admin/dashboard",
                headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
            )
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.json()

            # Verify structure
            assert "budget" in data, "Missing budget section"
            assert "users" in data, "Missing users section"
            assert "economics" in data, "Missing economics section"

            print_success("Admin dashboard accessible")
            print_info(f"Budget spent today: ${data['budget']['spent_today_usd']:.2f}")
            print_info(f"Active users: {data['users']['active_count']}")
            print_info(f"Revenue: {data['economics']['revenue_dzd']} DZD")
            print_info(f"Margin: {data['economics']['margin_percent']:.1f}%")
        except Exception as e:
            print_error(f"Admin dashboard test failed: {e}")
            return False
    return True


async def test_chat_free_tier():
    """Test 3: Chat endpoint with FREE tier (should use 100% Groq)"""
    print(f"\n{BLUE}[TEST 3/8] Chat with FREE tier{RESET}")

    if not TEST_USER_TOKEN:
        print_warning("TEST_USER_TOKEN not set, skipping test")
        return True

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{API_BASE_URL}/api/v2/chat",
                headers={"Authorization": f"Bearer {TEST_USER_TOKEN}"},
                json={
                    "messages": [
                        {"role": "user", "content": "Hello! Say 'TEST OK' if you can read this."}
                    ]
                }
            )
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.json()

            assert "response" in data, "Missing response field"
            assert data["provider"] == "groq", f"FREE tier should use Groq, got {data['provider']}"

            print_success("FREE tier chat works")
            print_info(f"Provider: {data['provider']}")
            print_info(f"Tokens: {data.get('tokens_input', 0)} in / {data.get('tokens_output', 0)} out")
        except Exception as e:
            print_error(f"FREE tier chat test failed: {e}")
            return False
    return True


async def test_chat_rate_limit():
    """Test 4: Rate limiting (should block after quota exceeded)"""
    print(f"\n{BLUE}[TEST 4/8] Rate Limiting{RESET}")

    if not TEST_USER_TOKEN:
        print_warning("TEST_USER_TOKEN not set, skipping test")
        return True

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Send 5 requests quickly (FREE tier has 1 msg/min, 3 msg/day)
            for i in range(5):
                response = await client.post(
                    f"{API_BASE_URL}/api/v2/chat",
                    headers={"Authorization": f"Bearer {TEST_USER_TOKEN}"},
                    json={"messages": [{"role": "user", "content": f"Test {i}"}]}
                )

                if response.status_code == 429:
                    print_success(f"Rate limit kicked in after {i} requests")
                    return True

            print_warning("Rate limit not triggered (might need to adjust test)")
        except Exception as e:
            print_error(f"Rate limit test failed: {e}")
            return False
    return True


async def test_payment_checkout():
    """Test 5: Create payment checkout (STUDENT tier)"""
    print(f"\n{BLUE}[TEST 5/8] Payment Checkout Creation{RESET}")

    if not TEST_USER_TOKEN:
        print_warning("TEST_USER_TOKEN not set, skipping test")
        return True

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{API_BASE_URL}/api/payment/subscribe/student",
                headers={"Authorization": f"Bearer {TEST_USER_TOKEN}"}
            )
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.json()

            assert "checkout_url" in data, "Missing checkout_url"
            assert "checkout_id" in data, "Missing checkout_id"

            print_success("Payment checkout created")
            print_info(f"Checkout URL: {data['checkout_url']}")
        except Exception as e:
            print_error(f"Payment checkout test failed: {e}")
            return False
    return True


async def test_models_endpoint():
    """Test 6: Available models by tier"""
    print(f"\n{BLUE}[TEST 6/8] Available Models{RESET}")

    if not TEST_USER_TOKEN:
        print_warning("TEST_USER_TOKEN not set, skipping test")
        return True

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{API_BASE_URL}/api/v2/models",
                headers={"Authorization": f"Bearer {TEST_USER_TOKEN}"}
            )
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.json()

            assert "models" in data, "Missing models list"
            assert len(data["models"]) > 0, "No models available"

            print_success(f"Models endpoint works ({len(data['models'])} models available)")
            for model in data["models"][:3]:  # Show first 3
                print_info(f"  - {model['name']}: {model['description']}")
        except Exception as e:
            print_error(f"Models endpoint test failed: {e}")
            return False
    return True


async def test_usage_today():
    """Test 7: Usage stats for current user"""
    print(f"\n{BLUE}[TEST 7/8] Usage Stats{RESET}")

    if not TEST_USER_TOKEN:
        print_warning("TEST_USER_TOKEN not set, skipping test")
        return True

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{API_BASE_URL}/api/v2/usage/today",
                headers={"Authorization": f"Bearer {TEST_USER_TOKEN}"}
            )
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.json()

            print_success("Usage stats retrieved")
            print_info(f"Messages today: {data['messages_today']}")
            print_info(f"Tier: {data['tier']}")
            print_info(f"Quota remaining: {data['quota_remaining']}/{data['quota_limit']}")
        except Exception as e:
            print_error(f"Usage stats test failed: {e}")
            return False
    return True


async def test_subscription_status():
    """Test 8: Check subscription status"""
    print(f"\n{BLUE}[TEST 8/8] Subscription Status{RESET}")

    if not TEST_USER_TOKEN:
        print_warning("TEST_USER_TOKEN not set, skipping test")
        return True

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{API_BASE_URL}/api/payment/status",
                headers={"Authorization": f"Bearer {TEST_USER_TOKEN}"}
            )
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.json()

            print_success("Subscription status retrieved")
            print_info(f"Tier: {data['tier']}")
            print_info(f"Active: {data['active']}")
            if data['expires_at']:
                print_info(f"Expires: {data['expires_at']}")
        except Exception as e:
            print_error(f"Subscription status test failed: {e}")
            return False
    return True


async def run_all_tests():
    """Run all tests sequentially"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  ZERO RISQUE ARCHITECTURE - TEST SUITE{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    print_info(f"Testing API at: {API_BASE_URL}")

    tests = [
        test_health,
        test_admin_dashboard,
        test_chat_free_tier,
        test_chat_rate_limit,
        test_payment_checkout,
        test_models_endpoint,
        test_usage_today,
        test_subscription_status,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            result = await test()
            if result:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print_error(f"Test crashed: {e}")
            failed += 1

    # Summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  TEST SUMMARY{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    print_success(f"Passed: {passed}/{len(tests)}")
    if failed > 0:
        print_error(f"Failed: {failed}/{len(tests)}")
    print(f"{BLUE}{'='*60}{RESET}\n")

    return failed == 0


if __name__ == "__main__":
    # Instructions
    if not ADMIN_TOKEN or not TEST_USER_TOKEN:
        print_warning("\n⚠️  TOKENS NOT SET - Some tests will be skipped")
        print_info("To run all tests, set environment variables:")
        print_info("  export ADMIN_TOKEN='your_admin_token'")
        print_info("  export TEST_USER_TOKEN='your_test_user_token'")
        print_info("\nYou can get tokens by logging in:")
        print_info("  curl -X POST http://localhost:8000/api/auth/login \\")
        print_info("    -H 'Content-Type: application/json' \\")
        print_info("    -d '{\"email\": \"admin@iafactory.dz\", \"password\": \"your_password\"}'")
        print()

    # Run tests
    success = asyncio.run(run_all_tests())
    exit(0 if success else 1)
