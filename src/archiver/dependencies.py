from typing import Annotated
from fastapi import Depends
from archiver.agent import Archiver, Janitor, Blocker
from archiver.config import Config
from archiver.repositories import TraceRepository, FlowRepository
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Engine, create_engine


def get_engine() -> Engine:
    return create_engine(Config.DATABASE_URL)


APIEngine = Annotated[Engine, Depends(get_engine)]


def get_session(
    engine: APIEngine,
):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


APISession = Annotated[Session, Depends(get_session)]


def get_trace_repository(session: APISession) -> TraceRepository:
    return TraceRepository(session)


def get_flow_repository(session: APISession) -> FlowRepository:
    return FlowRepository(session)


APITraceRepository = Annotated[TraceRepository, Depends(get_trace_repository)]
APIFlowRepository = Annotated[FlowRepository, Depends(get_flow_repository)]


def get_blocker(
    blocker: Blocker = Depends(Blocker),
) -> Blocker:
    return blocker


APIBlocker = Annotated[Blocker, Depends(get_blocker)]


def get_janitor(
    trace_repository: APITraceRepository,
    blocker: APIBlocker,
):
    return Janitor(
        trace_repository=trace_repository,
        blocker=blocker,
    )


APIJanitor = Annotated[Janitor, Depends(get_janitor)]


def get_archiver(
    trace_repository: APITraceRepository,
    flow_repository: APIFlowRepository,
    janitor: APIJanitor,
) -> Archiver:
    return Archiver(
        trace_repository=trace_repository,
        flow_repository=flow_repository,
        janitor=janitor,
    )


APIArchiver = Annotated[Archiver, Depends(get_archiver)]
