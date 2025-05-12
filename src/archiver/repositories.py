from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from archiver.models import Trace, Flow
from archiver.schemas import BaseTraceModel, FlowModel, TraceType
from typing import List

class TraceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_trace(self, trace_data: BaseTraceModel) -> Trace:
        trace = Trace(**trace_data.model_dump())
        self.session.add(trace)
        await self.session.commit()
        await self.session.refresh(trace)
        return trace
    
    async def get_request_by_proxy_id(self, proxy_id: str) -> Trace | None:
        result = await self.session.execute(
            select(Trace).where(Trace.proxy_id == proxy_id, Trace.type == TraceType.REQUEST)
        )
        return result.scalar_one_or_none()

    async def get_trace_by_id(self, trace_id: int) -> Trace | None:
        result = await self.session.execute(
            select(Trace).where(Trace.id == trace_id)
        )
        return result.scalar_one_or_none()

    async def list_traces(self, limit: int = 100, offset: int = 0) -> List[Trace]:
        result = await self.session.execute(
            select(Trace).order_by(Trace.timestamp.desc()).offset(offset).limit(limit)
        )
        return result.scalars().all()

class FlowRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_flow(self, flow_data: FlowModel) -> Flow:
        flow = Flow(**flow_data.model_dump())
        self.session.add(flow)
        await self.session.commit()
        await self.session.refresh(flow)
        return flow

    async def get_flow_by_id(self, flow_id: int) -> Flow | None:
        result = await self.session.execute(
            select(Flow).where(Flow.id == flow_id)
        )
        return result.scalar_one_or_none()

    async def list_flows(self, limit: int = 100, offset: int = 0) -> List[Flow]:
        result = await self.session.execute(
            select(Flow).order_by(Flow.timestamp.desc()).offset(offset).limit(limit)
        )
        return result.scalars().all()
