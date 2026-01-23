# product_launch_service.py

import os
import logging
from typing import Dict, Any
from textwrap import dedent

from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.firecrawl import FirecrawlTools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProductLaunchService:
    """
    A service to perform product launch intelligence analysis using a multi-agent team,
    decoupled from any specific UI.
    """
    
    def __init__(self, openai_api_key: str, firecrawl_api_key: str):
        if not openai_api_key or not firecrawl_api_key:
            raise ValueError("OpenAI and Firecrawl API keys are required.")
        
        # Set environment variables for Agno to pick up
        os.environ["OPENAI_API_KEY"] = openai_api_key
        os.environ["FIRECRAWL_API_KEY"] = firecrawl_api_key
        
        self._define_agents_and_team()

    def _define_agents_and_team(self):
        """Initializes the specialized agents and the coordinated team."""
        
        # Agent 1: Competitor Launch Analyst
        self.launch_analyst = Agent(
            name="Product Launch Analyst",
            description=dedent("""
                You are a senior Go-To-Market strategist who evaluates competitor product launches with a critical, evidence-driven lens.
                Your objective is to uncover:
                • How the product is positioned in the market
                • Which launch tactics drove success (strengths)
                • Where execution fell short (weaknesses)
                • Actionable learnings competitors can leverage
                Always cite observable signals (messaging, pricing actions, channel mix, timing, engagement metrics). Maintain a crisp, executive tone and focus on strategic value.
                IMPORTANT: Conclude your report with a 'Sources:' section, listing all URLs of websites you crawled or searched for this analysis.
            """),
            model=OpenAIChat(id="gpt-4o"),
            tools=[FirecrawlTools(search=True, crawl=True, poll_interval=10)],
            debug_mode=False, # Set to False for service
            markdown=True,
            exponential_backoff=True,
            delay_between_retries=2,
        )
        
        # Agent 2: Market Sentiment Specialist
        self.sentiment_analyst = Agent(
            name="Market Sentiment Specialist",
            description=dedent("""
                You are a market research expert specializing in sentiment analysis and consumer perception tracking.
                Your expertise includes:
                • Analyzing social media sentiment and customer feedback
                • Identifying positive and negative sentiment drivers
                • Tracking brand perception trends across platforms
                • Monitoring customer satisfaction and review patterns
                • Providing actionable insights on market reception
                Focus on extracting sentiment signals from social platforms, review sites, forums, and customer feedback channels.
                IMPORTANT: Conclude your report with a 'Sources:' section, listing all URLs of websites you crawled or searched for this analysis.
            """),
            model=OpenAIChat(id="gpt-4o"),
            tools=[FirecrawlTools(search=True, crawl=True, poll_interval=10)],
            debug_mode=False,
            markdown=True,
            exponential_backoff=True,
            delay_between_retries=2,
        )
        
        # Agent 3: Launch Metrics Specialist
        self.metrics_analyst = Agent(
            name="Launch Metrics Specialist", 
            description=dedent("""
                You are a product launch performance analyst who specializes in tracking and analyzing launch KPIs.
                Your focus areas include:
                • User adoption and engagement metrics
                • Revenue and business performance indicators
                • Market penetration and growth rates
                • Press coverage and media attention analysis
                • Social media traction and viral coefficient tracking
                • Competitive market share analysis
                Always provide quantitative insights with context and benchmark against industry standards when possible.
                IMPORTANT: Conclude your report with a 'Sources:' section, listing all URLs of websites you crawled or searched for this analysis.
            """),
            model=OpenAIChat(id="gpt-4o"),
            tools=[FirecrawlTools(search=True, crawl=True, poll_interval=10)],
            debug_mode=False,
            markdown=True,
            exponential_backoff=True,
            delay_between_retries=2,
        )

        # Create the coordinated team
        self.product_intelligence_team = Team(
            name="Product Intelligence Team",
            model=OpenAIChat(id="gpt-4o"),
            members=[self.launch_analyst, self.sentiment_analyst, self.metrics_analyst],
            instructions=[
                "Coordinate the analysis based on the user's request type:",
                "1. For competitor analysis: Use the Product Launch Analyst to evaluate positioning, strengths, weaknesses, and strategic insights",
                "2. For market sentiment: Use the Market Sentiment Specialist to analyze social media sentiment, customer feedback, and brand perception",
                "3. For launch metrics: Use the Launch Metrics Specialist to track KPIs, adoption rates, press coverage, and performance indicators",
                "Always provide evidence-based insights with specific examples and data points",
                "Structure responses with clear sections and actionable recommendations",
                "Include sources section with all URLs crawled or searched"
            ],
            markdown=True,
            debug_mode=False,
            show_members_responses=False, # Set to False for service
        )

    # Helper to craft competitor-focused launch report for product managers
    def _expand_competitor_report(self, bullet_text: str, competitor: str) -> str:
        prompt = (
            f"Transform the insight bullets below into a professional launch review for product managers analysing {competitor}.\n\n"
            f"Produce well-structured **Markdown** with a mix of tables, call-outs and concise bullet points — avoid long paragraphs.\n\n"
            f"=== FORMAT SPECIFICATION ===\n"
            f"# {competitor} – Launch Review\n\n"
            f"## 1. Market & Product Positioning\n"
            f"• Bullet point summary of how the product is positioned (max 6 bullets).\n\n"
            f"## 2. Launch Strengths\n"
            f"| Strength | Evidence / Rationale |\n|---|---|
| … | … | (add 4-6 rows)\n\n"
            f"## 3. Launch Weaknesses\n"
            f"| Weakness | Evidence / Rationale |\n|---|---|
| … | … | (add 4-6 rows)\n\n"
            f"## 4. Strategic Takeaways for Competitors\n"
            f"1. … (max 5 numbered recommendations)\n\n"
            f"=== SOURCE BULLETS ===\n{bullet_text}\n\n"
            f"Guidelines:\n"
            f"• Populate the tables with specific points derived from the bullets.\n"
            f"• Only include rows that contain meaningful data; omit any blank entries."
        )
        resp: RunOutput = self.product_intelligence_team.run(prompt)
        return resp.content if hasattr(resp, "content") else str(resp)

    # Helper to craft market sentiment report
    def _expand_sentiment_report(self, bullet_text: str, product: str) -> str:
        prompt = (
            f"Use the tagged bullets below to create a concise market-sentiment brief for **{product}**.\n\n"
            f"### Positive Sentiment\n"
            f"• List each positive point as a separate bullet (max 6).\n\n"
            f"### Negative Sentiment\n"
            f"• List each negative point as a separate bullet (max 6).\n\n"
            f"### Overall Summary\n"
            f"Provide a short paragraph (≤120 words) summarising the overall sentiment balance and key drivers.\n\n"
            f"Tagged Bullets:\n{bullet_text}"
        )
        resp: RunOutput = self.product_intelligence_team.run(prompt)
        return resp.content if hasattr(resp, "content") else str(resp)

    # Helper to craft launch metrics report
    def _expand_metrics_report(self, bullet_text: str, launch: str) -> str:
        prompt = (
            f"Convert the KPI bullets below into a launch-performance snapshot for **{launch}** suitable for an executive dashboard.\n\n"
            f"## Key Performance Indicators\n"
            f"| Metric | Value / Detail | Source |\n"
            f"|---|---|---|
| … | … | … |  (include one row per KPI)\n\n"
            f"## Qualitative Signals\n"
            f"• Bullet list of notable qualitative insights (max 5).\n\n"
            f"## Summary & Implications\n"
            f"Brief paragraph (≤120 words) highlighting what the metrics imply about launch success and next steps.\n\n"
            f"KPI Bullets:\n{bullet_text}"
        )
        resp: RunOutput = self.product_intelligence_team.run(prompt)
        return resp.content if hasattr(resp, "content") else str(resp)
    
    def analyze_launch(self, company_name: str, analysis_type: str) -> Dict[str, Any]:
        """
        Performs a product launch intelligence analysis for a given company.
        analysis_type can be "competitor", "sentiment", or "metrics".
        """
        if not company_name:
            return {"success": False, "error": "Company name is required."}
        if analysis_type not in ["competitor", "sentiment", "metrics"]:
            return {"success": False, "error": "Invalid analysis type. Choose 'competitor', 'sentiment', or 'metrics'."}

        logger.info(f"Starting '{analysis_type}' analysis for company: '{company_name}'")
        
        try:
            if analysis_type == "competitor":
                query = (
                    f"Generate up to 16 evidence-based insight bullets about {company_name}'s most recent product launches.\n"
                    f"Format requirements:\n"
                    f"• Start every bullet with exactly one tag: Positioning | Strength | Weakness | Learning\n"
                    f"• Follow the tag with a concise statement (max 30 words) referencing concrete observations: messaging, differentiation, pricing, channel selection, timing, engagement metrics, or customer feedback."
                )
                bullets: RunOutput = self.product_intelligence_team.run(query)
                report_content = self._expand_competitor_report(
                    bullets.content if hasattr(bullets, "content") else str(bullets),
                    company_name
                )
            elif analysis_type == "sentiment":
                query = (
                    f"Summarize market sentiment for {company_name} in <=10 bullets. "
                    f"Cover top positive & negative themes with source mentions (G2, Reddit, Twitter, customer reviews)."
                )
                bullets: RunOutput = self.product_intelligence_team.run(query)
                report_content = self._expand_sentiment_report(
                    bullets.content if hasattr(bullets, "content") else str(bullets),
                    company_name
                )
            else: # metrics
                query = (
                    f"List (max 10 bullets) the most important publicly available KPIs & qualitative signals for {company_name}'s recent product launches. "
                    f"Include engagement stats, press coverage, adoption metrics, and market traction data if available."
                )
                bullets: RunOutput = self.product_intelligence_team.run(query)
                report_content = self._expand_metrics_report(
                    bullets.content if hasattr(bullets, "content") else str(bullets),
                    company_name
                )
            
            if report_content:
                logger.info(f"Successfully generated '{analysis_type}' report for '{company_name}'.")
                return {
                    "success": True,
                    "report": report_content
                }
            else:
                logger.error("Team run did not produce any content for the report.")
                return {
                    "success": False,
                    "error": "Team run did not produce any content for the report."
                }

        except Exception as e:
            logger.error(f"An error occurred during {analysis_type} analysis: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

# Example of how to use the service
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    openai_key = os.getenv("OPENAI_API_KEY")
    firecrawl_key = os.getenv("FIRECRAWL_API_KEY")

    if not openai_key or not firecrawl_key:
        print("Please set OPENAI_API_KEY and FIRECRAWL_API_KEY in your .env file.")
    else:
        service = ProductLaunchService(openai_api_key=openai_key, firecrawl_api_key=firecrawl_key)
        
        company = "Apple" 
        
        print(f"--- Analyzing Competitor Strategy for {company} ---")
        competitor_result = service.analyze_launch(company, "competitor")
        if competitor_result["success"]:
            print(competitor_result["report"])
        else:
            print(f"Error: {competitor_result['error']}")

        print(f"\n--- Analyzing Market Sentiment for {company} ---")
        sentiment_result = service.analyze_launch(company, "sentiment")
        if sentiment_result["success"]:
            print(sentiment_result["report"])
        else:
            print(f"Error: {sentiment_result['error']}")
            
        print(f"\n--- Analyzing Launch Metrics for {company} ---")
        metrics_result = service.analyze_launch(company, "metrics")
        if metrics_result["success"]:
            print(metrics_result["report"])
        else:
            print(f"Error: {metrics_result['error']}")
