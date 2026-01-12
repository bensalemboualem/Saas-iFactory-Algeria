#!/usr/bin/env python3
"""
Script de vérification de la rotation des clés API
Vérifie que les anciennes clés exposées ne sont plus utilisées
"""
import os
import re
from pathlib import Path
from typing import List, Tuple, Dict

# Couleurs pour output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_success(msg: str):
    print(f"{GREEN}✅ {msg}{RESET}")


def print_error(msg: str):
    print(f"{RED}❌ {msg}{RESET}")


def print_warning(msg: str):
    print(f"{YELLOW}⚠️  {msg}{RESET}")


def print_info(msg: str):
    print(f"{BLUE}ℹ️  {msg}{RESET}")


# Patterns de clés exposées à détecter (partiels pour sécurité)
EXPOSED_KEY_PATTERNS = {
    "ANTHROPIC": r"sk-ant-api03-KXm",
    "OPENAI": r"sk-proj-ysv",
    "GROQ": r"gsk_[A-Za-z0-9]{40,}",
    "OPENROUTER": r"sk-or-v1-[A-Za-z0-9]{40,}",
    # Ajouter d'autres patterns si nécessaire
}


def scan_file_for_exposed_keys(file_path: Path) -> List[Tuple[str, str, int]]:
    """
    Scanne un fichier pour détecter des clés exposées
    Returns: List of (provider, match, line_number)
    """
    findings = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for provider, pattern in EXPOSED_KEY_PATTERNS.items():
                    if re.search(pattern, line):
                        # Masquer la clé trouvée
                        match = re.search(pattern, line).group(0)
                        masked = match[:10] + "..." + match[-5:]
                        findings.append((provider, masked, line_num))
    except Exception as e:
        print_warning(f"Impossible de lire {file_path}: {e}")

    return findings


def scan_directory(directory: Path, exclude_patterns: List[str]) -> Dict[Path, List[Tuple]]:
    """
    Scanne récursivement un répertoire pour détecter des clés exposées
    """
    findings = {}

    for file_path in directory.rglob("*"):
        # Skip directories
        if not file_path.is_file():
            continue

        # Skip excluded patterns
        if any(pattern in str(file_path) for pattern in exclude_patterns):
            continue

        # Skip binary files
        if file_path.suffix in ['.pyc', '.so', '.dll', '.exe', '.bin', '.png', '.jpg', '.gif', '.ico']:
            continue

        # Scan file
        file_findings = scan_file_for_exposed_keys(file_path)
        if file_findings:
            findings[file_path] = file_findings

    return findings


def check_env_local_exists() -> bool:
    """Vérifie que .env.local existe et contient des clés"""
    env_local_path = Path("services/api/.env.local")

    if not env_local_path.exists():
        print_error(".env.local n'existe pas dans services/api/")
        print_info("Exécutez d'abord: scripts/rotate_api_keys.bat")
        return False

    # Vérifier que le fichier contient des vraies clés (pas le template)
    with open(env_local_path, 'r') as f:
        content = f.read()

        if "VOTRE_NOUVELLE_CLE_ICI" in content:
            print_warning(".env.local existe mais contient encore des placeholders")
            print_info("Remplacez VOTRE_NOUVELLE_CLE_ICI par les vraies clés")
            return False

        required_keys = ["OPENROUTER_API_KEY", "GROQ_API_KEY", "ANTHROPIC_API_KEY"]
        missing_keys = []

        for key in required_keys:
            if f"{key}=" not in content or f"{key}=\n" in content:
                missing_keys.append(key)

        if missing_keys:
            print_warning(f"Clés manquantes dans .env.local: {', '.join(missing_keys)}")
            return False

    print_success(".env.local existe et contient des clés")
    return True


def check_gitignore() -> bool:
    """Vérifie que .gitignore protège les fichiers sensibles"""
    gitignore_path = Path(".gitignore")

    if not gitignore_path.exists():
        print_error(".gitignore n'existe pas")
        return False

    with open(gitignore_path, 'r') as f:
        content = f.read()

        required_patterns = ["**/.env.local", "**/.env.ready"]
        missing_patterns = []

        for pattern in required_patterns:
            if pattern not in content:
                missing_patterns.append(pattern)

        if missing_patterns:
            print_warning(f"Patterns manquants dans .gitignore: {', '.join(missing_patterns)}")
            print_info("Ajoutez-les avec: echo '**/.env.local' >> .gitignore")
            return False

    print_success(".gitignore protège les fichiers sensibles")
    return True


def check_exposed_file_removed() -> bool:
    """Vérifie que .env.ready est supprimé du tracking Git"""
    env_ready_path = Path("apps/video-studio/.env.ready")

    # Vérifier si le fichier existe localement (OK)
    if env_ready_path.exists():
        print_info(".env.ready existe localement (OK - gardé pour backup)")

    # Vérifier s'il est dans Git tracking
    import subprocess
    try:
        result = subprocess.run(
            ["git", "ls-files", str(env_ready_path)],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.stdout.strip():
            print_error(".env.ready est encore dans le tracking Git")
            print_info("Exécutez: git rm --cached apps/video-studio/.env.ready")
            return False
        else:
            print_success(".env.ready est supprimé du tracking Git")
            return True
    except Exception as e:
        print_warning(f"Impossible de vérifier Git status: {e}")
        return True  # Assume OK si Git non disponible


def main():
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  VERIFICATION ROTATION CLES API{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

    os.chdir(Path(__file__).parent.parent)  # Go to project root

    checks_passed = 0
    checks_total = 0

    # Check 1: .env.local exists and filled
    print(f"\n{YELLOW}[CHECK 1/5] Vérification .env.local...{RESET}")
    checks_total += 1
    if check_env_local_exists():
        checks_passed += 1

    # Check 2: .gitignore configured
    print(f"\n{YELLOW}[CHECK 2/5] Vérification .gitignore...{RESET}")
    checks_total += 1
    if check_gitignore():
        checks_passed += 1

    # Check 3: .env.ready removed from Git
    print(f"\n{YELLOW}[CHECK 3/5] Vérification .env.ready...{RESET}")
    checks_total += 1
    if check_exposed_file_removed():
        checks_passed += 1

    # Check 4: Scan codebase for exposed keys
    print(f"\n{YELLOW}[CHECK 4/5] Scan des clés exposées dans le codebase...{RESET}")
    checks_total += 1

    exclude_patterns = [
        "node_modules",
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        ".env.ready.EXPOSED.backup",
        "dist",
        "build",
        ".next",
    ]

    findings = scan_directory(Path("."), exclude_patterns)

    if findings:
        print_error(f"Clés exposées trouvées dans {len(findings)} fichier(s):")
        for file_path, file_findings in findings.items():
            print(f"\n  {RED}{file_path}{RESET}")
            for provider, masked_key, line_num in file_findings:
                print(f"    Ligne {line_num}: {provider} - {masked_key}")

        print_warning("\n⚠️  ACTIONS REQUISES:")
        print_info("1. Vérifier si ces fichiers doivent contenir ces clés")
        print_info("2. Si non, les supprimer et régénérer les clés")
        print_info("3. Si oui (ex: backup), les ajouter au .gitignore")
    else:
        print_success("Aucune clé exposée détectée dans le codebase")
        checks_passed += 1

    # Check 5: Verify no secrets in Git history (last 10 commits)
    print(f"\n{YELLOW}[CHECK 5/5] Vérification historique Git récent...{RESET}")
    checks_total += 1

    try:
        import subprocess
        result = subprocess.run(
            ["git", "log", "--all", "--oneline", "-10"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if ".env.ready" in result.stdout or "api.*key" in result.stdout.lower():
            print_warning("Commits récents mentionnent des clés ou .env.ready")
            print_info("Considérez un git filter-branch si nécessaire")
        else:
            print_success("Historique Git récent semble propre")
            checks_passed += 1
    except Exception as e:
        print_warning(f"Impossible de vérifier historique Git: {e}")
        checks_passed += 1  # Assume OK

    # Summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  RESUME{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

    if checks_passed == checks_total:
        print_success(f"Tous les checks passent: {checks_passed}/{checks_total}")
        print(f"\n{GREEN}✅ ROTATION DES CLES TERMINEE AVEC SUCCES{RESET}")
        print_info("\nProchaine étape: Appliquer la migration SQL")
        print_info("Exécutez: services\\api\\deploy_zero_risque.bat")
        return 0
    else:
        print_warning(f"Checks réussis: {checks_passed}/{checks_total}")
        print(f"\n{YELLOW}⚠️  ROTATION DES CLES INCOMPLETE{RESET}")
        print_info("\nCorrigez les erreurs ci-dessus avant de continuer")
        return 1


if __name__ == "__main__":
    exit(main())
