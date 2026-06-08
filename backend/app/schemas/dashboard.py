from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DashboardOverviewResponse(BaseModel):
    total_projects: int
    active_projects: int
    completed_projects: int
    total_reports: int
    avg_viability_score: Optional[float] = None
    avg_investor_readiness: Optional[float] = None
    recent_projects: list[dict]
    recent_activity: list[dict]


class AnalyticsResponse(BaseModel):
    projects_by_status: dict[str, int]
    projects_by_industry: dict[str, int]
    projects_by_business_model: dict[str, int]
    agent_execution_times: dict[str, float]
    agent_success_rates: dict[str, float]
    scores_over_time: list[dict]
    usage_stats: dict
