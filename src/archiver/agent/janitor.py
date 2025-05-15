import json
from urllib.parse import urlparse
from archiver.agent import Blocker
from archiver.config import Config
from archiver.repositories import MessageRepository
from archiver.schemas import RequestModel, ResponseModel, MessageModel


class Janitor:
    def __init__(
        self,
        message_repository: MessageRepository,
        blocker: Blocker,
    ):
        self.message_repository = message_repository
        self.blocker = blocker

    def _drop(self, data: MessageModel) -> MessageModel:

        if isinstance(data, RequestModel):
            data.is_junk = self.blocker.is_junk(data.host)

        headers = json.loads(data.headers)
        trailers = json.loads(data.trailers)

        clean_headers = headers.copy()
        clean_trailers = trailers.copy()

        for header in headers.keys():
            should_drop = self.blocker.should_drop_header(header)
            if should_drop:
                clean_headers.pop(header)

        for trailer in trailers.keys():
            should_drop = self.blocker.should_drop_trailer(trailer)
            if should_drop:
                clean_trailers.pop(trailer)

        data.headers = json.dumps(clean_headers)
        data.trailers = json.dumps(clean_trailers)

        return data

    def _field_truncate(self, value: str, max_length: int) -> tuple[str, bool]:
        if not value:
            return value, False
        if len(value) > max_length:
            return value[:max_length], True
        return value, False

    def _truncate(self, data: MessageModel) -> MessageModel:
        truncated = False

        def apply(field_name: str, max_length: int):
            nonlocal truncated
            value = getattr(data, field_name)
            new_value, was_truncated = self._field_truncate(value, max_length)
            setattr(data, field_name, new_value)
            truncated |= was_truncated

        if isinstance(data, RequestModel):
            apply("host", Config.MAX_URL_LENGTH)
            apply("path", Config.MAX_PATH_LENGTH)
            apply("method", Config.MAX_METHOD_LENGTH)

        apply("raw_content", Config.MAX_RAW_CONTENT_LENGTH)
        apply("headers", Config.MAX_HEADERS_LENGTH)
        apply("trailers", Config.MAX_TRAILERS_LENGTH)

        data.truncated = truncated
        return data

    def _safe(self, data: MessageModel) -> MessageModel:
        fields = list(MessageModel.model_fields.keys())

        if isinstance(data, RequestModel):
            fields += list(RequestModel.model_fields.keys())
        elif isinstance(data, ResponseModel):
            fields += list(ResponseModel.model_fields.keys())

        for field in fields:
            value = getattr(data, field)
            if isinstance(value, bytes):
                value = value.decode("utf-8", errors="replace")
                setattr(data, field, value)

        return data

    def clean(self, data: MessageModel) -> MessageModel:
        safe_data = self._safe(data)
        clean_data = self._drop(safe_data)
        truncated_data = self._truncate(clean_data)
        return truncated_data
