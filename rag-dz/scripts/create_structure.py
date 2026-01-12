"""
IA FACTORY - Création Structure Projet Complète
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

STRUCTURE = {
    "infrastructure": ["scripts", "docker", "kubernetes", "terraform"],
    "templates": ["documents", "presentations", "dashboards", "emails"],
    "outputs": ["propositions", "presentations", "dashboards", "reports", "invoices"],
    "api": ["routers", "models", "services", "middleware"],
    "core": ["rag", "agents", "llm", "embeddings"],
    "workflows": ["sales", "delivery", "support", "finance"],
    "social_media": ["content", "scheduler", "analytics"],
    "digital_twin": ["personality", "learning", "generation"],
    "clients": [],
    "config": [],
    "tests": [],
    "docs": []
}

def create_structure():
    print("🏭 Création structure IA Factory...")
    
    for folder, subfolders in STRUCTURE.items():
        folder_path = BASE_DIR / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {folder}/")
        
        for sub in subfolders:
            sub_path = folder_path / sub
            sub_path.mkdir(exist_ok=True)
            print(f"     └── {sub}/")
        
        if folder not in ["outputs", "docs", "config", "clients"]:
            init_file = folder_path / "__init__.py"
            if not init_file.exists():
                init_file.write_text("# IA Factory\n")
    
    print("\n✅ Structure créée!")

if __name__ == "__main__":
    create_structure()
