from app.ai.agents.base import BaseAgent
from app.ai.memory.shared_memory import SharedMemory


SYSTEM_PROMPT = """You are a Business Strategy Consultant specializing in early-stage startups.
Generate comprehensive business strategy based on startup idea and market analysis.
Output in JSON format.

Output JSON format:
{
    "strategy": {
        "business_model": "<business model description>",
        "value_proposition": "<unique value proposition>",
        "revenue_streams": [
            {"stream": "<stream name>", "model": "<pricing model>", "projected_revenue": "<amount>"}
        ],
        "pricing_strategy": "<pricing approach>",
        "go_to_market": {
            "channels": ["<channel 1>"],
            "customer_acquisition": "<acquisition strategy>",
            "partnerships": ["<partner 1>"],
            "launch_strategy": "<launch plan>"
        },
        "mvp_roadmap": {
            "phase_1": {"duration": "<duration>", "features": ["<feature>"]},
            "phase_2": {"duration": "<duration>", "features": ["<feature>"]},
            "phase_3": {"duration": "<duration>", "features": ["<feature>"]}
        },
        "key_metrics": ["<kpi 1>", "<kpi 2>"]
    },
    "lean_canvas": {
        "problem": "<top 3 problems>",
        "solution": "<solution>",
        "key_metrics": "<key metrics>",
        "unique_value_proposition": "<UVP>",
        "unfair_advantage": "<advantage>",
        "channels": "<channels>",
        "customer_segments": "<segments>",
        "cost_structure": "<costs>",
        "revenue_streams": "<revenues>"
    }
}"""


class BusinessStrategyAgent(BaseAgent):
    def generate(self, memory: SharedMemory, context: dict) -> dict:
        project_data = {k: v for k, v in context.items() if k != "market_data" and k != "competitor_data"}
        user_prompt = f"""
Startup: {project_data.get('name', 'Unknown')}
Industry: {project_data.get('industry', 'Unknown')}
Problem: {project_data.get('problem_statement', 'N/A')}
Solution: {project_data.get('solution', 'N/A')}
Target: {project_data.get('target_audience', 'N/A')}
Business Model: {project_data.get('business_model', 'N/A')}
Market Data: {context.get('market_data', {})}
Competitors: {context.get('competitor_data', {})}

Generate comprehensive business strategy including business model, pricing, GTM, and MVP roadmap."""
        result = self._call_llm(SYSTEM_PROMPT, user_prompt)
        return self._parse_json(result)

    def revise_strategy(self, memory: SharedMemory, context: dict) -> dict:
        user_prompt = f"""
Original Strategy: {context.get('strategy', {})}
Investor Feedback: {context.get('investor_feedback', {})}
Red Flags to Address: {context.get('investor_feedback', {}).get('red_flags', [])}

Revise the business strategy to address all investor concerns and red flags.
Maintain the successful elements while improving weak areas."""
        result = self._call_llm(SYSTEM_PROMPT, user_prompt, temperature=0.5)
        return self._parse_json(result)
