from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.delivery import Delivery


class DeliveryAttempt(Base):
    __tablename__ = "delivery_attempts"

    attempt_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, 
        primary_key=True, 
        default=uuid.uuid4
    )
    delivery_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, 
        ForeignKey("deliveries.delivery_id", 
        ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    attempt_number: Mapped[int] = mapped_column(
        Integer, 
        nullable=False
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    http_status: Mapped[int | None] = mapped_column(Integer)

    duration_ms: Mapped[int | None] = mapped_column(Integer)

    response_summary: Mapped[str | None] = mapped_column(Text)

    error_code: Mapped[str | None] = mapped_column(String(100))
    
    error_message: Mapped[str | None] = mapped_column(Text)

    delivery: Mapped[Delivery] = relationship(back_populates="attempts")
