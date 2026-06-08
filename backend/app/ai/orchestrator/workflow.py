import time
import json
import logging
from typing import Any, Optional
from app.ai.memory.shared_memory import SharedMemory, MemoryType
from app.ai.agents.startup_intelligence.agent import StartupIntelligenceAgent
from app.ai.agents.business_strategy.agent import BusinessStrategyAgent
from app.ai.agents.investor_critique.agent import InvestorCritiqueAgent
from app.ai.agents.pitch_intelligence.agent import PitchIntelligenceAgent

logger = logging.getLogger(__name__)


class AgentOpsWorkflow:
    def __init__(self):
        self.startup_agent = StartupIntelligenceAgent()
        self.strategy_agent = BusinessStrategyAgent()
        self.investor_agent = InvestorCritiqueAgent()
        self.pitch_agent = PitchIntelligenceAgent()

    def run(
        self,
        project_id: int,
        project_data: dict,
        agent_types: list[str],
    ) -> dict:
        memory = SharedMemory(project_id=project_id)
        memory.set("startup_idea", project_data, MemoryType.STARTUP_IDEA)

        agent_outputs = []
        scores = {}

        workflow_steps = {
            "startup_intelligence": self._run_startup_intelligence,
            "business_strategy": self._run_business_strategy,
            "investor_critique": self._run_investor_critique,
            "pitch_intelligence": self._run_pitch_intelligence,
        }

        for agent_type in agent_types:
            if agent_type in workflow_steps:
                step_func = workflow_steps[agent_type]
                start_time = time.time()
                try:
                    result = step_func(memory, project_data)
                    execution_time = int((time.time() - start_time) * 1000)
                    result["execution_time_ms"] = execution_time
                    agent_outputs.append(result)
                    logger.info(f"Agent {agent_type} completed in {execution_time}ms")
                except Exception as e:
                    logger.error(f"Agent {agent_type} failed: {e}")
                    agent_outputs.append({
                        "agent_type": agent_type,
                        "status": "failed",
                        "error": str(e),
                        "execution_time_ms": int((time.time() - start_time) * 1000),
                    })

        scores = memory.get_by_type(MemoryType.SCORES)

        self._run_critique_loop(memory, project_data)

        return {
            "agent_outputs": agent_outputs,
            "viability_score": scores.get("viability_score"),
            "investor_readiness_score": scores.get("investor_readiness_score"),
            "shared_memory": memory.to_dict(),
        }

    def _run_startup_intelligence(self, memory: SharedMemory, project_data: dict) -> dict:
        result = self.startup_agent.analyze(memory, project_data)
        memory.set("market_data", result.get("market_data", {}), MemoryType.MARKET_DATA, source_agent="startup_intelligence")
        memory.set("competitor_data", result.get("competitor_data", {}), MemoryType.COMPETITOR_DATA, source_agent="startup_intelligence")
        memory.set("viability_score", result.get("viability_score"), MemoryType.SCORES, source_agent="startup_intelligence")
        memory.set("swot_analysis", result.get("swot_analysis", {}), MemoryType.AGENT_OUTPUT, source_agent="startup_intelligence")
        return {
            "agent_type": "startup_intelligence",
            "status": "completed",
            "output": result,
        }

    def _run_business_strategy(self, memory: SharedMemory, project_data: dict) -> dict:
        startup_data = memory.get_latest("market_data") or {}
        competitor_data = memory.get_latest("competitor_data") or {}
        context = {**project_data, "market_data": startup_data, "competitor_data": competitor_data}
        result = self.strategy_agent.generate(memory, context)
        memory.set("business_strategy", result.get("strategy", {}), MemoryType.BUSINESS_STRATEGY, source_agent="business_strategy")
        memory.set("lean_canvas", result.get("lean_canvas", {}), MemoryType.AGENT_OUTPUT, source_agent="business_strategy")
        return {
            "agent_type": "business_strategy",
            "status": "completed",
            "output": result,
        }

    def _run_investor_critique(self, memory: SharedMemory, project_data: dict) -> dict:
        strategy = memory.get_latest("business_strategy") or {}
        market_data = memory.get_latest("market_data") or {}
        context = {**project_data, "strategy": strategy, "market_data": market_data}
        result = self.investor_agent.evaluate(memory, context)
        memory.set("investor_feedback", result.get("feedback", {}), MemoryType.INVESTOR_FEEDBACK, source_agent="investor_critique")
        memory.set("investor_readiness_score", result.get("readiness_score"), MemoryType.SCORES, source_agent="investor_critique")
        memory.set("risk_matrix", result.get("risk_matrix", {}), MemoryType.AGENT_OUTPUT, source_agent="investor_critique")
        return {
            "agent_type": "investor_critique",
            "status": "completed",
            "output": result,
        }

    def _run_pitch_intelligence(self, memory: SharedMemory, project_data: dict) -> dict:
        strategy = memory.get_latest("business_strategy") or {}
        feedback = memory.get_latest("investor_feedback") or {}
        context = {**project_data, "strategy": strategy, "investor_feedback": feedback}
        result = self.pitch_agent.generate_pitch(memory, context)
        memory.set("pitch_data", result.get("pitch", {}), MemoryType.PITCH_DATA, source_agent="pitch_intelligence")
        return {
            "agent_type": "pitch_intelligence",
            "status": "completed",
            "output": result,
        }

    def _run_critique_loop(self, memory: SharedMemory, project_data: dict) -> None:
        investor_feedback = memory.get_latest("investor_feedback") or {}
        red_flags = investor_feedback.get("red_flags", [])
        strategy = memory.get_latest("business_strategy") or {}

        if red_flags and strategy:
            revised_strategy = self.strategy_agent.revise_strategy(
                memory,
                {**project_data, "strategy": strategy, "investor_feedback": investor_feedback},
            )
            memory.set("business_strategy", revised_strategy, MemoryType.BUSINESS_STRATEGY, source_agent="critique_loop")
            memory.set("strategy_revision", {
                "original": strategy,
                "revised": revised_strategy,
                "red_flags_addressed": red_flags,
            }, MemoryType.AGENT_OUTPUT, source_agent="critique_loop")
