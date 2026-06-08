from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CreateProjectRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    industry: str = Field(min_length=1, max_length=100)
    problem_statement: str = Field(min_length=10)
    solution: str = Field(min_length=10)
    target_audience: str = Field(min_length=10)
    business_model: str
    country: str = Field(max_length=100)


class UpdateProjectRequest(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    problem_statement: Optional[str] = None
    solution: Optional[str] = None
    target_audience: Optional[str] = None
    business_model: Optional[str] = None
    country: Optional[str] = None
    status: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    owner_id: int
    name: str
    industry: str
    problem_statement: str
    solution: str
    target_audience: str
    business_model: str
    country: str
    status: str
    viability_score: Optional[float] = None
    investor_readiness_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    items: list[ProjectResponse]
    total: int
    page: int
    page_size: int


class ProjectStateResponse(BaseModel):
    id: int
    project_id: int
    version: int
    description: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
