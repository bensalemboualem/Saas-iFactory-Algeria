from fastapi import FastAPI
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
