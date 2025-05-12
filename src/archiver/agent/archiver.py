from archiver.config import Config
from archiver.schemas import BaseTraceModel, FlowModel, TraceType
from archiver.repositories import TraceRepository, FlowRepository



class Archiver:
    def __init__(self, trace_repository: TraceRepository, flow_repository: FlowRepository):
        self.trace_repository = trace_repository
        self.flow_repository = flow_repository

    def _field_truncate(value: str, max_length: int) -> tuple[str, bool]:
        if value is None:
            return value, False
        if len(value) > max_length:
            return value[:max_length], True
        return value, False

    def _truncate(self, data: BaseTraceModel) -> BaseTraceModel:
            truncated = False
            data['url'], was = self._field_truncate(data.get('url', ''), Config.MAX_URL_LENGTH)
            truncated |= was

            data['method'], was = self._field_truncate(data.get('method', ''), Config.MAX_METHOD_LENGTH)
            truncated |= was

            data['path'], was = self._field_truncate(data.get('path', ''), Config.MAX_PATH_LENGTH)
            truncated |= was

            data['raw'], was = self._field_truncate(data.get('raw', ''), Config.MAX_RAW_LENGTH)
            truncated |= was

            data['headers'], was = self._field_truncate(data.get('headers', ''), Config.MAX_HEADERS_LENGTH)
            truncated |= was

            data['body'], was = self._field_truncate(data.get('body', ''), Config.MAX_BODY_LENGTH)
            truncated |= was

            data['truncated'] = truncated
            return data
                

    def store(self, data: BaseTraceModel) -> None:
        truncated_data = self._truncate(data)
        trace = self.trace_repository.create_trace(truncated_data)
        if trace.type == TraceType.RESPONSE:
            if request := self.trace_repository.get_request_by_proxy_id(trace.proxy_id):
                self.flow_repository.create_flow(
                    FlowModel(
                        request_id=request.id,
                        response_id=trace.id,
                    )
                )
