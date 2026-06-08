from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ReportResponse(BaseModel):
    id: int
    project_id: int
    report_type: str
    format: str
    status: str
    title: str
    content: Optional[dict] = None
    file_path: Optional[str] = None
    file_size_bytes: Optional[int] = None
    generation_time_ms: Optional[int] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ReportListResponse(BaseModel):
    items: list[ReportResponse]
    total: int


class GenerateReportRequest(BaseModel):
    project_id: int
    report_type: str = "unified"
    formats: list[str] = ["pdf"]


class ExportRequest(BaseModel):
    project_id: int
    report_type: str = "unified"
    format: str = "pdf"
