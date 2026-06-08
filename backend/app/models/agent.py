import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Enum, String, Text, ForeignKey, func, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class AgentType(str, enum.Enum):
    STARTUP_INTELLIGENCE = "startup_intelligence"
    BUSINESS_STRATEGY = "business_strategy"
    INVESTOR_CRITIQUE = "investor_critique"
    PITCH_INTELLIGENCE = "pitch_intelligence"


class AgentStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    SKIPPED = "skipped"


class AgentOutput(Base):
    __tablename__ = "agent_outputs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_type: Mapped[AgentType] = mapped_column(Enum(AgentType), nullable=False, index=True)
    status: Mapped[AgentStatus] = mapped_column(Enum(AgentStatus), default=AgentStatus.PENDING, nullable=False, index=True)
    input_data: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    output_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    execution_time_ms: Mapped[Optional[int]] = mapped_column(nullable=True)
    token_usage: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    cost_usd: Mapped[Optional[float]] = mapped_column(nullable=True)
    retry_count: Mapped[int] = mapped_column(default=0, nullable=False)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    project = relationship("Project", back_populates="agent_outputs", lazy="selectin")

    __table_args__ = (
        Index("ix_agent_outputs_project_agent", "project_id", "agent_type"),
        Index("ix_agent_outputs_status", "status"),
    )

    def __repr__(self) -> str:
        return f"<AgentOutput(id={self.id}, project_id={self.project_id}, agent_type='{self.agent_type}', status='{self.status}')>"