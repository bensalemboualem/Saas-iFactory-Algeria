#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculer la taille totale du projet pour Hetzner VPS
"""
import os
from pathlib import Path
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_dir_size_safe(path, max_depth=10, current_depth=0):
    """Calculer taille avec protection contre chemins trop longs"""
    total = 0

    if current_depth > max_depth:
        return 0

    try:
        for entry in os.scandir(path):
            try:
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat().st_size
                elif entry.is_dir(follow_symlinks=False):
                    # Ignorer node_modules/.pnpm pour éviter chemins trop longs
                    if '.pnpm' not in entry.path:
                        total += get_dir_size_safe(entry.path, max_depth, current_depth + 1)
            except (PermissionError, OSError, FileNotFoundError):
                continue
    except (PermissionError, OSError, FileNotFoundError):
        pass

    return total

def format_bytes(size):
    """Formater en B, KB, MB, GB"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f'{size:.2f} {unit}'
        size /= 1024.0
    return f'{size:.2f} TB'

def main():
    base_path = Path(r'd:\IAFactory\rag-dz')

    print('='*80)
    print('CALCUL DE LA TAILLE DU PROJET RAG-DZ POUR HETZNER VPS')
    print('='*80)
    print()

    # Composants à mesurer
    components = {
        '46 Applications (apps/)': base_path / 'apps',
        'Backend FastAPI': base_path / 'backend',
        'Frontend Archon UI': base_path / 'frontend' / 'archon-ui',
        'Frontend RAG UI': base_path / 'frontend' / 'rag-ui',
        'Bolt-DIY': base_path / 'bolt-diy',
        'BMAD': base_path / 'bmad',
        'Scripts': base_path / 'scripts',
        'Nginx config': base_path / 'nginx',
        'Docker configs': base_path
    }

    print('📊 TAILLE DES COMPOSANTS:')
    print()

    total_size = 0
    sizes = {}

    for name, path in components.items():
        if path.exists():
            if name == 'Docker configs':
                # Compter seulement les fichiers docker à la racine
                size = sum(f.stat().st_size for f in path.glob('docker-compose*.yml') if f.is_file())
                size += sum(f.stat().st_size for f in path.glob('Dockerfile*') if f.is_file())
            else:
                size = get_dir_size_safe(path)

            sizes[name] = size
            total_size += size
            print(f'  {name:<35} {format_bytes(size):>15}')
        else:
            print(f'  {name:<35} {'[NON TROUVÉ]':>15}')

    print()
    print('─'*80)
    print(f'  {'TOTAL CODE SOURCE':<35} {format_bytes(total_size):>15}')
    print('='*80)
    print()

    # Estimations des dépendances
    print('📦 ESTIMATION DES DÉPENDANCES:')
    print()

    # Essayer de compter réellement node_modules si possible
    node_modules_paths = [
        base_path / 'frontend' / 'archon-ui' / 'node_modules',
        base_path / 'frontend' / 'rag-ui' / 'node_modules',
        base_path / 'bolt-diy' / 'node_modules'
    ]

    node_modules_size = 0
    for nm_path in node_modules_paths:
        if nm_path.exists():
            # Compter juste les fichiers directs pour estimation
            try:
                size = get_dir_size_safe(nm_path, max_depth=3)
                node_modules_size += size
            except:
                pass

    if node_modules_size > 0:
        print(f'  node_modules (mesuré)         {format_bytes(node_modules_size):>15}')
    else:
        node_modules_size = 500 * 1024 * 1024  # 500MB estimation
        print(f'  node_modules (estimé)         {format_bytes(node_modules_size):>15}')

    python_venv = 200 * 1024 * 1024  # 200MB
    docker_images = 2 * 1024 * 1024 * 1024  # 2GB
    database = 1 * 1024 * 1024 * 1024  # 1GB pour PostgreSQL

    print(f'  Python venv (estimé)          {format_bytes(python_venv):>15}')
    print(f'  Docker images (estimé)        {format_bytes(docker_images):>15}')
    print(f'  PostgreSQL + data (estimé)    {format_bytes(database):>15}')

    print()
    print('─'*80)

    total_with_deps = total_size + node_modules_size + python_venv + docker_images + database

    print(f'  {'TOTAL AVEC DÉPENDANCES':<35} {format_bytes(total_with_deps):>15}')
    print('='*80)
    print()

    # Calcul avec marge de sécurité (logs, uploads, backups)
    safety_margin = total_with_deps * 1.5  # 150% pour marge confortable

    print('🔒 AVEC MARGE DE SÉCURITÉ (logs, uploads, backups):')
    print(f'  Total × 1.5 =                 {format_bytes(safety_margin):>15}')
    print()
    print('='*80)
    print()

    # Recommandations Hetzner
    print('💡 RECOMMANDATIONS HETZNER VPS:')
    print()

    total_gb = safety_margin / (1024**3)

    if total_gb < 20:
        print('✅ CX22  (40 GB SSD)   - €5.83/mois    - SUFFISANT')
        print('✅ CX32  (80 GB SSD)   - €11.05/mois   - RECOMMANDÉ (confortable)')
        print('   CX42  (160 GB SSD)  - €21.49/mois   - Large (pour forte croissance)')
    elif total_gb < 40:
        print('⚠️  CX22  (40 GB SSD)   - €5.83/mois    - JUSTE (risqué)')
        print('✅ CX32  (80 GB SSD)   - €11.05/mois   - RECOMMANDÉ')
        print('   CX42  (160 GB SSD)  - €21.49/mois   - Confortable')
    else:
        print('❌ CX22  (40 GB SSD)   - €5.83/mois    - INSUFFISANT')
        print('⚠️  CX32  (80 GB SSD)   - €11.05/mois   - JUSTE')
        print('✅ CX42  (160 GB SSD)  - €21.49/mois   - RECOMMANDÉ')

    print()
    print('📝 NOTES:')
    print('  • Prévoir minimum 30-40% d\'espace libre en permanence')
    print('  • Les backups automatiques nécessitent espace supplémentaire')
    print('  • Les logs peuvent croître rapidement en production')
    print('  • Uploads utilisateurs (documents OCR, etc.) = espace variable')
    print()
    print('='*80)
    print()

    print('🎯 RECOMMANDATION FINALE:')
    print()
    if total_gb < 15:
        print('  ➡️  Hetzner CX22 (40 GB) est SUFFISANT pour démarrer')
        print('      Vous pouvez upgrader plus tard si nécessaire')
    elif total_gb < 25:
        print('  ➡️  Hetzner CX32 (80 GB) est RECOMMANDÉ')
        print('      Bon équilibre prix/performance/espace')
    else:
        print('  ➡️  Hetzner CX42 (160 GB) est RECOMMANDÉ')
        print('      Espace confortable pour production')

    print()
    print('='*80)

if __name__ == '__main__':
    main()
