from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.api_key import ApiKey
    from app.models.endpoint import Endpoint
    from app.models.event import Event
    from app.models.organization_member import OrganizationMember


class Organization(Base):
    __tablename__ = "organizations"

    org_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    org_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    memberships: Mapped[list[OrganizationMember]] = relationship(
        back_populates="organization", cascade="all, delete-orphan"
    )
    api_keys: Mapped[list[ApiKey]] = relationship(
        back_populates="organization", cascade="all, delete-orphan"
    )
    endpoints: Mapped[list[Endpoint]] = relationship(
        back_populates="organization", cascade="all, delete-orphan"
    )
    events: Mapped[list[Event]] = relationship(
        back_populates="organization", cascade="all, delete-orphan"
    )
