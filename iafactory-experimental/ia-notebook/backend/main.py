"""
IA Notebook Pro - Alternative to NotebookLM (MORE POWERFUL)
Full-featured document intelligence API with:
- Audio Overview (podcast generation with multiple voices)
- Video Summary (AI-generated video scripts)
- Mind Map generation
- FAQ Generator
- Study Guide / Learning Cards / Flashcards
- Quiz Generator
- Infographic Generator
- Presentation Generator
- Timeline extraction
- Executive Briefing
- RAG Chat with citations
- Dashboard from data files
- AI Agents for specialized help
- Google Drive / OneDrive integration via MCP

YOUR DATA STAYS PRIVATE - Not sent to Google!
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum
import os
import uuid

from notebook_lm_pro_service import notebook_pro_service, AgentType
from dashboard_generator import dashboard_generator
from mcp_gdrive import mcp_drive

app = FastAPI(
    title="IA Notebook Pro API",
    description="Alternative to NotebookLM - More Powerful, Your Data Stays Private",
    version="3.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== MODELS ====================

class QuestionRequest(BaseModel):
    question: str
    file_ids: List[str] = []
    language: str = "fr"


class GenerateRequest(BaseModel):
    file_ids: List[str]
    language: str = "fr"
    options: Optional[Dict[str, Any]] = {}


class AudioOverviewRequest(BaseModel):
    file_ids: List[str]
    language: str = "fr"
    style: str = "deep_dive"  # deep_dive, brief, debate, lecture
    voices: Optional[Dict[str, str]] = {"host1": "alloy", "host2": "nova"}


class VideoSummaryRequest(BaseModel):
    file_ids: List[str]
    language: str = "fr"
    duration: int = 60  # seconds


class QuizRequest(BaseModel):
    file_ids: List[str]
    question_count: int = 10
    question_types: Optional[List[str]] = ["multiple_choice", "true_false", "short_answer"]
    language: str = "fr"


class FlashcardRequest(BaseModel):
    file_ids: List[str]
    count: int = 20
    language: str = "fr"


class PresentationRequest(BaseModel):
    file_ids: List[str]
    slide_count: int = 10
    language: str = "fr"


class InfographicRequest(BaseModel):
    file_ids: List[str]
    style: str = "modern"
    language: str = "fr"


class AgentRequest(BaseModel):
    file_ids: List[str]
    agent_type: str  # research, tutor, analyst, writer, summarizer, critic
    task: str
    language: str = "fr"


class URLSourceRequest(BaseModel):
    url: str
    source_type: str = "url"  # url, youtube


class DriveConnectRequest(BaseModel):
    provider: str  # gdrive, onedrive
    credentials: Dict[str, Any]


class DashboardRequest(BaseModel):
    file_id: str
    title: Optional[str] = None
    language: str = "fr"
    auto_config: bool = True


# ==================== HEALTH ====================

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "ia-notebook-pro",
        "version": "3.0.0",
        "features": [
            "audio_overview",
            "video_summary",
            "mind_map",
            "faq_generator",
            "study_guide",
            "flashcards",
            "quiz_generator",
            "infographic",
            "presentation",
            "timeline",
            "briefing",
            "rag_chat",
            "dashboard",
            "ai_agents",
            "gdrive_integration",
            "onedrive_integration"
        ],
        "agents": [
            "research",
            "tutor",
            "analyst",
            "writer",
            "summarizer",
            "critic"
        ],
        "supported_formats": [
            "pdf", "docx", "doc", "txt", "md",
            "csv", "xlsx", "xls", "json",
            "pptx", "mp3", "wav",
            "png", "jpg", "webp"
        ]
    }


# ==================== UPLOAD ====================

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document (PDF, DOCX, TXT, CSV, XLSX, JSON, MP3, WAV, images)"""
    try:
        result = await notebook_pro_service.upload_file(file)
        return {
            "success": True,
            "file_id": result["file_id"],
            "filename": result["filename"],
            "chunks": result["chunks_count"],
            "message": f"Document indexed with {result['chunks_count']} chunks"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/upload-url")
async def upload_url(request: URLSourceRequest):
    """Upload a URL or YouTube video as source"""
    try:
        result = await notebook_pro_service.process_url(
            url=request.url,
            source_type=request.source_type
        )
        return {
            "success": True,
            "file_id": result["file_id"],
            "title": result.get("title", request.url),
            "chunks": result["chunks_count"],
            "source_type": request.source_type
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== CLOUD DRIVE INTEGRATION ====================

@app.post("/drive/connect")
async def connect_drive(request: DriveConnectRequest):
    """Connect to Google Drive or OneDrive"""
    try:
        if request.provider == "gdrive":
            success = await mcp_drive.connect_google_drive(request.credentials)
        elif request.provider == "onedrive":
            success = await mcp_drive.connect_onedrive(request.credentials.get("access_token", ""))
        else:
            raise HTTPException(status_code=400, detail="Unsupported provider")

        return {"success": success, "provider": request.provider}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/drive/status")
async def drive_status():
    """Get connected drive sources status"""
    return mcp_drive.get_connected_sources()


@app.get("/drive/files")
async def list_drive_files(
    provider: str = "gdrive",
    folder_id: str = "root",
    query: Optional[str] = None
):
    """List files from connected drive"""
    try:
        if provider == "gdrive":
            files = await mcp_drive.list_gdrive_files(folder_id, query)
        elif provider == "onedrive":
            files = await mcp_drive.list_onedrive_files(folder_id)
        else:
            raise HTTPException(status_code=400, detail="Unsupported provider")

        return {
            "success": True,
            "files": [{"id": f.id, "name": f.name, "mime_type": f.mime_type, "size": f.size} for f in files]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/drive/import/{provider}/{file_id}")
async def import_from_drive(provider: str, file_id: str):
    """Import a file from Google Drive or OneDrive"""
    try:
        save_path = os.path.join("./uploads", f"drive_{file_id}")

        if provider == "gdrive":
            path = await mcp_drive.download_gdrive_file(file_id, save_path)
        elif provider == "onedrive":
            path = await mcp_drive.download_onedrive_file(file_id, save_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported provider")

        # Now process the file
        # This would need additional handling based on file type
        return {"success": True, "local_path": path, "message": "File imported successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== RAG CHAT ====================

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Ask a question about uploaded documents with citations"""
    try:
        result = await notebook_pro_service.ask_question(
            file_ids=request.file_ids,
            question=request.question,
            language=request.language
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== AUDIO OVERVIEW (PODCAST) ====================

@app.post("/generate/audio-overview")
async def generate_audio_overview(request: AudioOverviewRequest, background_tasks: BackgroundTasks):
    """Generate a podcast-style audio overview with 2 AI voices"""
    task_id = str(uuid.uuid4())

    background_tasks.add_task(
        notebook_pro_service.generate_audio_overview,
        task_id=task_id,
        file_ids=request.file_ids,
        language=request.language,
        style=request.style,
        voices=request.voices
    )

    return {
        "success": True,
        "task_id": task_id,
        "status": "processing",
        "message": "Audio overview generation started"
    }


@app.get("/generate/audio-overview/{task_id}/status")
async def get_audio_status(task_id: str):
    """Check audio generation status"""
    return notebook_pro_service.get_task_status(task_id)


@app.get("/generate/audio-overview/{task_id}/download")
async def download_audio(task_id: str):
    """Download generated audio file"""
    audio_path = notebook_pro_service.get_audio_path(task_id)
    if not audio_path or not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio not ready or not found")
    return FileResponse(audio_path, media_type="audio/mpeg", filename=f"audio-overview-{task_id}.mp3")


# ==================== VIDEO SUMMARY ====================

@app.post("/generate/video-summary")
async def generate_video_summary(request: VideoSummaryRequest, background_tasks: BackgroundTasks):
    """Generate AI video summary script"""
    task_id = str(uuid.uuid4())

    background_tasks.add_task(
        notebook_pro_service.generate_video_summary,
        task_id=task_id,
        file_ids=request.file_ids,
        language=request.language,
        duration=request.duration
    )

    return {
        "success": True,
        "task_id": task_id,
        "status": "processing",
        "message": "Video summary generation started"
    }


@app.get("/generate/video-summary/{task_id}/status")
async def get_video_status(task_id: str):
    """Check video generation status"""
    return notebook_pro_service.get_task_status(task_id)


# ==================== MIND MAP ====================

@app.post("/generate/mind-map")
async def generate_mind_map(request: GenerateRequest):
    """Generate an interactive mind map from documents"""
    try:
        result = await notebook_pro_service.generate_mind_map(
            file_ids=request.file_ids,
            language=request.language
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== FAQ GENERATOR ====================

@app.post("/generate/faq")
async def generate_faq(request: GenerateRequest):
    """Generate FAQ from documents"""
    try:
        result = await notebook_pro_service.generate_faq(
            file_ids=request.file_ids,
            count=request.options.get("count", 10),
            language=request.language
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== STUDY GUIDE ====================

@app.post("/generate/study-guide")
async def generate_study_guide(request: GenerateRequest):
    """Generate a structured study guide"""
    try:
        result = await notebook_pro_service.generate_study_guide(
            file_ids=request.file_ids,
            language=request.language
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== FLASHCARDS ====================

@app.post("/generate/flashcards")
async def generate_flashcards(request: FlashcardRequest):
    """Generate learning flashcards"""
    try:
        result = await notebook_pro_service.generate_flashcards(
            file_ids=request.file_ids,
            count=request.count,
            language=request.language
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== QUIZ GENERATOR ====================

@app.post("/generate/quiz")
async def generate_quiz(request: QuizRequest):
    """Generate interactive quiz"""
    try:
        result = await notebook_pro_service.generate_quiz(
            file_ids=request.file_ids,
            question_count=request.question_count,
            question_types=request.question_types,
            language=request.language
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== INFOGRAPHIC ====================

@app.post("/generate/infographic")
async def generate_infographic(request: InfographicRequest):
    """Generate infographic structure"""
    try:
        result = await notebook_pro_service.generate_infographic(
            file_ids=request.file_ids,
            style=request.style,
            language=request.language
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== PRESENTATION ====================

@app.post("/generate/presentation")
async def generate_presentation(request: PresentationRequest):
    """Generate presentation slides"""
    try:
        result = await notebook_pro_service.generate_presentation(
            file_ids=request.file_ids,
            slide_count=request.slide_count,
            language=request.language
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== TIMELINE ====================

@app.post("/generate/timeline")
async def generate_timeline(request: GenerateRequest):
    """Extract and generate a timeline from documents"""
    try:
        result = await notebook_pro_service.generate_timeline(
            file_ids=request.file_ids,
            language=request.language
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== BRIEFING DOCUMENT ====================

@app.post("/generate/briefing")
async def generate_briefing(request: GenerateRequest):
    """Generate an executive briefing document"""
    try:
        result = await notebook_pro_service.generate_briefing(
            file_ids=request.file_ids,
            language=request.language
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== DASHBOARD (FROM DATA) ====================

@app.post("/generate/dashboard")
async def generate_dashboard(request: DashboardRequest):
    """Generate dashboard from data file (CSV, XLS, JSON)"""
    try:
        doc = notebook_pro_service.documents.get(request.file_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")

        result = await dashboard_generator.generate_dashboard(
            file_path=doc["file_path"],
            title=request.title or doc["filename"],
            language=request.language,
            auto_config=request.auto_config
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== AI AGENTS ====================

@app.post("/agent/assist")
async def agent_assist(request: AgentRequest):
    """Get help from specialized AI agent"""
    try:
        agent_type = AgentType(request.agent_type)
        result = await notebook_pro_service.agent_assist(
            file_ids=request.file_ids,
            agent_type=agent_type,
            task=request.task,
            language=request.language
        )
        return {"success": True, **result}
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid agent type. Valid types: {[a.value for a in AgentType]}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/agents")
async def list_agents():
    """List available AI agents"""
    return {
        "agents": [
            {
                "type": "research",
                "name": "Research Agent",
                "description": "Deep research and analysis with citations"
            },
            {
                "type": "tutor",
                "name": "Tutor Agent",
                "description": "Helps you learn and understand content"
            },
            {
                "type": "analyst",
                "name": "Analyst Agent",
                "description": "Data analysis and pattern recognition"
            },
            {
                "type": "writer",
                "name": "Writer Agent",
                "description": "Creates content from your documents"
            },
            {
                "type": "summarizer",
                "name": "Summarizer Agent",
                "description": "Creates concise summaries at different levels"
            },
            {
                "type": "critic",
                "name": "Critic Agent",
                "description": "Critical analysis and constructive feedback"
            }
        ]
    }


# ==================== DOCUMENTS MANAGEMENT ====================

@app.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    return {"documents": notebook_pro_service.list_documents()}


@app.delete("/documents/{file_id}")
async def delete_document(file_id: str):
    """Delete a document"""
    try:
        notebook_pro_service.delete_document(file_id)
        return {"success": True, "message": f"Document {file_id} deleted"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# ==================== NOTEBOOKS ====================

@app.post("/notebooks")
async def create_notebook(name: str, description: str = ""):
    """Create a new notebook"""
    notebook_id = str(uuid.uuid4())
    notebook_pro_service.notebooks[notebook_id] = {
        "id": notebook_id,
        "name": name,
        "description": description,
        "files": [],
        "created_at": __import__('datetime').datetime.now().isoformat()
    }
    return {"success": True, "notebook_id": notebook_id, "name": name}


@app.get("/notebooks")
async def list_notebooks():
    """List all notebooks"""
    return {"notebooks": list(notebook_pro_service.notebooks.values())}


@app.get("/notebooks/{notebook_id}")
async def get_notebook(notebook_id: str):
    """Get notebook details"""
    notebook = notebook_pro_service.notebooks.get(notebook_id)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return notebook


@app.post("/notebooks/{notebook_id}/files/{file_id}")
async def add_file_to_notebook(notebook_id: str, file_id: str):
    """Add a file to a notebook"""
    notebook = notebook_pro_service.notebooks.get(notebook_id)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")

    if file_id not in notebook_pro_service.documents:
        raise HTTPException(status_code=404, detail="Document not found")

    if file_id not in notebook["files"]:
        notebook["files"].append(file_id)

    return {"success": True, "message": f"File added to notebook"}


@app.delete("/notebooks/{notebook_id}")
async def delete_notebook(notebook_id: str):
    """Delete a notebook and all its sources"""
    if notebook_id in notebook_pro_service.notebooks:
        del notebook_pro_service.notebooks[notebook_id]
        return {"success": True, "message": f"Notebook {notebook_id} deleted"}
    raise HTTPException(status_code=404, detail="Notebook not found")


# ==================== SUPPORTED FORMATS ====================

@app.get("/formats")
async def supported_formats():
    """List all supported file formats"""
    return {
        "documents": ["pdf", "docx", "doc", "txt", "md", "rtf"],
        "spreadsheets": ["csv", "xlsx", "xls", "ods", "json"],
        "presentations": ["pptx", "ppt"],
        "audio": ["mp3", "wav", "webm", "ogg"],
        "images": ["png", "jpg", "jpeg", "webp", "gif"],
        "data": ["json", "xml", "parquet"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8300)
