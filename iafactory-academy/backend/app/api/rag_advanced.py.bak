"""
Advanced RAG API Endpoints
Quiz, Budget, Comparison, Timeline, Demo Mode for BBC School
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.services.rag.advanced_features import (
    LanguageDetector,
    QuizGenerator,
    ModuleComparator,
    BudgetCalculator,
    TimelineGenerator,
    AdaptiveAssistant,
    MinisterDemoMode,
    BBC_PROGRAM_DATA,
    get_arabic_response,
    Language
)


router = APIRouter(prefix="/rag/advanced", tags=["RAG Advanced"])


# ============================================
# Request/Response Models
# ============================================

class QuizRequest(BaseModel):
    """Request for quiz generation"""
    module: str = Field(..., description="Module ID (e.g., L1, L2, C1)")
    num_questions: int = Field(default=5, ge=1, le=10)
    difficulty: str = Field(default="all", pattern="^(all|Débutant|Intermédiaire|Avancé)$")


class QuizResponse(BaseModel):
    """Quiz response"""
    module: str
    questions: List[dict]
    total_questions: int


class CompareRequest(BaseModel):
    """Request for module comparison"""
    modules: List[str] = Field(..., min_length=2, max_length=5)


class CompareResponse(BaseModel):
    """Comparison response"""
    modules: List[dict]
    comparison_table: dict
    markdown: str


class BudgetRequest(BaseModel):
    """Request for budget calculation"""
    num_schools: int = Field(default=50, ge=1, le=500)
    num_teachers: int = Field(default=200, ge=1, le=2000)
    num_students: int = Field(default=5000, ge=1, le=100000)


class BudgetResponse(BaseModel):
    """Budget calculation response"""
    parameters: dict
    costs_per_unit: dict
    subtotals: dict
    total: dict
    breakdown: dict
    markdown: str


class TimelineResponse(BaseModel):
    """Timeline response"""
    events: List[dict]
    mermaid: str
    json_data: dict


class AdaptiveRequest(BaseModel):
    """Request for adaptive response"""
    question: str = Field(..., min_length=3)
    level: str = Field(default="college", pattern="^(primaire|college|lycee|enseignants)$")


class DemoButton(BaseModel):
    """Demo button"""
    label: str
    action: str


class DemoResponse(BaseModel):
    """Demo mode response"""
    content: str
    buttons: List[DemoButton]


class MultilingualRequest(BaseModel):
    """Multilingual chat request"""
    question: str = Field(..., min_length=3)


class MultilingualResponse(BaseModel):
    """Multilingual response"""
    answer: str
    detected_language: str
    language_name: str


class ProgramStatsResponse(BaseModel):
    """Program statistics"""
    program_name: str
    launch_date: str
    pilot_duration_months: int
    total_schools: int
    total_teachers: int
    total_students_target: int
    budget_total_da: int
    budget_total_usd: float
    levels: dict
    kpis: dict


# ============================================
# Endpoints
# ============================================

@router.post("/quiz", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    """
    Generate a dynamic quiz for a module

    Supports modules: L1-L8, C1-C6, P1-P4
    Returns QCM questions with explanations
    """
    try:
        questions = QuizGenerator.generate_quiz(
            module=request.module,
            num_questions=request.num_questions,
            difficulty=request.difficulty
        )

        return QuizResponse(
            module=request.module,
            questions=QuizGenerator.to_dict(questions),
            total_questions=len(questions)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare", response_model=CompareResponse)
async def compare_modules(request: CompareRequest):
    """
    Compare two or more modules

    Returns detailed comparison table with:
    - Duration, credits, difficulty
    - Prerequisites and projects
    """
    try:
        comparison = ModuleComparator.compare(request.modules)
        markdown = ModuleComparator.to_markdown_table(comparison)

        return CompareResponse(
            modules=comparison["modules"],
            comparison_table=comparison.get("comparison_table", {}),
            markdown=markdown
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/budget", response_model=BudgetResponse)
async def calculate_budget(request: BudgetRequest):
    """
    Calculate deployment budget

    Based on number of schools, teachers, and students.
    Returns detailed breakdown in DA and USD.
    """
    try:
        budget = BudgetCalculator.calculate(
            num_schools=request.num_schools,
            num_teachers=request.num_teachers,
            num_students=request.num_students
        )
        markdown = BudgetCalculator.to_markdown(budget)

        return BudgetResponse(
            parameters=budget["parameters"],
            costs_per_unit=budget["costs_per_unit"],
            subtotals=budget["subtotals"],
            total=budget["total"],
            breakdown=budget["breakdown"],
            markdown=markdown
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/timeline", response_model=TimelineResponse)
async def get_timeline():
    """
    Get deployment timeline

    Returns events, Mermaid chart, and JSON for visualization.
    """
    try:
        events = TimelineGenerator.get_timeline()
        mermaid = TimelineGenerator.to_mermaid()
        json_data = TimelineGenerator.to_json()

        return TimelineResponse(
            events=events,
            mermaid=mermaid,
            json_data=json_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/adaptive")
async def adaptive_chat(request: AdaptiveRequest):
    """
    Get response adapted to education level

    Adjusts vocabulary and tone for:
    - primaire: Simple, playful with emojis
    - college: Educational and engaging
    - lycee: Professional but accessible
    - enseignants: Technical and precise
    """
    try:
        system_prompt = AdaptiveAssistant.get_system_prompt(request.level)

        return {
            "level": request.level,
            "question": request.question,
            "system_prompt": system_prompt,
            "note": "Use this system prompt with the /rag/chat endpoint"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/demo", response_model=DemoResponse)
async def get_demo_mode(action: str = Query(default="présentation")):
    """
    Minister Demo Mode

    Pre-programmed perfect responses for presentation.
    Available actions: présentation, budget, timeline, kpis, modules_lycee, formation_enseignants
    """
    try:
        content = MinisterDemoMode.get_response(action)
        buttons = [DemoButton(**b) for b in MinisterDemoMode.get_buttons()]

        return DemoResponse(
            content=content,
            buttons=buttons
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/demo/buttons")
async def get_demo_buttons():
    """Get available demo buttons"""
    return MinisterDemoMode.get_buttons()


@router.post("/multilingual", response_model=MultilingualResponse)
async def multilingual_chat(request: MultilingualRequest):
    """
    Multilingual chat with automatic language detection

    Supports: French, Arabic, English
    Responds in the detected language.
    """
    try:
        # Detect language
        detected = LanguageDetector.detect(request.question)

        language_names = {
            Language.FRENCH: "Français",
            Language.ARABIC: "العربية",
            Language.ENGLISH: "English"
        }

        # For Arabic, check predefined responses
        if detected == Language.ARABIC:
            arabic_response = get_arabic_response(request.question)
            if arabic_response:
                return MultilingualResponse(
                    answer=arabic_response,
                    detected_language=detected.value,
                    language_name=language_names[detected]
                )

        # Default response indicating to use main chat
        return MultilingualResponse(
            answer=f"Langue détectée: {language_names[detected]}. Utilisez /rag/chat avec language='{detected.value}' pour une réponse complète.",
            detected_language=detected.value,
            language_name=language_names[detected]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=ProgramStatsResponse)
async def get_program_stats():
    """
    Get complete program statistics

    Returns all KPIs, levels, budget, and timeline info.
    """
    try:
        return ProgramStatsResponse(
            program_name=BBC_PROGRAM_DATA["program_name"],
            launch_date=BBC_PROGRAM_DATA["launch_date"],
            pilot_duration_months=BBC_PROGRAM_DATA["pilot_duration_months"],
            total_schools=BBC_PROGRAM_DATA["total_schools"],
            total_teachers=BBC_PROGRAM_DATA["total_teachers"],
            total_students_target=BBC_PROGRAM_DATA["total_students_target"],
            budget_total_da=BBC_PROGRAM_DATA["budget"]["total_da"],
            budget_total_usd=BBC_PROGRAM_DATA["budget"]["total_usd"],
            levels=BBC_PROGRAM_DATA["levels"],
            kpis=BBC_PROGRAM_DATA["kpis"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/modules")
async def list_modules(level: Optional[str] = None):
    """
    List all modules with details

    Optional filter by level: primaire, college, lycee
    """
    try:
        modules = BBC_PROGRAM_DATA["modules"]

        if level:
            level_data = BBC_PROGRAM_DATA["levels"].get(level)
            if level_data:
                module_ids = level_data.get("modules_list", [])
                modules = {k: v for k, v in modules.items() if k in module_ids}

        return {
            "count": len(modules),
            "modules": modules
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/modules/{module_id}")
async def get_module(module_id: str):
    """Get details for a specific module"""
    try:
        module = BBC_PROGRAM_DATA["modules"].get(module_id.upper())
        if not module:
            raise HTTPException(status_code=404, detail=f"Module {module_id} not found")

        return {
            "id": module_id.upper(),
            **module
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/kpis")
async def get_kpis():
    """Get all KPIs"""
    return BBC_PROGRAM_DATA["kpis"]


@router.get("/levels")
async def get_levels():
    """Get all education levels with details"""
    return BBC_PROGRAM_DATA["levels"]


# ============================================
# PDF Export Endpoints
# ============================================

from fastapi.responses import HTMLResponse
from app.services.rag.pdf_export import PDFExportService, ReportConfig


@router.get("/report/json")
async def get_report_json():
    """
    Get report content as JSON

    Structured data for custom PDF rendering.
    """
    try:
        config = ReportConfig()
        return PDFExportService.generate_report_content(config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report/markdown")
async def get_report_markdown():
    """
    Get report as Markdown

    Can be converted to PDF using pandoc or similar.
    """
    try:
        config = ReportConfig()
        markdown = PDFExportService.to_markdown(config)
        return {"format": "markdown", "content": markdown}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report/html", response_class=HTMLResponse)
async def get_report_html():
    """
    Get report as HTML

    Ready for printing or PDF conversion (Ctrl+P).
    """
    try:
        config = ReportConfig()
        return PDFExportService.to_html(config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
