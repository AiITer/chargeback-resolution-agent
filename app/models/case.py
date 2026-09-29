from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.schemas.case import CaseStatus


class ChargebackCaseModel(Base):
    __tablename__ = "chargeback_cases"

    case_id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
    )

    stripe_dispute_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    dispute_reason: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    status: Mapped[CaseStatus] = mapped_column(
    Enum(
        CaseStatus,
        name="case_status",
        values_callable=lambda enum_cls: [
            member.value for member in enum_cls
        ],
    ),
    nullable=False,
    default=CaseStatus.OPEN,
)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )