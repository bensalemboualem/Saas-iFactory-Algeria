#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path

apps_dir = Path(r"d:\IAFactory\rag-dz\apps")

with_index = []
without_index = []
incomplete = []

# Parcourir tous les dossiers d'apps
for app_path in sorted(apps_dir.iterdir()):
    if app_path.is_dir():
        app_name = app_path.name
        index_file = app_path / "index.html"

        # Compter les fichiers
        files = list(app_path.rglob("*"))
        file_count = len([f for f in files if f.is_file()])

        if index_file.exists():
            with_index.append((app_name, file_count))
        else:
            without_index.append((app_name, file_count))

        # App incomplete si pas d'index ou tres peu de fichiers
        if not index_file.exists() or file_count < 2:
            incomplete.append((app_name, file_count, index_file.exists()))

print("="*80)
print("VERIFICATION DES APPLICATIONS")
print("="*80)

print(f"\n[OK] APPS COMPLETES (avec index.html): {len(with_index)}")
for app, count in with_index:
    print(f"  [OK] {app:<40} ({count} fichiers)")

print(f"\n[!!] APPS SANS index.html: {len(without_index)}")
for app, count in without_index:
    print(f"  [!!] {app:<40} ({count} fichiers)")

print(f"\n[??] APPS POTENTIELLEMENT INCOMPLETES: {len(incomplete)}")
for app, count, has_index in incomplete:
    status = "index.html: OUI" if has_index else "index.html: NON"
    print(f"  [??] {app:<40} ({count} fichiers, {status})")

print(f"\nRESUME:")
print(f"  Total apps:           {len(with_index) + len(without_index)}")
print(f"  Apps completes:       {len(with_index)}")
print(f"  Apps sans index:      {len(without_index)}")
print(f"  Apps incompletes:     {len(incomplete)}")
if (len(with_index) + len(without_index)) > 0:
    print(f"  Taux de completion:   {len(with_index)/(len(with_index)+len(without_index))*100:.1f}%")

print("\n" + "="*80)
if len(without_index) > 0 or len(incomplete) > 10:
    print("[ATTENTION] Il y a des apps incompletes!")
    print("[ATTENTION] NE PAS DEPLOYER SUR VPS sans corriger d'abord!")
else:
    print("[OK] Toutes les apps principales sont completes!")
    print("[OK] Pret pour le deploiement VPS!")
print("="*80)
