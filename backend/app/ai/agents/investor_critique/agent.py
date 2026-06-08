from app.ai.agents.base import BaseAgent
from app.ai.memory.shared_memory import SharedMemory


SYSTEM_PROMPT = """You are a Venture Capitalist evaluating startup investment opportunities.
Be critical, thorough, and provide actionable feedback.
Think like a top-tier VC partner evaluating a deal.
Output in JSON format.

Output JSON format:
{
    "readiness_score": <float 0-100>,
    "feedback": {
        "overall_assessment": "<summary>",
        "strengths": ["<strength 1>"],
        "weaknesses": ["<weakness 1>"],
        "red_flags": ["<red flag 1>"],
        "recommendations": ["<recommendation 1>"],
        "investment_thesis": "<thesis statement>"
    },
    "risk_matrix": {
        "market_risk": {"level": "<high/medium/low>", "description": "<detail>"},
        "technical_risk": {"level": "<high/medium/low>", "description": "<detail>"},
        "team_risk": {"level": "<high/medium/low>", "description": "<detail>"},
        "financial_risk": {"level": "<high/medium/low>", "description": "<detail>"},
        "competitive_risk": {"level": "<high/medium/low>", "description": "<detail>"}
    },
    "funding_recommendation": {
        "recommended_round": "<seed/series_a/etc>",
        "recommended_amount": "<amount>",
        "valuation_range": "<range>",
        "suggested_investors": ["<investor type 1>"]
    },
    "due_diligence_questions": ["<question 1>"]
}"""


class InvestorCritiqueAgent(BaseAgent):
    def evaluate(self, memory: SharedMemory, context: dict) -> dict:
        user_prompt = f"""
Startup: {context.get('name', 'Unknown')}
Industry: {context.get('industry', 'Unknown')}
Problem: {context.get('problem_statement', 'N/A')}
Solution: {context.get('solution', 'N/A')}
Target: {context.get('target_audience', 'N/A')}
Business Model: {context.get('business_model', 'N/A')}
Country: {context.get('country', 'N/A')}
Strategy: {context.get('strategy', {})}
Market Data: {context.get('market_data', {})}

Evaluate this startup from a VC perspective. Assess readiness, risks, red flags, and provide funding recommendations."""
        result = self._call_llm(SYSTEM_PROMPT, user_prompt, temperature=0.3)
        return self._parse_json(result)
