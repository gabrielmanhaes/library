from sqlalchemy.orm import Session
from sqlalchemy import select
from archiver.models import Trace, Flow
from archiver.schemas import RequestModel, ResponseModel, FlowModel, TraceType
from typing import Sequence


class TraceRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_trace(self, trace_data: RequestModel | ResponseModel) -> Trace:
        print(trace_data.model_dump())
        trace = Trace(**trace_data.model_dump())
        self.session.add(trace)
        self.session.commit()
        self.session.refresh(trace)
        return trace

    def get_request_by_proxy_id(self, proxy_id: str) -> Trace | None:
        result = self.session.execute(
            select(Trace).where(
                Trace.proxy_id == proxy_id, Trace.type == TraceType.REQUEST
            )
        )
        return result.scalar_one_or_none()

    def get_trace_by_id(self, trace_id: int) -> Trace | None:
        result = self.session.execute(select(Trace).where(Trace.id == trace_id))
        return result.scalar_one_or_none()

    def list_traces(self, limit: int = 100, offset: int = 0) -> Sequence[Trace]:
        result = self.session.execute(
            select(Trace).order_by(Trace.created_at.desc()).offset(offset).limit(limit)
        )
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
