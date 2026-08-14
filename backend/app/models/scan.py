from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    network: Mapped[str] = mapped_column(String)

    status: Mapped[str] = mapped_column(
        String,
        default="completed",
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    finished_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    hosts_found: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    devices = relationship(
        "Device",
        back_populates="scan",
        cascade="all, delete-orphan",
    )