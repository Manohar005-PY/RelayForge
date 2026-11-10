from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, ForeignKey, JSON, String, Uuid, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.delivery import Delivery
    from app.models.organization import Organization
    from app.models.outbox import Outbox


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (
        UniqueConstraint("org_id", "idempotency_key", name="uq_events_org_idempotency_key"),
    )

    event_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("organizations.org_id", ondelete="CASCADE"), nullable=False, index=True
    )
    event_type: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    payload: Mapped[Any] = mapped_column(JSON, nullable=False)
    idempotency_key: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    organization: Mapped[Organization] = relationship(back_populates="events")
    deliveries: Mapped[list[Delivery]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )
    outbox_entry: Mapped[Outbox | None] = relationship(
        back_populates="event", cascade="all, delete-orphan", uselist=False
    )
