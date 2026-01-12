"""
Voice Agent API - Main Application
Faster-Whisper transcription with LLM cleaning for professionals
"""

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import our voice-agent router
try:
    from .router import router as voice_router
except ImportError:
    from router import router as voice_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Voice Agent API",
    description="Professional voice transcription with Faster-Whisper + LLM cleaning",
    version="1.0.0",
    docs_url="/api/voice-agent/docs",
    redoc_url="/api/voice-agent/redoc",
)

# CORS - Allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include voice-agent router
app.include_router(voice_router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "service": "voice-agent-api",
        "version": "1.0.0",
        "status": "running",
        "engine": "faster-whisper",
        "model": "large-v3",
        "docs": "/api/voice-agent/docs"
    }

# Health check at root level too
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "voice-agent"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8201"))
    logger.info(f"🎤 Starting Voice Agent API on port {port}")
    logger.info(f"📡 Docs available at http://localhost:{port}/api/voice-agent/docs")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
