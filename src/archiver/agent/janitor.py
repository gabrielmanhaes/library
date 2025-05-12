import json
from urllib.parse import urlparse
from archiver.agent import Blocker
from archiver.config import Config
from archiver.crypto import decrypt, encrypt
from archiver.repositories import TraceRepository
from archiver.schemas import RequestModel, ResponseModel


class Janitor:
    def __init__(self, trace_repository: TraceRepository, blocker: Blocker):
        self.trace_repository = trace_repository
        self.blocker = blocker

    def _extract_domain(self, url: str) -> str:
        try:
            parsed = urlparse(url)
            return parsed.netloc.lower()
        except Exception:
            return ""

    def _drop(
        self, data: RequestModel | ResponseModel
    ) -> RequestModel | ResponseModel | None:
        if isinstance(data, RequestModel):
            domain = self._extract_domain(data.url)
            should_drop_trace = self.blocker.should_drop_trace(domain)
        else:
            should_drop_trace = (
                self.trace_repository.get_request_by_proxy_id(data.proxy_id) is None
            )

        if should_drop_trace:
            return None

        headers = json.loads(data.headers)
        for header in headers.keys():
            should_drop_header = self.blocker.should_drop_header(header)
            if should_drop_header:
                headers.pop(header)

        data.headers = json.dumps(headers)

        return data

    def _field_truncate(self, value: str, max_length: int) -> tuple[str, bool]:
        if value is None or value == "":
            return value, False
        if len(value) > max_length:
            return value[:max_length], True
        return value, False

    def _truncate(
        self, data: RequestModel | ResponseModel
    ) -> RequestModel | ResponseModel:

        truncated = False

        if isinstance(data, RequestModel):
            data.url, was = self._field_truncate(data.url, Config.MAX_URL_LENGTH)
            truncated |= was

            data.method, was = self._field_truncate(
                data.method, Config.MAX_METHOD_LENGTH
            )
            truncated |= was

            data.path, was = self._field_truncate(data.path, Config.MAX_PATH_LENGTH)
            truncated |= was

        data.raw, was = self._field_truncate(data.raw, Config.MAX_RAW_LENGTH)
        truncated |= was

        data.headers, was = self._field_truncate(
            data.headers, Config.MAX_HEADERS_LENGTH
        )
        truncated |= was

        if data.body:
            data.body, was = self._field_truncate(data.body, Config.MAX_BODY_LENGTH)
            truncated |= was

        data.truncated = truncated
        return data

    def clean(
        self, data: RequestModel | ResponseModel
    ) -> RequestModel | ResponseModel | None:
        clean_data = self._drop(data)
        if clean_data is None:
            return None
        clean_data = self._truncate(clean_data)
        return clean_data
