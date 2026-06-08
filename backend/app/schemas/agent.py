from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class RunAgentRequest(BaseModel):
    project_id: int
    agent_types: list[str] = Field(default_factory=lambda: [
        "startup_intelligence",
        "business_strategy",
        "investor_critique",
        "pitch_intelligence",
    ])


class AgentOutputResponse(BaseModel):
    id: int
    project_id: int
    agent_type: str
    status: str
    input_data: dict
    output_data: Optional[dict] = None
    error_message: Optional[str] = None
    execution_time_ms: Optional[int] = None
    token_usage: Optional[dict] = None
    cost_usd: Optional[float] = None
    retry_count: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class AgentStatusResponse(BaseModel):
    project_id: int
    agents: list[AgentOutputResponse]
    overall_status: str
    progress_percentage: float
