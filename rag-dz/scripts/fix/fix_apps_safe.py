#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# CSS de la landing page (RÉFÉRENCE)
LANDING_CSS = """
        :root {
            --bg: #020617;
            --bg-alt: #020617;
            --card: #020617;
            --bg-card: #020617;
            --bg-secondary: #0f172a;
            --bg-dark: #020617;
            --border: rgba(255, 255, 255, 0.12);
            --border-primary: rgba(255, 255, 255, 0.12);
            --primary: #00a651;
            --primary-dark: #008c45;
            --accent: #00a651;
            --accent-primary: #00a651;
            --text: #f8fafc;
            --text-primary: #f8fafc;
            --text-secondary: rgba(248, 250, 252, 0.75);
            --muted: rgba(248, 250, 252, 0.75);
            --shadow: 0 20px 60px rgba(0, 0, 0, 0.55);
        }

        [data-theme="light"] {
            --bg: #f7f5f0;
            --bg-alt: #f7f5f0;
            --card: #f7f5f0;
            --bg-card: #ffffff;
            --bg-secondary: #f7f5f0;
            --bg-dark: #f7f5f0;
            --border: rgba(0, 0, 0, 0.08);
            --border-primary: rgba(0, 0, 0, 0.08);
            --primary: #00a651;
            --primary-dark: #008c45;
            --accent: #00a651;
            --accent-primary: #00a651;
            --text: #0f172a;
            --text-primary: #0f172a;
            --text-secondary: rgba(15, 23, 42, 0.7);
            --muted: rgba(15, 23, 42, 0.7);
            --shadow: 0 20px 60px rgba(15, 23, 42, 0.25);
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

def fix_app_safe(app_path):
    """Corrige une app de manière sûre ligne par ligne"""
    index_file = app_path / "index.html"

    if not index_file.exists():
        return False, "No index.html"

    # Backup
    backup_file = str(index_file) + f".backup-safe-fix-{os.getpid()}"
    with open(index_file, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    with open(backup_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

    # Traitement ligne par ligne
    output_lines = []
    skip_until_closing_div = 0
    skip_function = False
    in_head = False
    head_closed = False
    css_added = False
    has_auto_init = False
    has_unified_js = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # Détecter <html> et ajouter data-iaf-auto-init si manquant
        if "<html" in line and "data-iaf-auto-init" not in line:
            line = line.replace("<html", "<html data-iaf-auto-init")
            has_auto_init = True
        elif "data-iaf-auto-init" in line:
            has_auto_init = True

        # Suivre position dans le document
        if "<head" in line:
            in_head = True
        if "</head>" in line:
            in_head = False
            head_closed = True
            # Ajouter CSS juste avant </head> si pas encore ajouté
            if not css_added:
                output_lines.append("  <style>\n")
                output_lines.append(LANDING_CSS)
                output_lines.append("  </style>\n")
                css_added = True

        # Détecter ancien chatbot (commentaire ou div)
        if "<!-- IAF Chatbot" in line or "<!-- HELP CHATBOT" in line:
            skip_until_closing_div = 2  # Attendre 2 </div>
            i += 1
            continue

        if '<div class="iaf-chatbot"' in line or '<div class="help-bubble"' in line:
            skip_until_closing_div = 2
            i += 1
            continue

        # Skip les lignes dans l'ancien chatbot
        if skip_until_closing_div > 0:
            if "</div>" in line:
                skip_until_closing_div -= 1
            i += 1
            continue

        # Détecter et skip fonctions obsolètes
        if "function sendHelpMessage" in line or "function toggleTheme" in line:
            skip_function = True
            i += 1
            continue

        if skip_function:
            if "}" in line and line.strip() == "}":
                skip_function = False
            i += 1
            continue

        # Détecter système unifié existant
        if "iafactory-unified.js" in line:
            has_unified_js = True

        # Skip </body> et </html> pour les ajouter à la fin
        if "</body>" in line or "</html>" in line:
            i += 1
            continue

        # Ligne OK, on garde
        output_lines.append(line)
        i += 1

    # Ajouter système unifié si manquant
    if not has_unified_js:
        output_lines.append("\n")
        output_lines.append(UNIFIED_SYSTEM)
        output_lines.append("\n")

    # Fermer proprement
    output_lines.append("</body>\n")
    output_lines.append("</html>\n")

    # Écrire le fichier corrigé
    with open(index_file, "w", encoding="utf-8") as f:
        f.writelines(output_lines)

    return True, "Fixed"

# Apps à exclure
EXCLUDED = ["shared", "landing", "school-erp", "docs"]

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
            success, msg = fix_app_safe(app_path)
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
