#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

# Variables CSS de la landing page (RÉFÉRENCE)
LANDING_CSS = """
        :root {
            --bg: #020617;
            --bg-alt: #020617;
            --card: #020617;
            --border: rgba(255, 255, 255, 0.12);
            --primary: #00a651;
            --primary-dark: #008c45;
            --text: #f8fafc;
            --text-primary: #f8fafc;
            --text-secondary: rgba(248, 250, 252, 0.75);
            --muted: rgba(248, 250, 252, 0.75);
            --shadow: 0 20px 60px rgba(0, 0, 0, 0.55);

            /* Variables compatibles */
            --bg-card: #020617;
            --bg-secondary: #0f172a;
            --bg-dark: #020617;
            --border-primary: rgba(255, 255, 255, 0.12);
            --accent: #00a651;
            --accent-primary: #00a651;
        }

        [data-theme="light"] {
            --bg: #f7f5f0;
            --bg-alt: #f7f5f0;
            --card: #f7f5f0;
            --border: rgba(0, 0, 0, 0.08);
            --primary: #00a651;
            --primary-dark: #008c45;
            --text: #0f172a;
            --text-primary: #0f172a;
            --text-secondary: rgba(15, 23, 42, 0.7);
            --muted: rgba(15, 23, 42, 0.7);
            --shadow: 0 20px 60px rgba(15, 23, 42, 0.25);

            /* Variables compatibles */
            --bg-card: #ffffff;
            --bg-secondary: #f7f5f0;
            --bg-dark: #f7f5f0;
            --border-primary: rgba(0, 0, 0, 0.08);
            --accent: #00a651;
            --accent-primary: #00a651;
        }
"""

UNIFIED_SYSTEM = """
    <!-- Footer Unifié -->
    <div data-iaf-footer></div>

    <!-- Chatbot Unifié -->
    <button class="iaf-chatbot-btn" onclick="IAFactory.toggleChatbot()"
            title="Aide" aria-label="Aide">
        💬
    </button>

    <!-- Scripts Unifiés -->
    <script src="/apps/shared/iafactory-unified.js"></script>
"""

def fix_app(app_path):
    """Corrige une app complètement"""
    index_file = app_path / "index.html"

    if not index_file.exists():
        return False, "No index.html"

    # Backup
    backup_file = str(index_file) + f".backup-fix-all-{os.getpid()}"
    with open(index_file, "r", encoding="utf-8") as f:
        original = f.read()
    with open(backup_file, "w", encoding="utf-8") as f:
        f.write(original)

    content = original

    # 1. Ajouter data-iaf-auto-init si manquant
    if "data-iaf-auto-init" not in content:
        content = re.sub(
            r"<html([^>]*)>",
            r"<html\1 data-iaf-auto-init>",
            content,
            count=1
        )

    # 2. Supprimer TOUT ancien chatbot inline
    # Pattern pour chatbot inline complet
    content = re.sub(
        r"<!-- IAF Chatbot.*?</div>\s*</div>",
        "",
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<div class=["\']iaf-chatbot["\'].*?</div>\s*</div>',
        "",
        content,
        flags=re.DOTALL
    )

    # Supprimer anciens chatbots commentés
    content = re.sub(
        r"<!-- .*CHATBOT.*?-->",
        "",
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    # Supprimer iframes chatbot
    content = re.sub(r"<iframe[^>]*chatbot[^>]*>.*?</iframe>", "", content, flags=re.DOTALL)

    # Supprimer help-bubble
    content = re.sub(r"<div[^>]*help-bubble[^>]*>.*?</div>", "", content, flags=re.DOTALL)

    # Supprimer sendHelpMessage
    content = re.sub(r"function sendHelpMessage\s*\([^)]*\)\s*\{[^}]*\}", "", content, flags=re.DOTALL)

    # 3. Remplacer/Ajouter CSS variables
    if ":root" in content:
        # Remplacer le :root existant ET le [data-theme="light"] s'il existe
        content = re.sub(
            r":root\s*\{[^}]+\}(?:\s*\[data-theme=[\"']light[\"']\]\s*\{[^}]+\})?",
            LANDING_CSS,
            content,
            flags=re.DOTALL,
            count=1
        )
    elif "<style" in content:
        # Ajouter après le premier <style>
        content = re.sub(
            r"(<style[^>]*>)",
            r"\1" + LANDING_CSS,
            content,
            count=1
        )

    # 4. Nettoyer les fins et doublons
    # Supprimer balises fermantes
    content = content.replace("</body>", "").replace("</html>", "")

    # Supprimer commentaires bizarres de fin
    content = re.sub(r"\\1\s*=+\s*-->$", "", content.strip())
    content = content.rstrip()

    # Supprimer doublons de iafactory-unified.js et data-iaf-footer
    lines = content.split("\n")
    seen_unified = False
    seen_footer = False
    seen_chatbot = False
    cleaned_lines = []

    for line in lines:
        # Skip les doublons
        if "iafactory-unified.js" in line:
            if seen_unified:
                continue
            seen_unified = True
        if "data-iaf-footer" in line:
            if seen_footer:
                continue
            seen_footer = True
        if "iaf-chatbot-btn" in line and "IAFactory.toggleChatbot" in line:
            if seen_chatbot:
                continue
            seen_chatbot = True

        cleaned_lines.append(line)

    content = "\n".join(cleaned_lines)

    # 5. Ajouter système unifié à la fin
    if "iafactory-unified.js" not in content or "iaf-chatbot-btn" not in content:
        content += "\n" + UNIFIED_SYSTEM + "\n</body>\n</html>"
    else:
        content += "\n</body>\n</html>"

    # Écrire le fichier corrigé
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(content)

    return True, "Fixed"

# Apps à exclure
EXCLUDED = ["shared", "landing", "school-erp"]

def main():
    apps_dir = Path("/opt/iafactory-rag-dz/apps")

    fixed = 0
    skipped = 0
    errors = 0

    for app_path in sorted(apps_dir.iterdir()):
        if not app_path.is_dir():
            continue

        app_name = app_path.name

        if app_name in EXCLUDED:
            skipped += 1
            continue

        try:
            success, msg = fix_app(app_path)
            if success:
                print(f"✅ {app_name}")
                fixed += 1
            else:
                print(f"⏭️  {app_name}: {msg}")
                skipped += 1
        except Exception as e:
            print(f"❌ {app_name}: {e}")
            errors += 1

    print(f"\n{'='*50}")
    print(f"✅ Corrigées: {fixed}")
    print(f"⏭️  Ignorées: {skipped}")
    print(f"❌ Erreurs: {errors}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
