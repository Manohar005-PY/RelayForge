from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Uuid, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.endpoint import Endpoint


class EventSubscription(Base):
    __tablename__ = "event_subscriptions"
    __table_args__ = (
        UniqueConstraint("endpoint_id", "event_type", name="uq_event_subscriptions_endpoint_event"),
    )

    subscription_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, 
        primary_key=True, 
        default=uuid.uuid4
    )
    endpoint_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("endpoints.endpoint_id", ondelete="CASCADE"), nullable=False, 
        index=True
    )
    event_type: Mapped[str] = mapped_column(
        String(255), 
        nullable=False
        )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )

    endpoint: Mapped[Endpoint] = relationship(back_populates="subscriptions")
