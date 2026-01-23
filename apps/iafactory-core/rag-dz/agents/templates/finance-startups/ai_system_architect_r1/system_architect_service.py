# system_architect_service.py

from typing import Optional, List, Dict, Any, Union
import os
import logging
import json

from openai import OpenAI
import anthropic
from pydantic import BaseModel, Field
from enum import Enum

from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.models.anthropic import Claude

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Pydantic Models for Data Structure ---
class ArchitecturePattern(str, Enum):
    MICROSERVICES = "microservices"
    MONOLITHIC = "monolithic"
    SERVERLESS = "serverless"
    EVENT_DRIVEN = "event_driven"

class DatabaseType(str, Enum):
    SQL = "sql"
    NOSQL = "nosql"
    HYBRID = "hybrid"

class ComplianceStandard(str, Enum):
    HIPAA = "hipaa"
    GDPR = "gdpr"
    SOC2 = "soc2"
    ISO27001 = "iso27001"

class ArchitectureDecision(BaseModel):
    pattern: ArchitecturePattern
    rationale: str = Field(..., min_length=50)
    trade_offs: Dict[str, List[str]]
    estimated_cost: Dict[str, float]

class SecurityMeasure(BaseModel):
    measure_type: str
    implementation_priority: int = Field(..., ge=1, le=5)
    compliance_standards: List[ComplianceStandard]
    data_classification: str

class InfrastructureResource(BaseModel):
    resource_type: str
    specifications: Dict[str, str]
    scaling_policy: Dict[str, str]
    estimated_cost: float

class TechnicalAnalysis(BaseModel):
    architecture_decision: ArchitectureDecision
    infrastructure_resources: List[InfrastructureResource]
    security_measures: List[SecurityMeasure]
    database_choice: DatabaseType
    compliance_requirements: List[ComplianceStandard] = []
    performance_requirements: List[Dict[str, Union[str, float]]] = []
    risk_assessment: Dict[str, str] = {}


class SystemArchitectService:
    """
    A service to perform system architecture analysis using a dual-model approach,
    decoupled from any specific UI.
    """
    def __init__(self, deepseek_api_key: str, anthropic_api_key: str):
        if not deepseek_api_key or not anthropic_api_key:
            raise ValueError("DeepSeek and Anthropic API keys are required.")
        
        self.deepseek_client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
        
        claude_model = Claude(
            id="claude-3.5-sonnet-20240620", 
            api_key=anthropic_api_key,
            system_prompt="""Given the user's query and the DeepSeek reasoning:
            1. Provide a detailed analysis of the architecture decisions.
            2. Generate a project implementation roadmap.
            3. Create a comprehensive technical specification document.
            4. Format the output in clean markdown with proper sections.
            5. Include diagrams descriptions in mermaid.js format."""
        )
        self.claude_agent = Agent(model=claude_model, markdown=True)

    def _get_deepseek_reasoning(self, user_input: str) -> Dict[str, Any]:
        system_prompt = """You are an expert software architect... (full prompt as in original file)
        Your response must be a valid JSON object that matches the provided schema."""

        try:
            logger.info("[DeepSeek] Requesting technical analysis...")
            deepseek_response = self.deepseek_client.chat.completions.create(
                model="deepseek-reasoner",
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
                max_tokens=8000,
                stream=False
            )
            reasoning_content = deepseek_response.choices[0].message.reasoning_content
            normal_content = deepseek_response.choices[0].message.content
            logger.info("[DeepSeek] Analysis received.")
            
            return {
                "success": True,
                "reasoning": reasoning_content,
                "technical_analysis_json": normal_content
            }
        except Exception as e:
            logger.error(f"Error in DeepSeek analysis: {str(e)}")
            return {"success": False, "error": str(e)}

    def _get_claude_response(self, user_input: str, deepseek_output: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info("[Claude] Requesting detailed explanation...")
            message = f"""User Query: {user_input}\n\nDeepSeek Reasoning: {deepseek_output['reasoning']}\n\nDeepSeek Technical Analysis JSON: {deepseek_output['technical_analysis_json']}\n\nGive detailed explanation for each key value pair in brief in the JSON object, and why we chose it clearly. Don't use your own opinions, use the reasoning and the structured output to explain the choices."""
            
            response: RunOutput = self.claude_agent.run(message=message)
            logger.info("[Claude] Explanation received.")
            
            return {
                "success": True,
                "detailed_report": response.content
            }
        except Exception as e:
            logger.error(f"Error in Claude response: {str(e)}")
            return {"success": False, "error": str(e)}

    def analyze_architecture(self, user_prompt: str) -> Dict[str, Any]:
        """
        Runs the full dual-model pipeline to generate an architectural analysis.
        """
        logger.info(f"Starting architecture analysis for prompt: '{user_prompt[:50]}'...")
        
        deepseek_result = self._get_deepseek_reasoning(user_prompt)
        if not deepseek_result["success"]:
            return deepseek_result

        claude_result = self._get_claude_response(user_prompt, deepseek_result)
        if not claude_result["success"]:
            return claude_result
            
        return {
            "success": True,
            "reasoning": deepseek_result["reasoning"],
            "technical_analysis_json": deepseek_result["technical_analysis_json"],
            "detailed_report": claude_result["detailed_report"]
        }


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    ds_key = os.getenv("DEEPSEEK_API_KEY")
    ant_key = os.getenv("ANTHROPIC_API_KEY")

    if not ds_key or not ant_key:
        print("Please set DEEPSEEK_API_KEY and ANTHROPIC_API_KEY in your .env file.")
    else:
        service = SystemArchitectService(deepseek_api_key=ds_key, anthropic_api_key=ant_key)
        
        test_prompt = """We need to build a high-frequency trading platform that processes market data streams, 
        executes trades with sub-millisecond latency, maintains audit trails, and handles complex risk calculations."""
        
        print(f"--- Analyzing architecture for: {test_prompt[:50]}... ---")
        result = service.analyze_architecture(test_prompt)
        
        if result["success"]:
            print("\n--- DETAILED REPORT ---")
            print(result["detailed_report"])
        else:
            print(f"\n--- ERROR ---")
            print(result["error"])
