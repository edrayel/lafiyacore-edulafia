"""Bus tracking SQLAlchemy models."""

import uuid
from datetime import date, datetime, time

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Time, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from edulafia.database import Base


class BusRoute(Base):
    """Bus route model for transportation management."""

    __tablename__ = "bus_routes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    driver_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    driver_phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<BusRoute(id={self.id}, name={self.name}, driver={self.driver_name})>"


class BusStop(Base):
    """Bus stop model for route waypoints."""

    __tablename__ = "bus_stops"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    route_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("bus_routes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    stop_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    location: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    estimated_time: Mapped[time | None] = mapped_column(
        Time,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<BusStop(id={self.id}, route_id={self.route_id}, name={self.stop_name})>"


class BusAttendance(Base):
    """Bus attendance model for tracking student boarding."""

    __tablename__ = "bus_attendance"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    route_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("bus_routes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    boarded: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    alighted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    board_time: Mapped[time | None] = mapped_column(
        Time,
        nullable=True,
    )
    alight_time: Mapped[time | None] = mapped_column(
        Time,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<BusAttendance(id={self.id}, student_id={self.student_id}, date={self.date})>"
