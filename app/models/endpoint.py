from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.delivery import Delivery
    from app.models.event_subscription import EventSubscription
    from app.models.organization import Organization


class Endpoint(Base):
    __tablename__ = "endpoints"

    endpoint_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, 
        primary_key=True, 
        default=uuid.uuid4
    )
    org_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, 
        ForeignKey("organizations.org_id", ondelete="CASCADE"), nullable=False, 
        index=True
    )
    endpoint_url: Mapped[str] = mapped_column(
        Text, 
        nullable=False
        )
    signing_secret: Mapped[str] = mapped_column(
        String(255), 
        nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(32), 
        nullable=False, 
        default="active"
    )
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

    organization: Mapped[Organization] = relationship(back_populates="endpoints")

    subscriptions: Mapped[list[EventSubscription]] = relationship(
        back_populates="endpoint", 
        cascade="all, delete-orphan"
    )
    deliveries: Mapped[list[Delivery]] = relationship(back_populates="endpoint")
