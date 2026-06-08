import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Enum, String, Text, ForeignKey, func, Index, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class KnowledgeSourceType(str, enum.Enum):
    YC = "yc"
    PRODUCT_HUNT = "product_hunt"
    STARTUP_GENOME = "startup_genome"
    TECHCRUNCH = "techcrunch"
    CRUNCHBASE = "crunchbase"
    VC_BLOGS = "vc_blogs"
    RESEARCH_PAPERS = "research_papers"
    GITHUB_TRENDS = "github_trends"
    BUSINESS_FRAMEWORKS = "business_frameworks"
    CUSTOM = "custom"


class KnowledgeSource(Base):
    __tablename__ = "knowledge_sources"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    source_type: Mapped[KnowledgeSourceType] = mapped_column(Enum(KnowledgeSourceType), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    knowledge_metadata: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    embedding_model: Mapped[str] = mapped_column(String(100), nullable=False)
    chunk_count: Mapped[int] = mapped_column(default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    last_ingested_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index("ix_knowledge_sources_type_active", "source_type", "is_active"),
        UniqueConstraint("source_type", "url", name="uq_knowledge_source_url"),
    )

    def __repr__(self) -> str:
        return f"<KnowledgeSource(id={self.id}, type='{self.source_type}', title='{self.title[:50]}')>"


class RetrievalCache(Base):
    __tablename__ = "retrieval_cache"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    query_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    query_text: Mapped[str] = mapped_column(Text, nullable=False)
    agent_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    results: Mapped[dict] = mapped_column(JSON, nullable=False)
    hit_count: Mapped[int] = mapped_column(default=0, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("ix_retrieval_cache_agent_expires", "agent_type", "expires_at"),
    )

    def __repr__(self) -> str:
        return f"<RetrievalCache(id={self.id}, query_hash='{self.query_hash[:16]}', hits={self.hit_count})>"