from app.ai.agents.base import BaseAgent
from app.ai.memory.shared_memory import SharedMemory


SYSTEM_PROMPT = """You are a Startup Intelligence Analyst specializing in evaluating early-stage startup ideas.
Analyze the startup idea and provide structured output in JSON format.
Evaluate the viability, market potential, competitive landscape, and risks.

Output JSON format:
{
    "viability_score": <float 0-100>,
    "market_data": {
        "market_size": "<estimated TAM>",
        "market_growth": "<growth rate and trend>",
        "market_trends": ["<trend 1>", "<trend 2>"],
        "target_segments": ["<segment 1>", "<segment 2>"],
        "adoption_drivers": ["<driver 1>", "<driver 2>"],
        "market_risks": ["<risk 1>", "<risk 2>"]
    },
    "competitor_data": {
        "direct_competitors": [
            {"name": "<name>", "strength": "<strength>", "weakness": "<weakness>"}
        ],
        "indirect_competitors": ["<name 1>", "<name 2>"],
        "competitive_advantage": "<moat description>",
        "market_positioning": "<positioning strategy>"
    },
    "swot_analysis": {
        "strengths": ["<strength 1>"],
        "weaknesses": ["<weakness 1>"],
        "opportunities": ["<opportunity 1>"],
        "threats": ["<threat 1>"]
    },
    "key_assumptions": ["<assumption 1>"],
    "validation_required": ["<validation 1>"]
}"""


class StartupIntelligenceAgent(BaseAgent):
    def analyze(self, memory: SharedMemory, project_data: dict) -> dict:
        user_prompt = f"""
Startup Name: {project_data.get('name', 'Unknown')}
Industry: {project_data.get('industry', 'Unknown')}
Problem: {project_data.get('problem_statement', 'N/A')}
Solution: {project_data.get('solution', 'N/A')}
Target Audience: {project_data.get('target_audience', 'N/A')}
Business Model: {project_data.get('business_model', 'N/A')}
Country: {project_data.get('country', 'N/A')}

Analyze this startup idea comprehensively and provide scores, market data, competitor analysis, and SWOT."""
        result = self._call_llm(SYSTEM_PROMPT, user_prompt)
        parsed = self._parse_json(result)
        return parsed
