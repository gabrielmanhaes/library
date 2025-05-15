import os
import json
import httpx
from mitmproxy import http


ARCHIVER_URL = os.getenv("ARCHIVER_URL", "http://archiver/api/collect/")


def to_safe_json(data: http.Headers) -> str:
    if data:
        as_dict = {
            to_safe_text(k.decode("utf-8")): to_safe_text(v.decode("utf-8"))
            for k, v in data.fields
        }
        return json.dumps(as_dict)
    else:
        return "{}"


def to_safe_text(
    data: bytes | str | None, placeholder: str = "[binary omitted]"
) -> str:
    if data is None:
        return ""
    if isinstance(data, str):
        return data
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return placeholder


def response(flow: http.HTTPFlow) -> None:
    data = {
        "flow_id": to_safe_text(flow.id),
        "request": {
            "timestamp_start": int(flow.request.timestamp_start),
            "timestamp_end": int(flow.request.timestamp_end),
            "port": int(flow.request.port),
            "scheme": to_safe_text(flow.request.scheme),
            "host": to_safe_text(flow.request.host),
            "path": to_safe_text(flow.request.path),
            "method": to_safe_text(flow.request.method),
            "headers": to_safe_json(flow.request.headers),
            "trailers": to_safe_json(flow.request.trailers),
            "raw_content": to_safe_text(flow.request.raw_content),
        },
        "response": {
            "timestamp_start": int(flow.response.timestamp_start),
            "timestamp_end": int(flow.response.timestamp_end),
            "status_code": int(flow.response.status_code),
            "reason": to_safe_text(flow.response.reason),
            "headers": to_safe_json(flow.response.headers),
            "trailers": to_safe_json(flow.response.trailers),
            "raw_content": to_safe_text(flow.response.raw_content),
        },
    }
    httpx.post(ARCHIVER_URL, json=data)
