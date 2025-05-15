from typing import TYPE_CHECKING, Type
from archiver.config import logger
from archiver.models import Request, Response, Message
from archiver.client import LibrarianClient
from archiver.schemas import (
    RequestModel,
    RequestReadModel,
    ResponseModel,
    ResponseReadModel,
    MessageModel,
    FlowModel,
    GetFlowResponse,
)
from archiver.repositories import MessageRepository, FlowRepository

if TYPE_CHECKING:
    from archiver.agent import Janitor


class Archiver:
    def __init__(
        self,
        librarian_client: LibrarianClient,
        message_repository: MessageRepository,
        flow_repository: FlowRepository,
        janitor: "Janitor",
    ):
        self.librarian_client = librarian_client
        self.message_repository = message_repository
        self.flow_repository = flow_repository
        self.janitor = janitor

    def _store_flow(self, record: Message) -> None:
        request: Message | None = None
        response: Message | None = None

        if isinstance(record, Request):
            request = record
            response = self.message_repository.get_message_by_external_id(
                Response, record.external_id
            )

        elif isinstance(record, Response):
            response = record
            request = self.message_repository.get_message_by_external_id(
                Request, record.external_id
            )

        if request and response:
            model = FlowModel(
                request_id=request.id,
                response_id=response.id,
            )
            flow = self.flow_repository.create_flow(model)
            logger.debug(f"Flow {flow.request_id} stored.")

            self.librarian_client.dispatch(flow.id)

    def _store_message(self, data: MessageModel) -> Message:
        _type: Type[Message] | None = None

        if isinstance(data, RequestModel):
            _type = Request
        elif isinstance(data, ResponseModel):
            _type = Response

        if not _type:
            raise ValueError("Invalid message type")

        message = self.message_repository.create(_type, data)
        logger.debug(f"Message {message.external_id} stored.")

        return message

    def store(self, data: MessageModel) -> None:
        record: Message | None = None
        data.size = len(data.raw_content)
        clean_data = self.janitor.clean(data)

        record = self._store_message(clean_data)
        self._store_flow(record)

    def get_flow(self, flow_id: int) -> GetFlowResponse:
        flow = self.flow_repository.get_flow_by_id(flow_id)
        if not flow:
            raise ValueError(f"Flow {flow_id} not found")
        request = self.message_repository.get_message_by_id(Request, flow.request_id)
        response = self.message_repository.get_message_by_id(Response, flow.response_id)
        if not request or not response:
            raise ValueError(f"Flow {flow_id} not found")
        return GetFlowResponse(
            request=RequestReadModel.model_validate(request),
            response=ResponseReadModel.model_validate(response),
        )
