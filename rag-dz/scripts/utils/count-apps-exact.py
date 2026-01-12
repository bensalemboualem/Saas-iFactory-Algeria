#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

apps_dir = Path(r"d:\IAFactory\rag-dz\apps")

# Categorisation exacte
complete_apps = []      # 2+ fichiers avec index.html
stub_apps = []          # 1 seul fichier (juste index.html)
no_index = []           # Pas d'index.html

for app_path in sorted(apps_dir.iterdir()):
    if app_path.is_dir():
        app_name = app_path.name
        index_file = app_path / "index.html"
        file_count = len([f for f in app_path.rglob("*") if f.is_file()])

        if index_file.exists():
            if file_count == 1:
                stub_apps.append((app_name, file_count))
            else:
                complete_apps.append((app_name, file_count))
        else:
            no_index.append((app_name, file_count))

print("="*80)
print("COMPTAGE EXACT DES APPLICATIONS")
print("="*80)

print(f"\n[COMPLETE] APPS COMPLETES (2+ fichiers): {len(complete_apps)}")
for app, count in complete_apps:
    print(f"  {app:<40} ({count} fichiers)")

print(f"\n[STUB] APPS STUBS (1 seul fichier): {len(stub_apps)}")
for app, count in stub_apps:
    print(f"  {app:<40} ({count} fichier)")

print(f"\n[MANQUANT] APPS SANS index.html: {len(no_index)}")
for app, count in no_index:
    print(f"  {app:<40} ({count} fichiers)")

print("\n" + "="*80)
print("RESUME EXACT:")
print(f"  Apps COMPLETES (2+ fichiers):  {len(complete_apps)}")
print(f"  Apps STUBS (1 fichier):        {len(stub_apps)}")
print(f"  Apps SANS index.html:          {len(no_index)}")
print(f"  TOTAL:                         {len(complete_apps) + len(stub_apps) + len(no_index)}")
print("="*80)
