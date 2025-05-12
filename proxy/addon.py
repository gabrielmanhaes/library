import os
import json
import httpx
from mitmproxy import http


ARCHIVER_URL = os.getenv("ARCHIVER_URL", "http://archiver/api/collect")


def headers_to_json(headers: http.Headers) -> str:
    as_dict = {k.decode("utf-8"): v.decode("utf-8") for k, v in headers.fields}
    return json.dumps(as_dict)


def safe_text(data: bytes | str | None, placeholder: str = "[binary omitted]") -> str:
    if data is None:
        return ""
    if isinstance(data, str):
        return data
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return placeholder


def request(flow: http.HTTPFlow) -> None:
    data = {
        "proxy_id": flow.id,
        "start": flow.request.timestamp_start,
        "end": flow.request.timestamp_end,
        "headers": headers_to_json(flow.request.headers),
        "url": flow.request.url,
        "method": flow.request.method,
        "path": flow.request.path,
        "size": len(flow.request.content),
        "body": safe_text(flow.request.text),
        "raw": safe_text(flow.request.get_content().decode(errors="replace")),
        "type": "request",
    }
    httpx.post(ARCHIVER_URL, json=data)


def response(flow: http.HTTPFlow) -> None:
    data = {
        "proxy_id": flow.id,
        "start": flow.response.timestamp_start,
        "end": flow.response.timestamp_end,
        "status_code": flow.response.status_code,
        "headers": headers_to_json(flow.response.headers),
        "size": len(flow.response.content),
        "body": safe_text(flow.response.text),
        "raw": safe_text(flow.response.get_content().decode(errors="replace")),
        "type": "response",
    }
    httpx.post(ARCHIVER_URL, json=data)
