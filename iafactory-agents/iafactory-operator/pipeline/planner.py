"""
IA Factory Operator - Edit Planner
LLM-powered edit planning using Claude
"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime

import structlog

from core.config import settings
from core.state import (
    VideoEditorState,
    EditPlan,
    EditAction,
    EditActionType,
    TransitionType,
    SceneSegment,
    PLATFORM_SPECS,
    TEMPLATE_CONFIGS,
)

logger = structlog.get_logger(__name__)


# =============================================================================
# PROMPTS
# =============================================================================

PLANNER_SYSTEM_PROMPT = """Tu es un monteur vidéo professionnel expert pour les réseaux sociaux.
Tu crées des plans de montage optimisés pour l'engagement sur Instagram Reels, TikTok et YouTube Shorts.

Tu dois générer un plan de montage JSON précis basé sur l'analyse de la vidéo source.

Règles importantes:
1. Respecte STRICTEMENT la durée cible demandée (±1 seconde)
2. Privilégie les scènes avec parole (has_speech: true) pour le contenu parlé
3. Garde les meilleures scènes selon leur quality_score et engagement_score
4. Assure des transitions fluides entre les scènes
5. Place les sous-titres de manière visible mais non intrusive
6. Pour le marché algérien, privilégie un style épuré et professionnel

Format de sortie JSON obligatoire:
{
    "reasoning": "Explication de tes choix de montage...",
    "target_duration": 15.0,
    "scenes_to_use": [0, 2, 3],
    "actions": [
        {
            "action_type": "trim",
            "start_time": 0.0,
            "end_time": 5.0,
            "params": {"source_scene": 0}
        },
        {
            "action_type": "transition",
            "start_time": 5.0,
            "end_time": 5.3,
            "params": {"type": "dissolve", "duration": 0.3}
        }
    ],
    "caption_style": {
        "position": "bottom",
        "font_size": 42,
        "font_color": "#FFFFFF",
        "background_color": "#00000080",
        "animation": "fade"
    },
    "color_grade": "natural",
    "music_volume": 0.2
}"""


PLANNER_USER_PROMPT_TEMPLATE = """Crée un plan de montage pour cette vidéo:

**Paramètres demandés:**
- Durée cible: {target_duration} secondes
- Template: {template}
- Style: {style}
- Plateformes: {platforms}
- Langue: {language}
- Ajouter sous-titres: {add_captions}
- Ajouter musique: {add_music}

**Analyse de la vidéo source:**
- Durée totale: {source_duration:.1f}s
- Résolution: {width}x{height}
- FPS: {fps}
- Nombre de scènes: {total_scenes}

**Scènes détectées:**
{scenes_json}

**Transcription:**
{transcript}

Génère le plan de montage JSON optimisé pour maximiser l'engagement.
Assure-toi que la durée finale soit exactement {target_duration} secondes."""


# =============================================================================
# EDIT PLANNER
# =============================================================================

class EditPlanner:
    """
    Plans video edits using Claude LLM.
    Takes video analysis and generates an edit plan.
    """
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    async def plan(self, state: VideoEditorState) -> VideoEditorState:
        """Generate edit plan from video analysis"""
        state.add_log("📝 Planning video edits with AI...")
        state.set_status("planning", progress=45, stage="planning")
        
        try:
            if not state.analysis:
                raise ValueError("No video analysis available")
            
            analysis = state.analysis
            
            # Build prompt
            scenes_data = self._format_scenes_for_prompt(analysis.scenes)
            
            user_prompt = PLANNER_USER_PROMPT_TEMPLATE.format(
                target_duration=state.target_duration,
                template=state.template,
                style=state.style,
                platforms=", ".join(state.platforms),
                language=state.language,
                add_captions=state.add_captions,
                add_music=state.add_music,
                source_duration=analysis.duration,
                width=analysis.width,
                height=analysis.height,
                fps=analysis.fps,
                total_scenes=analysis.total_scenes,
                scenes_json=scenes_data,
                transcript=analysis.full_transcript[:2000] if analysis.full_transcript else "(Pas de transcription)",
            )
            
            state.add_log("🤖 Generating edit plan with Claude...")
            state.set_status("planning", progress=50)
            
            # Call LLM
            response = await self.llm_client.generate(
                system_prompt=PLANNER_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                max_tokens=2000,
                temperature=0.3,
            )
            
            state.add_log("📊 Parsing LLM response...")
            state.set_status("planning", progress=60)
            
            # Parse response
            plan_data = self._parse_llm_response(response)
            
            # Validate and build edit plan
            edit_plan = self._build_edit_plan(plan_data, state, analysis)
            
            state.edit_plan = edit_plan
            state.add_log(f"✅ Edit plan ready: {len(edit_plan.actions)} actions, {len(edit_plan.scenes_to_use)} scenes")
            state.set_status("planning", progress=70)
            
            return state
            
        except Exception as e:
            logger.exception("Edit planning failed", error=str(e))
            state.error = f"Planning failed: {str(e)}"
            state.add_log(f"❌ Planning error: {str(e)}")
            
            # Fallback to simple plan
            state.add_log("⚠️ Using fallback simple plan...")
            state.edit_plan = self._create_fallback_plan(state)
            return state
    
    def _format_scenes_for_prompt(self, scenes: List[SceneSegment]) -> str:
        """Format scenes as JSON for prompt"""
        scenes_list = []
        for i, scene in enumerate(scenes):
            scenes_list.append({
                "index": i,
                "start": round(scene.start_time, 2),
                "end": round(scene.end_time, 2),
                "duration": round(scene.duration, 2),
                "has_speech": scene.has_speech,
                "quality_score": round(scene.quality_score, 2),
                "motion_score": round(scene.motion_score, 2),
            })
        return json.dumps(scenes_list, indent=2, ensure_ascii=False)
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from LLM response"""
        # Try to extract JSON from response
        response = response.strip()
        
        # Handle markdown code blocks
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            response = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            response = response[start:end].strip()
        
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.debug(f"Response was: {response[:500]}")
            raise ValueError(f"Invalid JSON from LLM: {str(e)}")
    
    def _build_edit_plan(
        self,
        plan_data: Dict[str, Any],
        state: VideoEditorState,
        analysis: "VideoAnalysis"
    ) -> EditPlan:
        """Build EditPlan from parsed LLM response"""
        
        # Get platform specs
        primary_platform = state.platforms[0] if state.platforms else "instagram_reels"
        specs = PLATFORM_SPECS.get(primary_platform, PLATFORM_SPECS["instagram_reels"])
        
        # Build actions
        actions = []
        for i, action_data in enumerate(plan_data.get("actions", [])):
            action = EditAction(
                action_type=EditActionType(action_data.get("action_type", "trim")),
                start_time=float(action_data.get("start_time", 0)),
                end_time=float(action_data.get("end_time", 0)),
                params=action_data.get("params", {}),
                order=i,
            )
            actions.append(action)
        
        # Build caption segments from transcript
        caption_segments = []
        if state.add_captions and analysis.transcript_segments:
            for seg in analysis.transcript_segments:
                caption_segments.append({
                    "start": seg.get("start", 0),
                    "end": seg.get("end", 0),
                    "text": seg.get("text", ""),
                })
        
        plan = EditPlan(
            plan_id=f"plan_{state.job_id}",
            created_at=datetime.utcnow(),
            target_duration=float(plan_data.get("target_duration", state.target_duration)),
            target_width=specs["width"],
            target_height=specs["height"],
            target_fps=float(specs.get("fps", 30)),
            scenes_to_use=plan_data.get("scenes_to_use", list(range(min(5, analysis.total_scenes)))),
            actions=actions,
            caption_segments=caption_segments,
            caption_style=plan_data.get("caption_style", {
                "position": "bottom",
                "font_size": 42,
                "font_color": "#FFFFFF",
            }),
            music_track=plan_data.get("music_track"),
            music_volume=float(plan_data.get("music_volume", 0.2)),
            color_grade_preset=plan_data.get("color_grade"),
            reasoning=plan_data.get("reasoning", ""),
            confidence=0.8,
        )
        
        return plan
    
    def _create_fallback_plan(self, state: VideoEditorState) -> EditPlan:
        """Create a simple fallback plan if LLM fails"""
        analysis = state.analysis
        if not analysis:
            raise ValueError("No analysis for fallback plan")
        
        primary_platform = state.platforms[0] if state.platforms else "instagram_reels"
        specs = PLATFORM_SPECS.get(primary_platform, PLATFORM_SPECS["instagram_reels"])
        
        # Simple plan: take first N seconds, crop to vertical
        target_duration = state.target_duration
        
        actions = [
            EditAction(
                action_type=EditActionType.trim,
                start_time=0,
                end_time=min(target_duration, analysis.duration),
                params={"source": "full"},
                order=0,
            ),
            EditAction(
                action_type=EditActionType.crop_resize,
                start_time=0,
                end_time=target_duration,
                params={
                    "width": specs["width"],
                    "height": specs["height"],
                    "mode": "center_crop",
                },
                order=1,
            ),
        ]
        
        # Add fade in/out
        actions.append(EditAction(
            action_type=EditActionType.fade_in,
            start_time=0,
            end_time=0.5,
            params={"duration": 0.5},
            order=2,
        ))
        actions.append(EditAction(
            action_type=EditActionType.fade_out,
            start_time=target_duration - 0.5,
            end_time=target_duration,
            params={"duration": 0.5},
            order=3,
        ))
        
        return EditPlan(
            plan_id=f"fallback_{state.job_id}",
            target_duration=target_duration,
            target_width=specs["width"],
            target_height=specs["height"],
            target_fps=30.0,
            scenes_to_use=list(range(min(3, analysis.total_scenes))),
            actions=actions,
            reasoning="Fallback plan: simple trim and crop",
            confidence=0.5,
        )


# =============================================================================
# MODULE FUNCTION
# =============================================================================

async def plan_edits(state: VideoEditorState, llm_client) -> VideoEditorState:
    """Convenience function to plan edits"""
    planner = EditPlanner(llm_client=llm_client)
    return await planner.plan(state)
