import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import DateTime, Enum, String, Text, ForeignKey, func, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class ProjectStatus(str, enum.Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


class BusinessModelType(str, enum.Enum):
    B2B_SAAS = "b2b_saas"
    B2C_SAAS = "b2c_saas"
    MARKETPLACE = "marketplace"
    E_COMMERCE = "e_commerce"
    SUBSCRIPTION = "subscription"
    FREEMIUM = "freemium"
    ADVERTISING = "advertising"
    LICENSING = "licensing"
    CONSULTING = "consulting"
    HYBRID = "hybrid"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    industry: Mapped[str] = mapped_column(String(100), nullable=False)
    problem_statement: Mapped[str] = mapped_column(Text, nullable=False)
    solution: Mapped[str] = mapped_column(Text, nullable=False)
    target_audience: Mapped[str] = mapped_column(Text, nullable=False)
    business_model: Mapped[BusinessModelType] = mapped_column(Enum(BusinessModelType), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[ProjectStatus] = mapped_column(Enum(ProjectStatus), default=ProjectStatus.DRAFT, nullable=False, index=True)
    viability_score: Mapped[Optional[float]] = mapped_column(nullable=True)
    investor_readiness_score: Mapped[Optional[float]] = mapped_column(nullable=True)
    project_metadata: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    owner = relationship("User", back_populates="projects", lazy="selectin")
    states = relationship("ProjectState", back_populates="project", lazy="selectin", order_by="ProjectState.created_at.desc()")
    agent_outputs = relationship("AgentOutput", back_populates="project", lazy="selectin")
    reports = relationship("Report", back_populates="project", lazy="selectin")
    audit_logs = relationship("AuditLog", back_populates="project", lazy="selectin")

    __table_args__ = (
        Index("ix_projects_owner_status", "owner_id", "status"),
        Index("ix_projects_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status}')>"


class ProjectState(Base):
    __tablename__ = "project_states"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    state_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    version: Mapped[int] = mapped_column(default=1, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    project = relationship("Project", back_populates="states", lazy="selectin")

    __table_args__ = (
        Index("ix_project_states_project_version", "project_id", "version"),
    )

    def __repr__(self) -> str:
        return f"<ProjectState(id={self.id}, project_id={self.project_id}, version={self.version})>"