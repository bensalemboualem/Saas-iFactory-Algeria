"""
Dzir IA Video PRO - FastAPI Server with AI Assistant
REST API for professional video generation with AI script optimization
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from pydantic import BaseModel
import logging
from pathlib import Path
import tempfile
import os

from .pipeline import VideoPipeline
from .ai_assistant.script_optimizer import ScriptOptimizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Dzir IA Video PRO API",
    description="Professional YouTube Shorts generation with AI script optimization and multi-AI generators",
    version="2.1.0",
    docs_url=None,  # Désactiver les docs par défaut
    redoc_url=None,  # Désactiver redoc par défaut
    openapi_url="/openapi.json",
    root_path="/dzirvideo"  # Important pour Nginx proxy
)

# Configure CORS pour permettre à ReDoc/Swagger de charger openapi.json
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, limiter aux domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directories
app.mount("/output", StaticFiles(directory="output"), name="output")

# Initialize services
pipeline = VideoPipeline()
ai_optimizer = ScriptOptimizer(api_key=os.getenv("CLAUDE_API_KEY"))


# ===== Models =====

class VideoRequest(BaseModel):
    """Video generation request"""
    script_text: str
    title: str
    description: str = ""
    tags: list[str] = []
    publish: bool = False
    privacy_status: str = "public"


class ScriptOptimizationRequest(BaseModel):
    """AI script optimization request"""
    raw_idea: str
    niche: str = "general"  # tech, business, education, motivation, etc.
    tone: str = "energetic"  # energetic, calm, professional, funny
    target_duration: int = 45  # seconds


class ScriptAnalysisRequest(BaseModel):
    """Script analysis request"""
    script: str


# ===== Endpoints =====

@app.get("/")
async def root():
    """Serve PRO web interface"""
    return FileResponse("public/index-pro.html")


@app.get("/api")
async def api_info():
    """API information (JSON)"""
    return {
        "service": "Dzir IA Video PRO",
        "version": "2.1.0",
        "status": "running",
        "features": {
            "ai_script_optimization": True,
            "script_analysis": True,
            "professional_editing": True,
            "youtube_upload": True
        },
        "endpoints": {
            "health": "/health",
            "generate": "POST /generate",
            "ai_optimize": "POST /ai/optimize-script",
            "ai_analyze": "POST /ai/analyze-script",
            "status": "/status"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "dzir-ia-video-pro"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Custom Swagger UI with correct openapi.json path"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
        <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
        <title>{app.title} - Swagger UI</title>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
            const ui = SwaggerUIBundle({{
                url: '/dzirvideo/openapi.json',
                dom_id: '#swagger-ui',
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout",
                deepLinking: true,
                showExtensions: true,
                showCommonExtensions: true
            }})
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/redoc", include_in_schema=False)
async def custom_redoc_html():
    """Custom ReDoc with correct openapi.json path"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{app.title} - ReDoc</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
        <style>
            body {{
                margin: 0;
                padding: 0;
            }}
        </style>
    </head>
    <body>
        <redoc spec-url='/dzirvideo/openapi.json'></redoc>
        <script src="https://cdn.jsdelivr.net/npm/redoc@2.1.3/bundles/redoc.standalone.js"></script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# ===== AI Endpoints =====

@app.post("/ai/optimize-script")
async def optimize_script(request: ScriptOptimizationRequest):
    """
    AI-powered script optimization

    Transforms raw idea into viral YouTube Short script with:
    - Attention-grabbing hook (first 3 seconds)
    - Engaging main content
    - Strong call-to-action
    - Optimized title, description, tags
    - Viral score prediction
    """
    try:
        result = ai_optimizer.optimize_script(
            raw_idea=request.raw_idea,
            niche=request.niche,
            tone=request.tone,
            target_duration=request.target_duration
        )

        return {
            "success": True,
            "hook": result.hook,
            "main_content": result.main_content,
            "cta": result.cta,
            "full_script": result.full_script,
            "title": result.title,
            "description": result.description,
            "tags": result.tags,
            "viral_score": result.viral_score,
            "improvements": result.improvements
        }

    except Exception as e:
        logging.error(f"AI optimization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ai/analyze-script")
async def analyze_script(request: ScriptAnalysisRequest):
    """
    Analyze existing script and provide optimization suggestions

    Returns:
    - Word count, character count, estimated duration
    - Hook analysis, CTA detection
    - Viral score prediction
    - Improvement suggestions
    """
    try:
        analysis = ai_optimizer.analyze_script(request.script)

        return {
            "success": True,
            **analysis
        }

    except Exception as e:
        logging.error(f"Script analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Video Generation Endpoints =====

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
        "ai_assistant": "enabled" if ai_optimizer.api_key else "disabled (fallback mode)",
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
