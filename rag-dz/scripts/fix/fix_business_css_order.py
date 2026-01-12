#!/usr/bin/env python3
import sys

file_path = "/opt/iafactory-rag-dz/apps/business-dz/index.html"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Trouver <style> et :root
style_line = None
root_start = None
root_end = None

for i, line in enumerate(lines):
    if "<style>" in line and style_line is None:
        style_line = i
    if ":root {" in line and root_start is None:
        root_start = i
    if root_start is not None and root_end is None:
        if "[data-theme=\"light\"]" in line:
            # Trouver la fin de ce bloc
            for j in range(i, min(i+50, len(lines))):
                if lines[j].strip() == "}":
                    root_end = j
                    break

if style_line and root_start and root_end:
    print(f"✅ Trouvé:")
    print(f"   <style> à ligne {style_line+1}")
    print(f"   :root à ligne {root_start+1}")
    print(f"   Fin bloc à ligne {root_end+1}")

    # Extraire le bloc :root
    root_block = lines[root_start:root_end+1]

    # Supprimer le bloc de sa position actuelle
    del lines[root_start:root_end+1]

    # Insérer juste après <style>
    for i, block_line in enumerate(root_block):
        lines.insert(style_line + 1 + i, block_line)

    # Sauvegarder
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"✅ Bloc :root déplacé juste après <style>")
    print(f"   Nouveau fichier: {len(lines)} lignes")
else:
    print(f"❌ Erreur:")
    print(f"   style_line: {style_line}")
    print(f"   root_start: {root_start}")
    print(f"   root_end: {root_end}")
