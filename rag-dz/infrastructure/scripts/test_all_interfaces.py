#!/usr/bin/env python3
"""
Script de test automatique de toutes les interfaces RAG.dz
Usage: python test_all_interfaces.py
"""

import requests
import json
import time
from typing import Dict, List, Tuple
from dataclasses import dataclass
import sys

# Configuration
BASE_URL = "http://localhost:8180"
FRONTEND_URL = "http://localhost:5173"
PROMETHEUS_URL = "http://localhost:9090"
GRAFANA_URL = "http://localhost:3001"
QDRANT_URL = "http://localhost:6333"
API_KEY = "test-api-key-ragdz-2024"

# Couleurs pour output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


@dataclass
class TestResult:
    name: str
    passed: bool
    message: str
    duration: float


class InterfaceTester:
    """Testeur d'interfaces RAG.dz"""

    def __init__(self):
        self.results: List[TestResult] = []
        self.headers = {"X-API-Key": API_KEY}

    def print_header(self, text: str):
        """Affiche un en-tête"""
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}{text:^60}{RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")

    def print_test(self, name: str, passed: bool, message: str = ""):
        """Affiche le résultat d'un test"""
        icon = f"{GREEN}✓{RESET}" if passed else f"{RED}✗{RESET}"
        status = f"{GREEN}PASS{RESET}" if passed else f"{RED}FAIL{RESET}"
        print(f"{icon} {name:50s} [{status}]")
        if message and not passed:
            print(f"  {YELLOW}→ {message}{RESET}")

    def add_result(self, name: str, passed: bool, message: str, duration: float):
        """Ajoute un résultat de test"""
        self.results.append(TestResult(name, passed, message, duration))
        self.print_test(name, passed, message)

    def test_service(self, name: str, url: str, timeout: int = 5) -> bool:
        """Test générique de disponibilité service"""
        start = time.time()
        try:
            response = requests.get(url, timeout=timeout)
            duration = time.time() - start
            passed = response.status_code == 200
            message = f"Status {response.status_code}" if not passed else ""
            self.add_result(name, passed, message, duration)
            return passed
        except Exception as e:
            duration = time.time() - start
            self.add_result(name, False, str(e), duration)
            return False

    # ========================================
    # TESTS BACKEND
    # ========================================

    def test_backend(self):
        """Tests du backend API"""
        self.print_header("🔧 TESTS BACKEND API")

        # Health check
        self.test_service("Backend Health Check", f"{BASE_URL}/health")

        # Metrics
        self.test_service("Prometheus Metrics", f"{BASE_URL}/metrics")

        # API Docs
        self.test_service("Swagger Documentation", f"{BASE_URL}/docs")

        # Test avec API key
        start = time.time()
        try:
            response = requests.post(
                f"{BASE_URL}/api/test/embed",
                headers=self.headers,
                json={},
                timeout=30  # Embeddings peuvent prendre du temps
            )
            duration = time.time() - start
            passed = response.status_code in [200, 422]  # 422 = validation error OK
            message = f"Status {response.status_code}" if not passed else ""
            self.add_result("Embed Endpoint (with API key)", passed, message, duration)
        except Exception as e:
            duration = time.time() - start
            self.add_result("Embed Endpoint (with API key)", False, str(e), duration)

        # Test sans API key (doit échouer)
        start = time.time()
        try:
            response = requests.post(
                f"{BASE_URL}/api/query",
                json={"query": "test"},
                timeout=5
            )
            duration = time.time() - start
            # Doit retourner 401 (Unauthorized)
            passed = response.status_code == 401
            message = "Auth should be required" if not passed else ""
            self.add_result("API Key Required (security)", passed, message, duration)
        except Exception as e:
            duration = time.time() - start
            self.add_result("API Key Required (security)", False, str(e), duration)

        # Test Query endpoint
        start = time.time()
        try:
            response = requests.post(
                f"{BASE_URL}/api/query",
                headers=self.headers,
                json={
                    "query": "test query",
                    "max_results": 5,
                    "use_cache": True
                },
                timeout=30
            )
            duration = time.time() - start
            passed = response.status_code == 200
            if passed:
                data = response.json()
                # Vérifier structure réponse
                passed = all(k in data for k in ["answer", "results", "query", "search_time_ms"])
            message = f"Status {response.status_code}" if not passed else ""
            self.add_result("Query Endpoint", passed, message, duration)

            # Vérifier cache
            if passed and "from_cache" in data:
                cache_info = f"Cache: {data.get('from_cache', False)}"
                print(f"  {BLUE}→ {cache_info}{RESET}")

        except Exception as e:
            duration = time.time() - start
            self.add_result("Query Endpoint", False, str(e), duration)

        # Test Pagination
        start = time.time()
        try:
            response = requests.get(
                f"{BASE_URL}/api/search",
                headers=self.headers,
                params={"query": "test", "page": 1, "page_size": 10},
                timeout=10
            )
            duration = time.time() - start
            passed = response.status_code == 200
            if passed:
                data = response.json()
                passed = "items" in data and "pagination" in data
            message = f"Status {response.status_code}" if not passed else ""
            self.add_result("Paginated Search", passed, message, duration)
        except Exception as e:
            duration = time.time() - start
            self.add_result("Paginated Search", False, str(e), duration)

        # Test Rate Limiting
        print(f"\n{YELLOW}Testing rate limiting (will make 65 requests)...{RESET}")
        start = time.time()
        rate_limited = False
        for i in range(65):
            try:
                response = requests.get(
                    f"{BASE_URL}/health",
                    headers=self.headers,
                    timeout=2
                )
                if response.status_code == 429:
                    rate_limited = True
                    duration = time.time() - start
                    self.add_result("Rate Limiting (60/min)", True, f"Limited at request {i+1}", duration)
                    break
            except:
                pass
            time.sleep(0.05)

        if not rate_limited:
            duration = time.time() - start
            self.add_result("Rate Limiting (60/min)", False, "Not triggered after 65 requests", duration)

    # ========================================
    # TESTS FRONTEND
    # ========================================

    def test_frontend(self):
        """Tests du frontend"""
        self.print_header("🎨 TESTS FRONTEND")

        # Frontend accessible
        self.test_service("Frontend Accessibility", FRONTEND_URL, timeout=10)

        # Vérifier assets (si build)
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            if response.status_code == 200:
                # Vérifier que ce n'est pas juste un proxy
                passed = len(response.text) > 100
                message = "Empty response" if not passed else ""
                self.add_result("Frontend Content", passed, message, 0)
        except Exception as e:
            self.add_result("Frontend Content", False, str(e), 0)

    # ========================================
    # TESTS BASE DE DONNÉES
    # ========================================

    def test_database(self):
        """Tests de la base de données"""
        self.print_header("🗄️  TESTS BASE DE DONNÉES")

        # PostgreSQL (via backend health)
        start = time.time()
        try:
            # Le backend ne démarre pas sans DB
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            duration = time.time() - start
            passed = response.status_code == 200
            self.add_result("PostgreSQL Connection", passed, "", duration)
        except Exception as e:
            duration = time.time() - start
            self.add_result("PostgreSQL Connection", False, str(e), duration)

    # ========================================
    # TESTS CACHE REDIS
    # ========================================

    def test_redis(self):
        """Tests du cache Redis"""
        self.print_header("💾 TESTS CACHE REDIS")

        # Test via query cache
        print(f"{YELLOW}Making 2 identical queries to test cache...{RESET}")

        # Première requête (sans cache)
        start1 = time.time()
        try:
            response1 = requests.post(
                f"{BASE_URL}/api/query",
                headers=self.headers,
                json={"query": "cache test unique query", "use_cache": True},
                timeout=30
            )
            duration1 = time.time() - start1

            if response1.status_code == 200:
                data1 = response1.json()
                time1 = data1.get("search_time_ms", 0)

                # Deuxième requête (avec cache)
                time.sleep(0.5)
                start2 = time.time()
                response2 = requests.post(
                    f"{BASE_URL}/api/query",
                    headers=self.headers,
                    json={"query": "cache test unique query", "use_cache": True},
                    timeout=30
                )
                duration2 = time.time() - start2
                data2 = response2.json()
                time2 = data2.get("search_time_ms", 0)

                # Cache devrait être plus rapide
                from_cache = data2.get("from_cache", False)
                passed = from_cache or duration2 < duration1

                message = f"1st: {time1}ms, 2nd: {time2}ms, from_cache: {from_cache}"
                self.add_result("Redis Cache Working", passed, message, duration2)

                if passed and from_cache:
                    speedup = duration1 / duration2 if duration2 > 0 else 1
                    print(f"  {GREEN}→ Speedup: {speedup:.1f}x{RESET}")
            else:
                self.add_result("Redis Cache Working", False, f"Status {response1.status_code}", duration1)

        except Exception as e:
            self.add_result("Redis Cache Working", False, str(e), 0)

    # ========================================
    # TESTS QDRANT
    # ========================================

    def test_qdrant(self):
        """Tests de Qdrant Vector DB"""
        self.print_header("🔍 TESTS QDRANT VECTOR DB")

        # Health check
        self.test_service("Qdrant Health", f"{QDRANT_URL}/health")

        # Collections
        start = time.time()
        try:
            response = requests.get(f"{QDRANT_URL}/collections", timeout=5)
            duration = time.time() - start
            passed = response.status_code == 200
            if passed:
                data = response.json()
                collections = data.get("result", {}).get("collections", [])
                print(f"  {BLUE}→ Collections found: {len(collections)}{RESET}")
            message = f"Status {response.status_code}" if not passed else ""
            self.add_result("Qdrant Collections API", passed, message, duration)
        except Exception as e:
            duration = time.time() - start
            self.add_result("Qdrant Collections API", False, str(e), duration)

    # ========================================
    # TESTS MONITORING
    # ========================================

    def test_monitoring(self):
        """Tests du monitoring"""
        self.print_header("📊 TESTS MONITORING")

        # Prometheus
        self.test_service("Prometheus Web UI", PROMETHEUS_URL)

        # Prometheus targets
        start = time.time()
        try:
            response = requests.get(f"{PROMETHEUS_URL}/api/v1/targets", timeout=5)
            duration = time.time() - start
            passed = response.status_code == 200
            if passed:
                data = response.json()
                if data.get("status") == "success":
                    targets = data.get("data", {}).get("activeTargets", [])
                    up_count = sum(1 for t in targets if t.get("health") == "up")
                    total = len(targets)
                    print(f"  {BLUE}→ Targets UP: {up_count}/{total}{RESET}")
                    passed = up_count > 0
            message = f"Status {response.status_code}" if not passed else ""
            self.add_result("Prometheus Targets", passed, message, duration)
        except Exception as e:
            duration = time.time() - start
            self.add_result("Prometheus Targets", False, str(e), duration)

        # Grafana
        self.test_service("Grafana Web UI", GRAFANA_URL)

        # Grafana health
        start = time.time()
        try:
            response = requests.get(f"{GRAFANA_URL}/api/health", timeout=5)
            duration = time.time() - start
            passed = response.status_code == 200
            message = f"Status {response.status_code}" if not passed else ""
            self.add_result("Grafana API Health", passed, message, duration)
        except Exception as e:
            duration = time.time() - start
            self.add_result("Grafana API Health", False, str(e), duration)

    # ========================================
    # RAPPORT FINAL
    # ========================================

    def print_summary(self):
        """Affiche le résumé des tests"""
        self.print_header("📋 RÉSUMÉ DES TESTS")

        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        success_rate = (passed / total * 100) if total > 0 else 0

        print(f"Total tests:     {total}")
        print(f"{GREEN}Passed:          {passed}{RESET}")
        print(f"{RED}Failed:          {failed}{RESET}")
        print(f"Success rate:    {success_rate:.1f}%")

        # Temps moyen
        avg_duration = sum(r.duration for r in self.results) / total if total > 0 else 0
        print(f"Average time:    {avg_duration:.2f}s")

        # Liste des échecs
        if failed > 0:
            print(f"\n{RED}Failed tests:{RESET}")
            for r in self.results:
                if not r.passed:
                    print(f"  • {r.name}")
                    if r.message:
                        print(f"    → {r.message}")

        print(f"\n{BLUE}{'='*60}{RESET}")

        # Status global
        if failed == 0:
            print(f"{GREEN}✓ ALL TESTS PASSED!{RESET}")
            return 0
        else:
            print(f"{RED}✗ SOME TESTS FAILED{RESET}")
            return 1

    def run_all_tests(self):
        """Lance tous les tests"""
        print(f"{BLUE}")
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║        RAG.dz - Test Automatique des Interfaces          ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print(f"{RESET}")

        print(f"{YELLOW}Configuration:{RESET}")
        print(f"  Backend:     {BASE_URL}")
        print(f"  Frontend:    {FRONTEND_URL}")
        print(f"  Prometheus:  {PROMETHEUS_URL}")
        print(f"  Grafana:     {GRAFANA_URL}")
        print(f"  Qdrant:      {QDRANT_URL}")

        # Lancer tous les tests
        self.test_backend()
        self.test_frontend()
        self.test_database()
        self.test_redis()
        self.test_qdrant()
        self.test_monitoring()

        # Résumé
        return self.print_summary()


def main():
    """Point d'entrée principal"""
    tester = InterfaceTester()
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
