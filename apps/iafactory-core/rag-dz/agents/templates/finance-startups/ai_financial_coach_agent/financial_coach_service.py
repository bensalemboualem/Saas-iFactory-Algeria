# financial_coach_service.py

import pandas as pd
from typing import Dict, List, Optional, Any
import os
import asyncio
from datetime import datetime
import json
import logging
from pydantic import BaseModel, Field

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

APP_NAME = "finance_advisor_service"
USER_ID = "default_user"

# --- Pydantic Models for Data Structure ---
class SpendingCategory(BaseModel):
    category: str = Field(..., description="Expense category name")
    amount: float = Field(..., description="Amount spent in this category")
    percentage: Optional[float] = Field(None, description="Percentage of total spending")

class SpendingRecommendation(BaseModel):
    category: str = Field(..., description="Category for recommendation")
    recommendation: str = Field(..., description="Recommendation details")
    potential_savings: Optional[float] = Field(None, description="Estimated monthly savings")

class BudgetAnalysis(BaseModel):
    total_expenses: float = Field(..., description="Total monthly expenses")
    monthly_income: Optional[float] = Field(None, description="Monthly income")
    spending_categories: List[SpendingCategory] = Field(..., description="Breakdown of spending by category")
    recommendations: List[SpendingRecommendation] = Field(..., description="Spending recommendations")

class EmergencyFund(BaseModel):
    recommended_amount: float = Field(..., description="Recommended emergency fund size")
    current_amount: Optional[float] = Field(None, description="Current emergency fund (if any)")
    current_status: str = Field(..., description="Status assessment of emergency fund")

class SavingsRecommendation(BaseModel):
    category: str = Field(..., description="Savings category")
    amount: float = Field(..., description="Recommended monthly amount")
    rationale: Optional[str] = Field(None, description="Explanation for this recommendation")

class AutomationTechnique(BaseModel):
    name: str = Field(..., description="Name of automation technique")
    description: str = Field(..., description="Details of how to implement")

class SavingsStrategy(BaseModel):
    emergency_fund: EmergencyFund = Field(..., description="Emergency fund recommendation")
    recommendations: List[SavingsRecommendation] = Field(..., description="Savings allocation recommendations")
    automation_techniques: Optional[List[AutomationTechnique]] = Field(None, description="Automation techniques to help save")

class Debt(BaseModel):
    name: str = Field(..., description="Name of debt")
    amount: float = Field(..., description="Current balance")
    interest_rate: float = Field(..., description="Annual interest rate (%)")
    min_payment: Optional[float] = Field(None, description="Minimum monthly payment")

class PayoffPlan(BaseModel):
    total_interest: float = Field(..., description="Total interest paid")
    months_to_payoff: int = Field(..., description="Months until debt-free")
    monthly_payment: Optional[float] = Field(None, description="Recommended monthly payment")

class PayoffPlans(BaseModel):
    avalanche: PayoffPlan = Field(..., description="Highest interest first method")
    snowball: PayoffPlan = Field(..., description="Smallest balance first method")

class DebtRecommendation(BaseModel):
    title: str = Field(..., description="Title of recommendation")
    description: str = Field(..., description="Details of recommendation")
    impact: Optional[str] = Field(None, description="Expected impact of this action")

class DebtReduction(BaseModel):
    total_debt: float = Field(..., description="Total debt amount")
    debts: List[Debt] = Field(..., description="List of all debts")
    payoff_plans: PayoffPlans = Field(..., description="Debt payoff strategies")
    recommendations: Optional[List[DebtRecommendation]] = Field(None, description="Recommendations for debt reduction")


def parse_json_safely(data: str, default_value: Any = None) -> Any:
    """Safely parse JSON data with error handling"""
    try:
        return json.loads(data) if isinstance(data, str) else data
    except json.JSONDecodeError:
        return default_value

class FinanceAdvisorSystem:
    def __init__(self, gemini_api_key: str):
        if not gemini_api_key:
            raise ValueError("Gemini API key is required.")
        genai.configure(api_key=gemini_api_key)
        
        self.session_service = InMemorySessionService()
        self._define_agents()
        
        self.runner = Runner(
            agent=self.coordinator_agent,
            app_name=APP_NAME,
            session_service=self.session_service
        )

    def _define_agents(self):
        self.budget_analysis_agent = LlmAgent(
            name="BudgetAnalysisAgent", model="gemini-1.5-flash",
            description="Analyzes financial data to categorize spending patterns and recommend budget improvements",
            instruction="""You are a Budget Analysis Agent... (Full instruction as before)""",
            output_schema=BudgetAnalysis, output_key="budget_analysis"
        )
        self.savings_strategy_agent = LlmAgent(
            name="SavingsStrategyAgent", model="gemini-1.5-flash",
            description="Recommends optimal savings strategies based on income, expenses, and financial goals",
            instruction="""You are a Savings Strategy Agent... (Full instruction as before)""",
            output_schema=SavingsStrategy, output_key="savings_strategy"
        )
        self.debt_reduction_agent = LlmAgent(
            name="DebtReductionAgent", model="gemini-1.5-flash",
            description="Creates optimized debt payoff plans to minimize interest paid and time to debt freedom",
            instruction="""You are a Debt Reduction Agent... (Full instruction as before)""",
            output_schema=DebtReduction, output_key="debt_reduction"
        )
        self.coordinator_agent = SequentialAgent(
            name="FinanceCoordinatorAgent",
            description="Coordinates specialized finance agents to provide comprehensive financial advice",
            sub_agents=[
                self.budget_analysis_agent, self.savings_strategy_agent, self.debt_reduction_agent
            ]
        )

    async def analyze_finances(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        session_id = f"finance_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            initial_state = {
                "monthly_income": financial_data.get("monthly_income", 0),
                "dependants": financial_data.get("dependants", 0),
                "transactions": financial_data.get("transactions", []),
                "manual_expenses": financial_data.get("manual_expenses", {}),
                "debts": financial_data.get("debts", [])
            }
            
            session = self.session_service.create_session(
                app_name=APP_NAME, user_id=USER_ID, session_id=session_id, state=initial_state
            )
            
            if session.state.get("transactions"):
                self._preprocess_transactions(session)
            
            if session.state.get("manual_expenses"):
                self._preprocess_manual_expenses(session)
            
            default_results = self._create_default_results(financial_data)
            
            user_content = types.Content(role='user', parts=[types.Part(text=json.dumps(financial_data))])
            
            async for event in self.runner.run_async(user_id=USER_ID, session_id=session_id, new_message=user_content):
                if event.is_final_response() and event.author == self.coordinator_agent.name:
                    break
            
            updated_session = self.session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
            
            results = {}
            for key in ["budget_analysis", "savings_strategy", "debt_reduction"]:
                value = updated_session.state.get(key)
                results[key] = parse_json_safely(value, default_results[key]) if value else default_results[key]
            
            return {"success": True, "analysis": results}
            
        except Exception as e:
            logger.exception(f"Error during finance analysis: {str(e)}")
            return {"success": False, "error": str(e)}
        finally:
            self.session_service.delete_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
    
    def _preprocess_transactions(self, session):
        transactions = session.state.get("transactions", [])
        if not transactions: return
        df = pd.DataFrame(transactions)
        if 'Date' in df.columns: df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
        if 'Category' in df.columns and 'Amount' in df.columns:
            session.state["category_spending"] = df.groupby('Category')['Amount'].sum().to_dict()
            session.state["total_spending"] = df['Amount'].sum()
    
    def _preprocess_manual_expenses(self, session):
        manual_expenses = session.state.get("manual_expenses", {})
        if not manual_expenses or manual_expenses is None: return
        session.state.update({
            "total_manual_spending": sum(manual_expenses.values()),
            "manual_category_spending": manual_expenses
        })

    def _create_default_results(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        monthly_income = financial_data.get("monthly_income", 0)
        expenses = financial_data.get("manual_expenses", {}) or {}
        if not expenses and financial_data.get("transactions"):
            expenses = {t.get("Category", "Uncategorized"): expenses.get(t.get("Category", "Uncategorized"), 0) + t.get("Amount", 0) for t in financial_data["transactions"]}
        total_expenses = sum(expenses.values())
        return {
            "budget_analysis": BudgetAnalysis(total_expenses=total_expenses, monthly_income=monthly_income, spending_categories=[], recommendations=[]).model_dump(),
            "savings_strategy": SavingsStrategy(emergency_fund=EmergencyFund(recommended_amount=total_expenses*6, current_status=""), recommendations=[]).model_dump(),
            "debt_reduction": DebtReduction(total_debt=0, debts=[], payoff_plans=PayoffPlans(avalanche=PayoffPlan(total_interest=0, months_to_payoff=0), snowball=PayoffPlan(total_interest=0, months_to_payoff=0))).model_dump(),
        }

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    
    async def main():
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("GOOGLE_API_KEY not found in .env file.")
            return

        service = FinanceAdvisorSystem(gemini_api_key=api_key)
        
        sample_data = {
            "monthly_income": 5000,
            "dependants": 1,
            "manual_expenses": {
                "Housing": 1500, "Food": 600, "Transportation": 300, 
                "Entertainment": 200, "Utilities": 150
            },
            "debts": [
                {"name": "Credit Card", "amount": 5000, "interest_rate": 18.9, "min_payment": 100},
                {"name": "Student Loan", "amount": 20000, "interest_rate": 5.8, "min_payment": 250}
            ]
        }
        
        results = await service.analyze_finances(sample_data)
        
        if results['success']:
            print(json.dumps(results['analysis'], indent=2))
        else:
            print(f"Error: {results['error']}")

    asyncio.run(main())