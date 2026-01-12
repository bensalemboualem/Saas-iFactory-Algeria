#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de tous les ports des interfaces RAG.dz
Vérifie que chaque service est accessible sur son port dédié
"""

import socket
import time
from typing import Dict, List, Tuple
import sys
import os

# Fix Windows console encoding
if sys.platform == "win32":
    os.system("chcp 65001 >nul 2>&1")
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

# Configuration des ports à tester
PORTS_CONFIG = {
    "Frontends": [
        (3737, "Archon UI", "http://localhost:3737"),
        (5173, "RAG-UI Simple", "http://localhost:5173"),
        (5174, "Bolt.diy AI Editor", "http://localhost:5174"),
        (3001, "Grafana Monitoring", "http://localhost:3001"),
    ],
    "Backend & API": [
        (8180, "FastAPI Backend", "http://localhost:8180/docs"),
    ],
    "Databases": [
        (5432, "PostgreSQL", "localhost:5432"),
        (6333, "Qdrant Vector DB", "http://localhost:6333/dashboard"),
        (6334, "Qdrant gRPC", "localhost:6334"),
        (6379, "Redis Cache", "localhost:6379"),
    ],
    "Monitoring": [
        (9090, "Prometheus", "http://localhost:9090"),
        (9121, "Redis Exporter", "http://localhost:9121/metrics"),
        (9187, "Postgres Exporter", "http://localhost:9187/metrics"),
    ],
}


def check_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """Vérifie si un port est ouvert"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.error:
        return False


def print_header():
    """Affiche l'en-tête du test"""
    print("\n" + "=" * 80)
    print("🌐 RAG.dz - Test de tous les Ports")
    print("=" * 80)
    print(f"⏰ Test démarré à {time.strftime('%Y-%m-%d %H:%M:%S')}\n")


def print_category(category: str):
    """Affiche le nom de la catégorie"""
    print(f"\n📦 {category}")
    print("─" * 80)


def print_result(port: int, name: str, url: str, is_open: bool):
    """Affiche le résultat d'un test"""
    status = "✅ UP" if is_open else "❌ DOWN"
    port_str = f"{port:5d}"
    name_str = f"{name:30s}"
    print(f"  {port_str}  {status}  {name_str}  {url}")


def print_summary(total: int, up: int, down: int):
    """Affiche le résumé final"""
    print("\n" + "=" * 80)
    print("📊 Résumé")
    print("=" * 80)
    print(f"  Total services:    {total:3d}")
    print(f"  ✅ En ligne:       {up:3d} ({up * 100 // total if total > 0 else 0}%)")
    print(f"  ❌ Hors ligne:     {down:3d} ({down * 100 // total if total > 0 else 0}%)")
    print("=" * 80)


def print_recommendations(down_services: List[Tuple[int, str, str]]):
    """Affiche les recommandations pour les services hors ligne"""
    if not down_services:
        print("\n🎉 Tous les services sont en ligne ! Excellent travail !")
        return

    print("\n⚠️  Services Hors Ligne - Actions Recommandées")
    print("─" * 80)

    for port, name, url in down_services:
        print(f"\n  Port {port} - {name}")

        # Recommandations spécifiques
        if port == 3737:
            print("    → docker-compose up -d frontend")
        elif port == 5173:
            print("    → docker-compose up -d rag-ui")
        elif port == 5174:
            print("    → docker-compose --profile bolt up -d")
        elif port == 8180:
            print("    → docker-compose up -d backend")
        elif port in [5432, 6333, 6334, 6379]:
            service_name = {
                5432: "postgres",
                6333: "qdrant",
                6334: "qdrant",
                6379: "redis",
            }[port]
            print(f"    → docker-compose up -d {service_name}")
        elif port in [9090, 9121, 9187, 3001]:
            service_name = {
                9090: "prometheus",
                9121: "redis-exporter",
                9187: "postgres-exporter",
                3001: "grafana",
            }[port]
            print(f"    → docker-compose up -d {service_name}")


def print_access_guide():
    """Affiche le guide d'accès rapide"""
    print("\n🚀 Accès Rapide aux Interfaces")
    print("─" * 80)
    print("\n  Interfaces Principales:")
    print("    • Archon UI:      http://localhost:3737")
    print("    • RAG-UI:         http://localhost:5173")
    print("    • Bolt.diy:       http://localhost:5174")
    print("\n  API & Documentation:")
    print("    • Swagger UI:     http://localhost:8180/docs")
    print("    • API Health:     http://localhost:8180/health")
    print("\n  Monitoring:")
    print("    • Grafana:        http://localhost:3001  (admin/admin)")
    print("    • Prometheus:     http://localhost:9090")
    print("    • Qdrant:         http://localhost:6333/dashboard")
    print("=" * 80)


def main():
    """Fonction principale"""
    print_header()

    total_services = 0
    up_services = 0
    down_services = []

    # Tester tous les ports par catégorie
    for category, ports in PORTS_CONFIG.items():
        print_category(category)

        for port, name, url in ports:
            total_services += 1
            is_open = check_port("localhost", port)

            if is_open:
                up_services += 1
            else:
                down_services.append((port, name, url))

            print_result(port, name, url, is_open)

    # Afficher le résumé
    down_count = total_services - up_services
    print_summary(total_services, up_services, down_count)

    # Afficher les recommandations
    print_recommendations(down_services)

    # Afficher le guide d'accès
    if up_services > 0:
        print_access_guide()

    # Code de sortie
    print()
    if down_count == 0:
        print("✅ TOUS LES SERVICES SONT OPÉRATIONNELS !")
        return 0
    else:
        print(f"⚠️  {down_count} service(s) nécessite(nt) votre attention.")
        print("\n💡 Astuce: Exécutez 'docker-compose up -d' pour démarrer tous les services.")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu par l'utilisateur")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)
