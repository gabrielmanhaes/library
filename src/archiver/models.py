from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import String, Text, ForeignKey, DateTime, Enum as SQLAlchemyEnum

from .schemas import TraceType


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, nullable=False
    )


class Trace(Base):
    __tablename__ = "traces"

    start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    status_code: Mapped[Optional[int]] = mapped_column(nullable=True)
    headers: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    method: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    proxy_id: Mapped[str] = mapped_column(String(36), nullable=False)
    size: Mapped[int] = mapped_column(nullable=False)
    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    truncated: Mapped[bool] = mapped_column(nullable=False)
    raw: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[TraceType] = mapped_column(SQLAlchemyEnum(TraceType), nullable=False)

    request_flows = relationship(
        "Flow", back_populates="request", foreign_keys="Flow.request_id"
    )
    response_flows = relationship(
        "Flow", back_populates="response", foreign_keys="Flow.response_id"
    )


class Flow(Base):
    __tablename__ = "flows"

    request_id: Mapped[int] = mapped_column(ForeignKey("traces.id"), nullable=False)
    response_id: Mapped[int] = mapped_column(ForeignKey("traces.id"), nullable=False)

    request: Mapped["Trace"] = relationship(
        back_populates="request_flows", foreign_keys=[request_id]
    )
    response: Mapped["Trace"] = relationship(
        back_populates="response_flows", foreign_keys=[response_id]
    )

    links = relationship("Link", back_populates="flow")


class Annotation(Base):
    __tablename__ = "annotations"

    meta: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(64), nullable=False)
    source: Mapped[str] = mapped_column(String(64), nullable=False)

    links = relationship("Link", back_populates="annotation")


class Link(Base):
    __tablename__ = "links"

    annotation_id: Mapped[int] = mapped_column(
        ForeignKey("annotations.id"), nullable=False
    )
    flow_id: Mapped[int] = mapped_column(ForeignKey("flows.id"), nullable=False)

    annotation: Mapped["Annotation"] = relationship(
        back_populates="links", foreign_keys=[annotation_id]
    )
    flow: Mapped["Flow"] = relationship(back_populates="links", foreign_keys=[flow_id])
