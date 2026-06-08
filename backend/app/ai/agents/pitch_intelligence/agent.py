from app.ai.agents.base import BaseAgent
from app.ai.memory.shared_memory import SharedMemory


SYSTEM_PROMPT = """You are a Pitch Coach specializing in crafting investor presentations.
Create compelling pitch narratives that tell a story and convince investors.
Output in JSON format.

Output JSON format:
{
    "pitch": {
        "executive_summary": "<2-3 sentence summary>",
        "problem": "<problem statement>",
        "solution": "<solution description>",
        "market_opportunity": "<market sizing>",
        "why_now": "<timing rationale>",
        "product": "<product description>",
        "traction": "<traction highlights>",
        "business_model": "<model explanation>",
        "competition": "<competitive landscape>",
        "team": "<team highlights>",
        "financials": "<key financial projections>",
        "ask": "<funding ask and use of funds>"
    },
    "slide_deck": [
        {"slide": 1, "title": "Title Slide", "content": "<content>", "notes": "<speaker notes>"},
        {"slide": 2, "title": "Problem", "content": "<content>", "notes": "<speaker notes>"},
        {"slide": 3, "title": "Solution", "content": "<content>", "notes": "<speaker notes>"},
        {"slide": 4, "title": "Market Opportunity", "content": "<content>", "notes": "<speaker notes>"},
        {"slide": 5, "title": "Why Now", "content": "<content>", "notes": "<speaker notes>"},
        {"slide": 6, "title": "Product", "content": "<content>", "notes": "<speaker notes>"},
        {"slide": 7, "title": "Traction", "content": "<content>", "notes": "<speaker notes>"},
        {"slide": 8, "title": "Business Model", "content": "<content>", "notes": "<speaker notes>"},
        {"slide": 9, "title": "Competition", "content": "<content>", "notes": "<speaker notes>"},
        {"slide": 10, "title": "Team", "content": "<content>", "notes": "<speaker notes>"},
        {"slide": 11, "title": "Financial Projections", "content": "<content>", "notes": "<speaker notes>"},
        {"slide": 12, "title": "Investment Ask", "content": "<content>", "notes": "<speaker notes>"}
    ],
    "investor_narrative": "<complete pitch narrative for speaking>"
}"""


class PitchIntelligenceAgent(BaseAgent):
    def generate_pitch(self, memory: SharedMemory, context: dict) -> dict:
        user_prompt = f"""
Startup: {context.get('name', 'Unknown')}
Industry: {context.get('industry', 'Unknown')}
Problem: {context.get('problem_statement', 'N/A')}
Solution: {context.get('solution', 'N/A')}
Target: {context.get('target_audience', 'N/A')}
Business Model: {context.get('business_model', 'N/A')}
Strategy: {context.get('strategy', {})}
Investor Feedback: {context.get('investor_feedback', {})}

Generate a compelling investor pitch deck, executive summary, and narrative."""
        result = self._call_llm(SYSTEM_PROMPT, user_prompt, temperature=0.8)
        return self._parse_json(result)
