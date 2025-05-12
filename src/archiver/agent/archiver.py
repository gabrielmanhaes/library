from archiver.config import logger
from archiver.schemas import RequestModel, ResponseModel, FlowModel, TraceType
from archiver.repositories import TraceRepository, FlowRepository
from archiver.crypto import encrypt


class Archiver:
    def __init__(
        self,
        trace_repository: TraceRepository,
        flow_repository: FlowRepository,
        janitor: "Janitor",
    ):
        self.trace_repository = trace_repository
        self.flow_repository = flow_repository
        self.janitor = janitor

    def encrypt(
        self, data: RequestModel | ResponseModel
    ) -> RequestModel | ResponseModel:
        encrypted_data = data
        if isinstance(encrypted_data, RequestModel):
            encrypted_data.url = encrypt(encrypted_data.url)
            encrypted_data.path = encrypt(encrypted_data.path)

        encrypted_data.raw = encrypt(encrypted_data.raw)
        encrypted_data.headers = encrypt(encrypted_data.headers)

        if encrypted_data.body:
            encrypted_data.body = encrypt(encrypted_data.body)

        return encrypted_data

    def store(self, data: RequestModel | ResponseModel) -> None:
        clean_data = self.janitor.clean(data)
        if clean_data is None:
            logger.debug(f"Request {data.proxy_id} dropped by janitor.")
            return
        else:
            encrypted_data = self.encrypt(clean_data)
            trace = self.trace_repository.create_trace(encrypted_data)
            if trace.type == TraceType.RESPONSE:
                if request := self.trace_repository.get_request_by_proxy_id(
                    trace.proxy_id
                ):
                    self.flow_repository.create_flow(
                        FlowModel(
                            request_id=request.id,
                            response_id=trace.id,
                        )
                    )
