"""
Dzir IA Video - FastAPI Server
REST API for video generation and publishing
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import logging
from pathlib import Path
import tempfile

from .pipeline import VideoPipeline
from .api_generators import router as generators_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Dzir IA Video API",
    description="Automated YouTube Shorts generation and publishing with AI + 43 AI Generators",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    root_path="/dzirvideo",  # Important pour Nginx proxy
    swagger_ui_parameters={
        "url": "/dzirvideo/openapi.json"  # Force le bon chemin pour Swagger UI
    }
)

# Include generators router
app.include_router(generators_router)

# Initialize pipeline
pipeline = VideoPipeline()


class VideoRequest(BaseModel):
    """Video generation request"""
    script_text: str
    title: str
    description: str = ""
    tags: list[str] = []
    publish: bool = False
    privacy_status: str = "public"


@app.get("/")
async def root():
    """API root"""
    return {
        "service": "Dzir IA Video",
        "version": "2.1.0",
        "status": "running",
        "features": {
            "ai_generators": 31,
            "categories": 6,
            "free_generators": 13,
            "premium_generators": 6
        },
        "endpoints": {
            "health": "/health",
            "generate": "POST /generate",
            "generate_file": "POST /generate/file",
            "status": "GET /status",
            "generators": {
                "list": "GET /api/v1/generators/list",
                "info": "GET /api/v1/generators/info/{name}",
                "summary": "GET /api/v1/generators/summary",
                "generate": "POST /api/v1/generators/generate",
                "status": "GET /api/v1/generators/status/{name}/{task_id}",
                "compare": "POST /api/v1/generators/compare",
                "recommend": "POST /api/v1/generators/recommend"
            }
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "dzir-ia-video"}


@app.post("/generate")
async def generate_video(request: VideoRequest):
    """
    Generate video from script text

    Args:
        request: VideoRequest with script, title, etc.

    Returns:
        JSON with video details and paths
    """
    try:
        result = pipeline.run_full_pipeline(
            script_text=request.script_text,
            title=request.title,
            description=request.description,
            tags=request.tags,
            publish=request.publish,
            privacy_status=request.privacy_status
        )

        return JSONResponse(content=result)

    except Exception as e:
        logging.error(f"Error generating video: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/file")
async def generate_from_file(
    script_file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(""),
    tags: str = Form(""),  # Comma-separated
    publish: bool = Form(False),
    privacy_status: str = Form("public")
):
    """
    Generate video from uploaded script file (.md or .txt)

    Args:
        script_file: Script file (markdown or text)
        title: Video title
        description: Video description
        tags: Comma-separated tags
        publish: Whether to publish to YouTube
        privacy_status: YouTube privacy status

    Returns:
        JSON with video details
    """
    try:
        # Read script content
        content = await script_file.read()
        script_text = content.decode('utf-8')

        # Parse tags
        tags_list = [t.strip() for t in tags.split(',') if t.strip()]

        # Generate video
        result = pipeline.run_full_pipeline(
            script_text=script_text,
            title=title,
            description=description,
            tags=tags_list,
            publish=publish,
            privacy_status=privacy_status
        )

        return JSONResponse(content=result)

    except Exception as e:
        logging.error(f"Error generating video from file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{filename}")
async def download_video(filename: str):
    """
    Download generated video

    Args:
        filename: Video filename

    Returns:
        Video file
    """
    video_path = Path("./output/videos") / filename

    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")

    return FileResponse(
        path=video_path,
        media_type="video/mp4",
        filename=filename
    )


@app.get("/status")
async def get_status():
    """Get pipeline status and configuration"""
    return {
        "pipeline": "ready",
        "config": {
            "tts_model": pipeline.config.get('tts_model'),
            "subtitle_style": pipeline.config.get('subtitle_style'),
            "video_resolution": f"{pipeline.config.get('video_width')}x{pipeline.config.get('video_height')}",
            "fps": pipeline.config.get('video_fps')
        },
        "youtube_configured": bool(
            pipeline.config.get('youtube_client_id') and
            pipeline.config.get('youtube_refresh_token')
        )
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8200)
