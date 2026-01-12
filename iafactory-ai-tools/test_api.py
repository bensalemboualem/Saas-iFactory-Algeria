#!/usr/bin/env python3
"""
Test script for iafactory AI Tools API
Run this after starting the services to verify everything works
"""
import requests
import json
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8001/api/v1"


def print_result(test_name: str, success: bool, details: str = ""):
    """Print test result with color"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} - {test_name}")
    if details:
        print(f"   {details}")
    print()


def test_health_check() -> bool:
    """Test 1: Health check"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        success = response.status_code == 200
        details = f"Status: {response.status_code}"
        print_result("Health Check", success, details)
        return success
    except Exception as e:
        print_result("Health Check", False, str(e))
        return False


def test_get_languages() -> bool:
    """Test 2: Get supported languages"""
    try:
        response = requests.get(f"{BASE_URL}/translator/languages", timeout=5)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            langs = [lang['code'] for lang in data['supported_languages']]
            details = f"Supported: {', '.join(langs)}"
        else:
            details = f"Status: {response.status_code}"
        
        print_result("Get Languages", success, details)
        return success
    except Exception as e:
        print_result("Get Languages", False, str(e))
        return False


def test_translate_fr_to_ar() -> bool:
    """Test 3: French to Arabic translation"""
    try:
        payload = {
            "text": "Bonjour le monde",
            "source_language": "fr",
            "target_language": "ar",
            "tenant_id": "rag-dz"
        }
        
        response = requests.post(
            f"{BASE_URL}/translator/translate",
            json=payload,
            timeout=10
        )
        
        success = response.status_code == 200
        
        if success:
            data = response.json()
            details = f"Translation: {data['translated_text'][:50]}"
        else:
            details = f"Status: {response.status_code}, Error: {response.text[:100]}"
        
        print_result("French to Arabic Translation", success, details)
        return success
    except Exception as e:
        print_result("French to Arabic Translation", False, str(e))
        return False


def test_translate_en_to_fr() -> bool:
    """Test 4: English to French translation"""
    try:
        payload = {
            "text": "Hello world",
            "source_language": "en",
            "target_language": "fr",
            "tenant_id": "helvetia"
        }
        
        response = requests.post(
            f"{BASE_URL}/translator/translate",
            json=payload,
            timeout=10
        )
        
        success = response.status_code == 200
        
        if success:
            data = response.json()
            details = f"Translation: {data['translated_text']}"
        else:
            details = f"Status: {response.status_code}"
        
        print_result("English to French Translation", success, details)
        return success
    except Exception as e:
        print_result("English to French Translation", False, str(e))
        return False


def test_batch_translation() -> bool:
    """Test 5: Batch translation"""
    try:
        payload = {
            "texts": [
                "Bonjour",
                "Comment allez-vous?",
                "Merci beaucoup"
            ],
            "source_language": "fr",
            "target_language": "en",
            "tenant_id": "helvetia"
        }
        
        response = requests.post(
            f"{BASE_URL}/translator/translate/batch",
            json=payload,
            timeout=15
        )
        
        success = response.status_code == 200
        
        if success:
            data = response.json()
            count = len(data['translations'])
            details = f"Translated {count} texts, {data['total_characters']} chars"
        else:
            details = f"Status: {response.status_code}"
        
        print_result("Batch Translation", success, details)
        return success
    except Exception as e:
        print_result("Batch Translation", False, str(e))
        return False


def test_translation_health() -> bool:
    """Test 6: Translation service health"""
    try:
        response = requests.get(f"{BASE_URL}/translator/health", timeout=5)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            details = f"Status: {data['status']}, Provider: {data['provider']}"
        else:
            details = f"Status: {response.status_code}"
        
        print_result("Translation Service Health", success, details)
        return success
    except Exception as e:
        print_result("Translation Service Health", False, str(e))
        return False


def test_invalid_language() -> bool:
    """Test 7: Invalid language code (should fail gracefully)"""
    try:
        payload = {
            "text": "Test",
            "source_language": "fr",
            "target_language": "zz",  # Invalid
            "tenant_id": "test"
        }
        
        response = requests.post(
            f"{BASE_URL}/translator/translate",
            json=payload,
            timeout=10
        )
        
        # Should return 422 for validation error
        success = response.status_code == 422
        details = f"Correctly rejected invalid language, Status: {response.status_code}"
        
        print_result("Invalid Language Handling", success, details)
        return success
    except Exception as e:
        print_result("Invalid Language Handling", False, str(e))
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 iafactory AI Tools - API Tests")
    print("="*60 + "\n")
    
    tests = [
        test_health_check,
        test_get_languages,
        test_translate_fr_to_ar,
        test_translate_en_to_fr,
        test_batch_translation,
        test_translation_health,
        test_invalid_language
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Summary
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"📊 Results: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    if passed == total:
        print("✅ All tests passed! Your API is ready to use.")
        return 0
    else:
        print(f"❌ {total - passed} test(s) failed. Check the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
