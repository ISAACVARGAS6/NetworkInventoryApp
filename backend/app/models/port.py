from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base


class Port(Base):
    __tablename__ = "ports"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id")
    )

    port: Mapped[int] = mapped_column(Integer)

    service: Mapped[str] = mapped_column(String)

    device = relationship(
        "Device",
        back_populates="ports",
    )