"""
Recruitment Agent Team - HR automation for PMEs
"""
from typing import Dict, Any, List
from ..core.base_agent import BaseAgent, AgentConfig, AgentResponse, MultiAgentTeam
import logging

logger = logging.getLogger(__name__)

class JobPostingAgent(BaseAgent):
    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(name="JobPostingAgent", model="deepseek-chat", temperature=0.7, language="fr")
        super().__init__(config)
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        job_title = input_data.get("job_title")
        department = input_data.get("department")
        experience = input_data.get("experience_years", 2)
        skills = input_data.get("required_skills", [])
        location = input_data.get("location")
        contract_type = input_data.get("contract_type", "CDI")
        salary_range = input_data.get("salary_range")
        
        system_prompt = f"""Tu es un expert RH en rédaction d'offres d'emploi.

POSTE: {job_title}
DÉPARTEMENT: {department}
EXPÉRIENCE: {experience} ans
COMPÉTENCES: {skills}
LIEU: {location}
CONTRAT: {contract_type}
SALAIRE: {salary_range}

Crée une offre d'emploi professionnelle:
1. 🎯 Titre accrocheur
2. 🏢 Présentation entreprise
3. 📋 Missions principales
4. ✅ Profil recherché
5. 💼 Compétences requises
6. 🎁 Avantages
7. 📩 Processus candidature
"""
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Crée une offre pour {job_title}"}]
        response = await self._call_llm(messages)
        return AgentResponse(content=response['content'], metadata={"job_title": job_title, "location": location})

class CVScreenerAgent(BaseAgent):
    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(name="CVScreener", model="deepseek-chat", temperature=0.4, language="fr")
        super().__init__(config)
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        cv_text = input_data.get("cv_text")
        job_requirements = input_data.get("job_requirements", {})
        required_skills = input_data.get("required_skills", [])
        
        system_prompt = f"""Tu es un expert en screening de CV.

EXIGENCES POSTE:
{job_requirements}

COMPÉTENCES REQUISES:
{required_skills}

ANALYSE DU CV:
1. 📊 Score global (0-100)
2. ✅ Compétences correspondantes
3. ❌ Compétences manquantes
4. 💼 Expérience pertinente
5. 🎓 Formation
6. 💪 Points forts
7. ⚠️ Points d'attention
8. 📝 Recommandation (Retenir/À revoir/Rejeter)
"""
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Analyse ce CV:\n\n{cv_text}"}]
        response = await self._call_llm(messages)
        return AgentResponse(content=response['content'], metadata={"job_requirements": job_requirements})

class InterviewGuideAgent(BaseAgent):
    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(name="InterviewGuide", model="deepseek-chat", temperature=0.6, language="fr")
        super().__init__(config)
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        job_title = input_data.get("job_title")
        interview_type = input_data.get("interview_type", "technique")
        duration = input_data.get("duration", 45)
        competencies = input_data.get("competencies", [])
        
        system_prompt = f"""Tu es un expert en recrutement.

POSTE: {job_title}
TYPE: {interview_type}
DURÉE: {duration} min
COMPÉTENCES À ÉVALUER: {competencies}

Crée un guide d'entretien structuré:
1. 🎯 Introduction (5 min)
2. 💼 Questions techniques
3. 🧠 Questions comportementales (STAR)
4. 🎭 Mise en situation
5. ❓ Questions du candidat
6. 📋 Grille d'évaluation
7. 📝 Notes pour le recruteur
"""
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Crée un guide pour {job_title}"}]
        response = await self._call_llm(messages)
        return AgentResponse(content=response['content'], metadata={"job_title": job_title, "interview_type": interview_type})

class RecruitmentTeam(MultiAgentTeam):
    def __init__(self):
        agents = [JobPostingAgent(), CVScreenerAgent(), InterviewGuideAgent()]
        super().__init__(agents, orchestrator="sequential")
    
    async def full_recruitment_pipeline(self, job_data: Dict[str, Any], cv_list: List[str] = None) -> Dict[str, Any]:
        job_posting = await self.agents[0].execute(job_data)
        interview_guide = await self.agents[2].execute({"job_title": job_data.get("job_title"), "competencies": job_data.get("required_skills", [])})
        
        screened_cvs = []
        if cv_list:
            for cv in cv_list:
                result = await self.agents[1].execute({"cv_text": cv, "required_skills": job_data.get("required_skills", [])})
                screened_cvs.append(result.content)
        
        return {"job_posting": job_posting.content, "interview_guide": interview_guide.content, "screened_cvs": screened_cvs}

__all__ = ['RecruitmentTeam', 'JobPostingAgent', 'CVScreenerAgent', 'InterviewGuideAgent']
