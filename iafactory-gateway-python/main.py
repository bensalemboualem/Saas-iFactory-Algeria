# -*- coding: utf-8 -*-
"""
IAFactory Gateway - Python/FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="IAFactory Gateway",
    description="Gateway IA multi-providers pour Algerie",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.llm import router as llm_router
from api.credits import router as credits_router
from api.webhook import router as webhook_router
from core.database import db

@app.on_event("startup")
async def startup():
    await db.connect()

app.include_router(llm_router)
app.include_router(credits_router)
app.include_router(webhook_router)

@app.get("/")
async def root():
    return {"message":"IAFactory Gateway","version":"2.0.0","status":"healthy"}

@app.get("/health")
async def health():
    return {"status":"ok","port":os.getenv("API_PORT","3001")}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("API_PORT","3001")))
