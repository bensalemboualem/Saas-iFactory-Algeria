"""
Teaching Agent Team - Multi-agent for education
Specialized for Algerian education system
"""
from typing import Dict, Any, List
from ..core.base_agent import BaseAgent, AgentConfig, AgentResponse, MultiAgentTeam
import logging

logger = logging.getLogger(__name__)

EDUCATIONAL_CONTENT = {
    "subjects": {
        "histoire": {"levels": ["CM1", "CM2", "6ème", "5ème", "4ème", "3ème"]},
        "mathematiques": {"levels": ["CP", "CE1", "CE2", "CM1", "CM2", "6ème", "5ème", "4ème", "3ème"]},
        "sciences": {"levels": ["CE2", "CM1", "CM2", "6ème", "5ème", "4ème", "3ème"]},
        "francais": {"levels": ["CP", "CE1", "CE2", "CM1", "CM2", "6ème", "5ème", "4ème", "3ème"]},
        "arabe": {"levels": ["CP", "CE1", "CE2", "CM1", "CM2", "6ème", "5ème", "4ème", "3ème"]}
    }
}

class ContentGeneratorAgent(BaseAgent):
    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(name="ContentGenerator", model="deepseek-chat", temperature=0.7, language="fr")
        super().__init__(config)
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        subject = input_data.get("subject")
        level = input_data.get("level")
        topic = input_data.get("topic")
        content_type = input_data.get("content_type", "lesson")
        duration = input_data.get("duration", 45)
        
        system_prompt = f"""Tu es un expert en pédagogie pour écoles algériennes.

NIVEAU: {level}
MATIÈRE: {subject}
SUJET: {topic}
TYPE: {content_type}
DURÉE: {duration} minutes

STRUCTURE:
1. Titre et objectifs pédagogiques
2. Prérequis
3. Contenu principal structuré
4. Activités pratiques
5. Points clés à retenir
6. Évaluation

FORMAT: Markdown professionnel
"""
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Crée un {content_type} sur: {topic}"}]
        response = await self._call_llm(messages)
        return AgentResponse(content=response['content'], metadata={"subject": subject, "level": level, "topic": topic})

class AssessmentAgent(BaseAgent):
    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(name="AssessmentAgent", model="deepseek-chat", temperature=0.6, language="fr")
        super().__init__(config)
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        subject = input_data.get("subject")
        level = input_data.get("level")
        topic = input_data.get("topic")
        num_questions = input_data.get("num_questions", 10)
        
        system_prompt = f"""Tu es un expert en évaluation pédagogique.

MATIÈRE: {subject}
NIVEAU: {level}
SUJET: {topic}
QUESTIONS: {num_questions}

Crée une évaluation avec:
- QCM
- Vrai/Faux
- Questions ouvertes
- Exercices d'application
- Corrigé détaillé avec barème
"""
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Crée une évaluation sur: {topic}"}]
        response = await self._call_llm(messages)
        return AgentResponse(content=response['content'], metadata={"subject": subject, "level": level})

class TeachingTeam(MultiAgentTeam):
    def __init__(self):
        agents = [ContentGeneratorAgent(), AssessmentAgent()]
        super().__init__(agents, orchestrator="sequential")
    
    async def create_complete_lesson(self, subject: str, level: str, topic: str) -> Dict[str, Any]:
        lesson = await self.agents[0].execute({"subject": subject, "level": level, "topic": topic, "content_type": "lesson"})
        quiz = await self.agents[1].execute({"subject": subject, "level": level, "topic": topic, "num_questions": 5})
        return {"lesson": lesson.content, "quiz": quiz.content}

__all__ = ['TeachingTeam', 'ContentGeneratorAgent', 'AssessmentAgent', 'EDUCATIONAL_CONTENT']
