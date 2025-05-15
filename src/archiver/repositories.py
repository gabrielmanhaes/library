from sqlalchemy.orm import Session
from sqlalchemy import select
from archiver.models import Message, Flow
from archiver.schemas import MessageModel, FlowModel
from typing import Type, Sequence


class MessageRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, type_: Type[Message], data: MessageModel) -> Message:
        message = type_(**data.model_dump())
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def get_message_by_external_id(
        self, type_: Type[Message], external_id: str
    ) -> Message | None:
        stmt = select(type_).where(type_.external_id == external_id)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def get_message_by_id(
        self, type_: Type[Message], message_id: int
    ) -> Message | None:
        stmt = select(type_).where(type_.id == message_id)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def list(
        self, type_: Type[Message], limit: int = 100, offset: int = 0
    ) -> Sequence[Message]:
        stmt = (
            select(type_).order_by(type_.created_at.desc()).offset(offset).limit(limit)
        )
        result = self.session.execute(stmt)
        return result.scalars().all()


class FlowRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_flow(self, flow_data: FlowModel) -> Flow:
        flow = Flow(**flow_data.model_dump())
        self.session.add(flow)
        self.session.commit()
        self.session.refresh(flow)
        return flow

    def get_flow_by_id(self, flow_id: int) -> Flow | None:
        result = self.session.execute(select(Flow).where(Flow.id == flow_id))
        return result.scalar_one_or_none()

    def list_flows(self, limit: int = 100, offset: int = 0) -> Sequence[Flow]:
        result = self.session.execute(
            select(Flow).order_by(Flow.created_at.desc()).offset(offset).limit(limit)
        )
        return result.scalars().all()
