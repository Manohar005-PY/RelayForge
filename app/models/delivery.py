from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.delivery_attempt import DeliveryAttempt
    from app.models.endpoint import Endpoint
    from app.models.event import Event


class Delivery(Base):
    __tablename__ = "deliveries"

    delivery_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, 
        primary_key=True, 
        default=uuid.uuid4
    )
    event_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, 
        ForeignKey("events.event_id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    endpoint_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, 
        ForeignKey("endpoints.endpoint_id", 
        ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    status: Mapped[str] = mapped_column(
        String(32), 
        nullable=False, 
        default="pending"
    )
    attempt_count: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        default=0, 
        server_default="0"
    )
    max_attempts: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        default=5, 
        server_default="5"
    )
    last_attempt_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    next_attempt_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    delivered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    lease_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    last_error: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now(), 
        onupdate=func.now()
    )

    event: Mapped[Event] = relationship(back_populates="deliveries")
    endpoint: Mapped[Endpoint] = relationship(back_populates="deliveries")
    attempts: Mapped[list[DeliveryAttempt]] = relationship(
        back_populates="delivery", cascade="all, delete-orphan"
    )
