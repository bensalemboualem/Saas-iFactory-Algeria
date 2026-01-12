"""
IA Factory Algeria - Browser Automation Service
Stack: Browser-Use + Ollama (Qwen2.5) + FastAPI
Coût: $0/mois (100% local)
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
import asyncio
import os
import json
from enum import Enum

from agents.sonelgaz import SonelgazAgent
from agents.cnas import CNASAgent
from config import settings

app = FastAPI(
    title="IA Factory - Browser Automation",
    description="Automatisation navigateur pour services algériens (Sonelgaz, CNAS)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============== MODELS ==============

class ServiceType(str, Enum):
    SONELGAZ = "sonelgaz"
    CNAS = "cnas"

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class SonelgazRequest(BaseModel):
    reference_client: str = Field(..., description="Numéro de référence client Sonelgaz")
    action: str = Field(default="get_factures", description="Action: get_factures, get_consommation")

class CNASRequest(BaseModel):
    numero_securite_sociale: str = Field(..., description="Numéro de sécurité sociale")
    action: str = Field(default="get_attestation", description="Action: get_attestation, get_historique")

class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    service: ServiceType
    created_at: datetime
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# ============== STORAGE ==============

tasks_db: Dict[str, TaskResponse] = {}

# ============== AGENTS ==============

sonelgaz_agent = SonelgazAgent()
cnas_agent = CNASAgent()

# ============== ROUTES ==============

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "browser-automation",
        "ollama_url": settings.OLLAMA_BASE_URL,
        "model": settings.OLLAMA_MODEL
    }

@app.get("/services")
async def list_services():
    """Liste des services disponibles"""
    return {
        "services": [
            {
                "id": "sonelgaz",
                "name": "Sonelgaz",
                "description": "Consultation factures électricité/gaz",
                "actions": ["get_factures", "get_consommation"],
                "required_fields": ["reference_client"]
            },
            {
                "id": "cnas",
                "name": "CNAS",
                "description": "Sécurité sociale - attestations",
                "actions": ["get_attestation", "get_historique"],
                "required_fields": ["numero_securite_sociale"]
            }
        ]
    }

@app.post("/sonelgaz", response_model=TaskResponse)
async def sonelgaz_task(request: SonelgazRequest, background_tasks: BackgroundTasks):
    """Lancer une tâche Sonelgaz"""
    task_id = f"sonelgaz_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    task = TaskResponse(
        task_id=task_id,
        status=TaskStatus.PENDING,
        service=ServiceType.SONELGAZ,
        created_at=datetime.now()
    )
    tasks_db[task_id] = task
    
    background_tasks.add_task(
        run_sonelgaz_task,
        task_id,
        request.reference_client,
        request.action
    )
    
    return task

@app.post("/cnas", response_model=TaskResponse)
async def cnas_task(request: CNASRequest, background_tasks: BackgroundTasks):
    """Lancer une tâche CNAS"""
    task_id = f"cnas_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    task = TaskResponse(
        task_id=task_id,
        status=TaskStatus.PENDING,
        service=ServiceType.CNAS,
        created_at=datetime.now()
    )
    tasks_db[task_id] = task
    
    background_tasks.add_task(
        run_cnas_task,
        task_id,
        request.numero_securite_sociale,
        request.action
    )
    
    return task

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Récupérer le statut d'une tâche"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return tasks_db[task_id]

@app.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(limit: int = 10):
    """Liste des dernières tâches"""
    sorted_tasks = sorted(
        tasks_db.values(),
        key=lambda x: x.created_at,
        reverse=True
    )
    return sorted_tasks[:limit]

# ============== BACKGROUND TASKS ==============

async def run_sonelgaz_task(task_id: str, reference: str, action: str):
    """Exécuter tâche Sonelgaz en arrière-plan"""
    tasks_db[task_id].status = TaskStatus.RUNNING
    
    try:
        if action == "get_factures":
            result = await sonelgaz_agent.get_factures(reference)
        elif action == "get_consommation":
            result = await sonelgaz_agent.get_consommation(reference)
        else:
            raise ValueError(f"Action inconnue: {action}")
        
        tasks_db[task_id].status = TaskStatus.COMPLETED
        tasks_db[task_id].result = result
        
    except Exception as e:
        tasks_db[task_id].status = TaskStatus.FAILED
        tasks_db[task_id].error = str(e)

async def run_cnas_task(task_id: str, nss: str, action: str):
    """Exécuter tâche CNAS en arrière-plan"""
    tasks_db[task_id].status = TaskStatus.RUNNING
    
    try:
        if action == "get_attestation":
            result = await cnas_agent.get_attestation(nss)
        elif action == "get_historique":
            result = await cnas_agent.get_historique(nss)
        else:
            raise ValueError(f"Action inconnue: {action}")
        
        tasks_db[task_id].status = TaskStatus.COMPLETED
        tasks_db[task_id].result = result
        
    except Exception as e:
        tasks_db[task_id].status = TaskStatus.FAILED
        tasks_db[task_id].error = str(e)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8100)
