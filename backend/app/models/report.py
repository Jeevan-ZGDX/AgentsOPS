import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Enum, String, Text, ForeignKey, func, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class ReportType(str, enum.Enum):
    STARTUP = "startup"
    BUSINESS_STRATEGY = "business_strategy"
    INVESTOR = "investor"
    PITCH = "pitch"
    UNIFIED = "unified"


class ReportFormat(str, enum.Enum):
    PDF = "pdf"
    PPT = "ppt"
    HTML = "html"
    MARKDOWN = "markdown"
    JSON = "json"


class ReportStatus(str, enum.Enum):
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    report_type: Mapped[ReportType] = mapped_column(Enum(ReportType), nullable=False, index=True)
    format: Mapped[ReportFormat] = mapped_column(Enum(ReportFormat), nullable=False)
    status: Mapped[ReportStatus] = mapped_column(Enum(ReportStatus), default=ReportStatus.GENERATING, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    file_size_bytes: Mapped[Optional[int]] = mapped_column(nullable=True)
    generation_time_ms: Mapped[Optional[int]] = mapped_column(nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    project = relationship("Project", back_populates="reports", lazy="selectin")

    __table_args__ = (
        Index("ix_reports_project_type", "project_id", "report_type"),
        Index("ix_reports_status", "status"),
    )

    def __repr__(self) -> str:
        return f"<Report(id={self.id}, project_id={self.project_id}, type='{self.report_type}', format='{self.format}')>"