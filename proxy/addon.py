from mitmproxy import http
import httpx
import os

ARCHIVER_URL = os.getenv("ARCHIVER_URL", "http://archiver/api/collect")

def request(flow: http.HTTPFlow) -> None:
    data = {
        "proxy_id": flow.id,
        "start": int(flow.request.timestamp_start),
        "end": int(flow.request.timestamp_end),
        "headers": str(flow.request.headers),
        "url": flow.request.url,
        "method": flow.request.method,
        "path": flow.request.path,
        "size": len(flow.request.content),
        "body": flow.request.text,
        "raw": flow.request.get_content().decode(errors="replace"),
        "type": "request"
    }
    httpx.post(ARCHIVER_URL, json=data)

def response(flow: http.HTTPFlow) -> None:
    data = {
        "proxy_id": flow.id,
        "start": int(flow.response.timestamp_start),
        "end": int(flow.response.timestamp_end),
        "status_code": flow.response.status_code,
        "headers": str(flow.response.headers),
        "size": len(flow.response.content),
        "body": flow.response.text,
        "raw": flow.response.get_content().decode(errors="replace"),
        "type": "response"
    }
    httpx.post(ARCHIVER_URL, json=data)
