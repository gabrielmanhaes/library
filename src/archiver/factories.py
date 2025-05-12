from archiver.agent import Archiver, Janitor, Blocker
from archiver.repositories import TraceRepository, FlowRepository
from archiver.config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def get_archiver_instance() -> Archiver:
    engine = create_engine(Config.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        trace_repo = TraceRepository(db)
        flow_repo = FlowRepository(db)
        blocker = Blocker()
        janitor = Janitor(trace_repository=trace_repo, blocker=blocker)
        return Archiver(
            trace_repository=trace_repo,
            flow_repository=flow_repo,
            janitor=janitor,
        )
    except Exception:
        db.close()
        raise
