from archiver.repositories import MessageRepository, FlowRepository
from archiver.agent import Archiver, Janitor, Blocker
from archiver.client import LibrarianClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from archiver.config import Config


def get_archiver_instance() -> Archiver:
    engine = create_engine(Config.DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        librarian_client = LibrarianClient()
        message_repository = MessageRepository(db)
        flow_repository = FlowRepository(db)
        blocker = Blocker()
        janitor = Janitor(message_repository=message_repository, blocker=blocker)
        return Archiver(
            librarian_client=librarian_client,
            message_repository=message_repository,
            flow_repository=flow_repository,
            janitor=janitor,
        )
    except Exception:
        db.close()
        raise
