from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import String, Text, ForeignKey, DateTime, Enum as SQLAlchemyEnum

from .schemas import TraceType

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=datetime.now, nullable=False)

class Trace(Base):
    __tablename__ = "traces"
    
    start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status_code: Mapped[int] = mapped_column()
    headers: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(String(1024))
    method: Mapped[str] = mapped_column(String(8))
    path: Mapped[str] = mapped_column(String(1024))
    proxy_id: Mapped[str] = mapped_column(String(36))
    size: Mapped[int] = mapped_column(nullable=False)
    body: Mapped[Optional[str]] = mapped_column(Text)
    truncated: Mapped[bool] = mapped_column(nullable=False)
    raw: Mapped[Optional[str]] = mapped_column(Text, nullable=False)
    type: Mapped[TraceType] = mapped_column(SQLAlchemyEnum(TraceType), nullable=False)

class Flow(Base):
    __tablename__ = "flows"

    request_id: Mapped[int] = mapped_column(ForeignKey("traces.id"))
    response_id: Mapped[int] = mapped_column(ForeignKey("traces.id"))
    
    request: Mapped["Trace"] = relationship(back_populates="flows")
    response: Mapped["Trace"] = relationship(back_populates="flows")

class Annotation(Base):
    __tablename__ = "annotations"

    meta: Mapped[Optional[str]] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(64), nullable=False)
    source: Mapped[str] = mapped_column(String(64), nullable=False)

class Link(Base):
    __tablename__ = "links"

    annotation_id: Mapped[int] = mapped_column(ForeignKey("annotations.id"), nullable=False)
    flow_id: Mapped[int] = mapped_column(ForeignKey("flows.id"), nullable=False)

    annotation: Mapped["Annotation"] = relationship(back_populates="links")
    flow: Mapped["Flow"] = relationship(back_populates="links")
