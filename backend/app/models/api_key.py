from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, String, Text, ForeignKey, func, Index, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class APIKey(Base):
    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    key_hash: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    key_prefix: Mapped[str] = mapped_column(String(10), nullable=False)
    last_five: Mapped[str] = mapped_column(String(5), nullable=False)
    permissions: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="api_keys", lazy="selectin")

    __table_args__ = (
        Index("ix_api_keys_user_active", "user_id", "is_active"),
    )

    def __repr__(self) -> str:
        return f"<APIKey(id={self.id}, user_id={self.user_id}, prefix='{self.key_prefix}')>"
