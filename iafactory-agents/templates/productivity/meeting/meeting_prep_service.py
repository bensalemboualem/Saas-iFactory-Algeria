# meeting_prep_service.py

import os
import logging
from typing import Dict, List, Optional, Any
from textwrap import dedent

from crewai import Agent, Task, Crew, LLM
from crewai.process import Process
from crewai_tools import SerperDevTool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MeetingPrepService:
    """
    A service to prepare comprehensive meeting materials using a multi-agent system,
    decoupled from any specific UI.
    """
    
    def __init__(self, anthropic_api_key: str, serper_api_key: str):
        if not anthropic_api_key or not serper_api_key:
            raise ValueError("Anthropic and Serper API keys are required.")
        
        # Set API keys as environment variables for CrewAI tools
        os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key
        os.environ["SERPER_API_KEY"] = serper_api_key

        self._define_agents_and_crew()

    def _define_agents_and_crew(self):
        """Initializes the agents, tasks, and crew for meeting preparation."""
        
        # Define the LLM for all agents
        claude_llm = LLM(model="claude-3-5-sonnet-20240620", temperature=0.7)
        
        # Define the search tool
        search_tool = SerperDevTool()

        # Define the agents
        self.context_analyzer = Agent(
            role='Meeting Context Specialist',
            goal='Analyze and summarize key background information for the meeting',
            backstory='You are an expert at quickly understanding complex business contexts and identifying critical information.',
            verbose=False, # Set to False for service, logging will cover it
            allow_delegation=False,
            llm=claude_llm,
            tools=[search_tool]
        )

        self.industry_insights_generator = Agent(
            role='Industry Expert',
            goal='Provide in-depth industry analysis and identify key trends',
            backstory='You are a seasoned industry analyst with a knack for spotting emerging trends and opportunities.',
            verbose=False,
            allow_delegation=False,
            llm=claude_llm,
            tools=[search_tool]
        )

        self.strategy_formulator = Agent(
            role='Meeting Strategist',
            goal='Develop a tailored meeting strategy and detailed agenda',
            backstory='You are a master meeting planner, known for creating highly effective strategies and agendas.',
            verbose=False,
            allow_delegation=False,
            llm=claude_llm,
        )

        self.executive_briefing_creator = Agent(
            role='Communication Specialist',
            goal='Synthesize information into concise and impactful briefings',
            backstory='You are an expert communicator, skilled at distilling complex information into clear, actionable insights.',
            verbose=False,
            allow_delegation=False,
            llm=claude_llm,
        )
        
        # The crew will be created dynamically in prepare_meeting to pass task descriptions

    def prepare_meeting(self, company_name: str, meeting_objective: str, attendees: str, meeting_duration: int, focus_areas: str) -> Dict[str, Any]:
        """
        Runs the multi-agent pipeline to generate meeting preparation materials.
        """
        if not all([company_name, meeting_objective, attendees, meeting_duration]):
            return {"success": False, "error": "Missing required meeting details."}

        logger.info(f"Starting meeting preparation for company: '{company_name}' with objective: '{meeting_objective}'")
        
        try:
            # Define the tasks dynamically based on input
            context_analysis_task = Task(
                description=dedent(f"""
                Analyze the context for the meeting with {company_name}, considering:
                1. The meeting objective: {meeting_objective}
                2. The attendees: {attendees}
                3. The meeting duration: {meeting_duration} minutes
                4. Specific focus areas or concerns: {focus_areas}

                Research {company_name} thoroughly, including:
                1. Recent news and press releases
                2. Key products or services
                3. Major competitors

                Provide a comprehensive summary of your findings, highlighting the most relevant information for the meeting context.
                Format your output using markdown with appropriate headings and subheadings.
                """),
                agent=self.context_analyzer,
                expected_output="A detailed analysis of the meeting context and company background, including recent developments, financial performance, and relevance to the meeting objective, formatted in markdown with headings and subheadings."
            )

            industry_analysis_task = Task(
                description=dedent(f"""
                Based on the context analysis for {company_name} and the meeting objective: {meeting_objective}, provide an in-depth industry analysis:
                1. Identify key trends and developments in the industry
                2. Analyze the competitive landscape
                3. Highlight potential opportunities and threats
                4. Provide insights on market positioning

                Ensure the analysis is relevant to the meeting objective and attendees' roles.
                Format your output using markdown with appropriate headings and subheadings.
                """),
                agent=self.industry_insights_generator,
                expected_output="A comprehensive industry analysis report, including trends, competitive landscape, opportunities, threats, and relevant insights for the meeting objective, formatted in markdown with headings and subheadings."
            )

            strategy_development_task = Task(
                description=dedent(f"""
                Using the context analysis and industry insights, develop a tailored meeting strategy and detailed agenda for the {meeting_duration}-minute meeting with {company_name}. Include:
                1. A time-boxed agenda with clear objectives for each section
                2. Key talking points for each agenda item
                3. Suggested speakers or leaders for each section
                4. Potential discussion topics and questions to drive the conversation
                5. Strategies to address the specific focus areas and concerns: {focus_areas}

                Ensure the strategy and agenda align with the meeting objective: {meeting_objective}
                Format your output using markdown with appropriate headings and subheadings.
                """),
                agent=self.strategy_formulator,
                expected_output="A detailed meeting strategy and time-boxed agenda, including objectives, key talking points, and strategies to address specific focus areas, formatted in markdown with headings and subheadings."
            )

            executive_brief_task = Task(
                description=dedent(f"""
                Synthesize all the gathered information into a comprehensive yet concise executive brief for the meeting with {company_name}. Create the following components:

                1. A detailed one-page executive summary including:
                   - Clear statement of the meeting objective
                   - List of key attendees and their roles
                   - Critical background points about {company_name} and relevant industry context
                   - Top 3-5 strategic goals for the meeting, aligned with the objective
                   - Brief overview of the meeting structure and key topics to be covered

                2. An in-depth list of key talking points, each supported by:
                   - Relevant data or statistics
                   - Specific examples or case studies
                   - Connection to the company's current situation or challenges

                3. Anticipate and prepare for potential questions:
                   - List likely questions from attendees based on their roles and the meeting objective
                   - Craft thoughtful, data-driven responses to each question
                   - Include any supporting information or additional context that might be needed

                4. Strategic recommendations and next steps:
                   - Provide 3-5 actionable recommendations based on the analysis
                   - Outline clear next steps for implementation or follow-up
                   - Suggest timelines or deadlines for key actions
                   - Identify potential challenges or roadblocks and propose mitigation strategies

                Ensure the brief is comprehensive yet concise, highly actionable, and precisely aligned with the meeting objective: {meeting_objective}. The document should be structured for easy navigation and quick reference during the meeting.
                Format your output using markdown with appropriate headings and subheadings.
                """),
                agent=self.executive_briefing_creator,
                expected_output="A comprehensive executive brief including summary, key talking points, Q&A preparation, and strategic recommendations, formatted in markdown with main headings (H1), section headings (H2), and subsection headings (H3) where appropriate. Use bullet points, numbered lists, and emphasis (bold/italic) for key information."
            )

            # Create the crew
            meeting_prep_crew = Crew(
                agents=[self.context_analyzer, self.industry_insights_generator, self.strategy_formulator, self.executive_briefing_creator],
                tasks=[context_analysis_task, industry_analysis_task, strategy_development_task, executive_brief_task],
                verbose=True, # Can set to False for production service
                process=Process.sequential
            )
            
            result = meeting_prep_crew.kickoff()
            
            logger.info(f"Successfully prepared meeting for '{company_name}'.")
            return {
                "success": True,
                "preparation_material": result
            }

        except Exception as e:
            logger.error(f"An error occurred during meeting preparation: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

# Example of how to use the service
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    ant_key = os.getenv("ANTHROPIC_API_KEY")
    serp_key = os.getenv("SERPER_API_KEY")

    if not ant_key or not serp_key:
        print("Please set ANTHROPIC_API_KEY and SERPER_API_KEY in your .env file.")
    else:
        service = MeetingPrepService(anthropic_api_key=ant_key, serper_api_key=serp_key)
        
        comp_name = "Tech Innovations Inc."
        obj = "Discuss Q4 strategy and product roadmap."
        attend = "John Doe (CEO), Jane Smith (CTO), Bob Johnson (Head of Product)"
        duration = 90
        focus = "Market trends, competitive landscape, budget allocation"
        
        print(f"--- Preparing meeting for {comp_name} ---")
        result = service.prepare_meeting(comp_name, obj, attend, duration, focus)
        
        if result["success"]:
            print("\n--- MEETING PREPARATION MATERIAL ---")
            print(result["preparation_material"])
        else:
            print(f"\n--- ERROR ---")
            print(result["error"])
