from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.organization import Organization


class ApiKey(Base):
    __tablename__ = "api_keys"

    api_key_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, 
        primary_key=True, 
        default=uuid.uuid4
    )

    org_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, 
        ForeignKey("organizations.org_id", 
        ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(255), 
        nullable=False
    )
    key_hash: Mapped[str] = mapped_column(
        String(255), 
        nullable=False, 
        unique=True
    )
    last_used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )

    organization: Mapped[Organization] = relationship(back_populates="api_keys")
