from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    scan_id: Mapped[int] = mapped_column(
        ForeignKey("scans.id")
    )

    ip: Mapped[str] = mapped_column(String)

    hostname: Mapped[str] = mapped_column(String)

    mac: Mapped[str] = mapped_column(String)

    manufacturer: Mapped[str] = mapped_column(String)

    ping_ms: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    device_type: Mapped[str] = mapped_column(String)

    scan = relationship(
        "Scan",
        back_populates="devices",
    )

    ports = relationship(
        "Port",
        back_populates="device",
        cascade="all, delete-orphan",
    )