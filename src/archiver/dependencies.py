from typing import Annotated
from fastapi import Depends
from archiver.client import LibrarianClient
from archiver.agent import Archiver, Janitor, Blocker
from archiver.config import Config
from archiver.repositories import MessageRepository, FlowRepository
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Engine, create_engine

engine = create_engine(Config.DATABASE_URL, pool_pre_ping=True)


def get_engine() -> Engine:
    return engine


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


def get_librarian_client() -> LibrarianClient:
    return LibrarianClient()


APILibrarianClient = Annotated[LibrarianClient, Depends(get_librarian_client)]


def get_message_repository(session: APISession) -> MessageRepository:
    return MessageRepository(session)


def get_flow_repository(session: APISession) -> FlowRepository:
    return FlowRepository(session)


APIMessageRepository = Annotated[MessageRepository, Depends(get_message_repository)]
APIFlowRepository = Annotated[FlowRepository, Depends(get_flow_repository)]


def get_blocker(
    blocker: Blocker = Depends(Blocker),
) -> Blocker:
    return blocker


APIBlocker = Annotated[Blocker, Depends(get_blocker)]


def get_janitor(
    message_repository: APIMessageRepository,
    blocker: APIBlocker,
):
    return Janitor(
        message_repository=message_repository,
        blocker=blocker,
    )


APIJanitor = Annotated[Janitor, Depends(get_janitor)]


def get_archiver(
    librarian_client: APILibrarianClient,
    message_repository: APIMessageRepository,
    flow_repository: APIFlowRepository,
    janitor: APIJanitor,
) -> Archiver:
    return Archiver(
        librarian_client=librarian_client,
        message_repository=message_repository,
        flow_repository=flow_repository,
        janitor=janitor,
    )


APIArchiver = Annotated[Archiver, Depends(get_archiver)]
