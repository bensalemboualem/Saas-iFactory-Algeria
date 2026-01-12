"""
IA FACTORY - Script Principal de Lancement
Point d'entrée pour démarrer tous les services
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

BASE = Path(__file__).parent

def run_api():
    """Lance l'API FastAPI"""
    print("🚀 Démarrage API IA Factory...")
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "api.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ], cwd=BASE)

def gen_docs():
    """Génère tous les documents templates"""
    print("📄 Génération documents...")
    
    sys.path.insert(0, str(BASE))
    
    from templates.documents.proposition_commerciale import PropositionGenerator
    from templates.presentations.teaching_assistant_deck import TeachingAssistantDeck
    from templates.dashboards.kpi_dashboard import KPIDashboard
    
    gen = PropositionGenerator()
    f1 = gen.generate({"name": "Demo CH", "company": "Swiss Corp"}, ["RAG System"], "CH")
    f2 = gen.generate({"name": "Demo DZ", "company": "Algerie Telecom"}, ["RAG System"], "DZ")
    print(f"  ✅ Proposition CH: {f1}")
    print(f"  ✅ Proposition DZ: {f2}")
    
    f3 = TeachingAssistantDeck().generate("CH")
    f4 = TeachingAssistantDeck().generate("DZ")
    print(f"  ✅ Deck CH: {f3}")
    print(f"  ✅ Deck DZ: {f4}")
    
    f5 = KPIDashboard().generate()
    print(f"  ✅ Dashboard: {f5}")

def create_struct():
    """Crée la structure de dossiers"""
    exec(open(BASE / "create_structure.py").read())

def main():
    print("🏭 IA FACTORY")
    print("📧 CH: contact@iafactory.ch")
    print("📧 DZ: contact@iafactoryalgeria.com\n")
    
    parser = argparse.ArgumentParser(description="IA Factory CLI")
    parser.add_argument("command", choices=[
        "api", "docs", "structure", "all"
    ], nargs="?", default="all")
    
    args = parser.parse_args()
    
    {"structure": create_struct, "docs": gen_docs, "api": run_api, "all": lambda: (create_struct(), gen_docs(), print("\n✅ Prêt! Lance: python run.py api"))}[args.command]()

if __name__ == "__main__":
    import subprocess, sys, os, webbrowser, time, threading
    from pathlib import Path

    BASE = Path(__file__).parent
    os.chdir(BASE)

    print("=" * 50)
    print("🏭 IA FACTORY - LANCEMENT")
    print("📧 CH: contact@iafactory.ch")
    print("📧 DZ: contact@iafactoryalgeria.com")
    print("=" * 50)

    # 1. Install
    print("\n📦 Installation packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "fastapi", "uvicorn"], 
                   capture_output=True)
    print("✅ OK")

    # 2. Create folders
    (BASE / "api").mkdir(exist_ok=True)

    # 3. Create API
    (BASE / "api" / "main.py").write_text('''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(title="IA Factory")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def root():
    return {"name": "IA Factory", "CH": "contact@iafactory.ch", "DZ": "contact@iafactoryalgeria.com", "time": datetime.now().isoformat()}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/kpis")
def kpis():
    return {"mrr": 8500, "clients": 12, "margin": "92%"}
''')
    print("✅ API créée")

    # 4. Open browser after delay
    def open_browser():
        time.sleep(3)
        webbrowser.open("http://127.0.0.1:8000")
    threading.Thread(target=open_browser, daemon=True).start()

    # 5. Run server
    print("\n🚀 http://127.0.0.1:8000")
    print("📚 http://127.0.0.1:8000/docs")
    print("\nCtrl+C pour arrêter\n")
    
    subprocess.run([sys.executable, "-m", "uvicorn", "api.main:app", "--host", "127.0.0.1", "--port", "8000"])
