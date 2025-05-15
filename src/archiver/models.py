from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import String, Text, ForeignKey, DateTime


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, nullable=False
    )


class Message(Base):
    __abstract__ = True

    external_id: Mapped[str] = mapped_column(String(36), nullable=False)
    start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    headers: Mapped[str] = mapped_column(Text, nullable=False)
    trailers: Mapped[str] = mapped_column(Text, nullable=False)
    raw_content: Mapped[str] = mapped_column(Text, nullable=False)
    truncated: Mapped[bool] = mapped_column(nullable=False)
    size: Mapped[int] = mapped_column(nullable=False)


class Request(Message):
    __tablename__ = "requests"

    scheme: Mapped[str] = mapped_column(String(8), nullable=False)
    host: Mapped[str] = mapped_column(Text, nullable=False)
    port: Mapped[int] = mapped_column(nullable=False)
    path: Mapped[str] = mapped_column(Text, nullable=False)
    method: Mapped[str] = mapped_column(String(64), nullable=False)
    is_junk: Mapped[bool] = mapped_column(nullable=False, default=False)

    requests = relationship(
        "Flow", back_populates="request", foreign_keys="Flow.request_id"
    )


class Response(Message):
    __tablename__ = "responses"

    status_code: Mapped[Optional[int]] = mapped_column(nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=False)

    responses = relationship(
        "Flow", back_populates="response", foreign_keys="Flow.response_id"
    )


class Flow(Base):
    __tablename__ = "flows"

    request_id: Mapped[int] = mapped_column(ForeignKey("requests.id"), nullable=False)
    response_id: Mapped[int] = mapped_column(ForeignKey("responses.id"), nullable=False)
    processed: Mapped[bool] = mapped_column(nullable=False, default=False)

    request: Mapped["Request"] = relationship(
        back_populates="requests", foreign_keys=[request_id]
    )
    response: Mapped["Response"] = relationship(
        back_populates="responses", foreign_keys=[response_id]
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
