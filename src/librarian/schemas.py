import uuid
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MessageModel(BaseModel):
    id: int
    created_at: datetime
    external_id: uuid.UUID
    start: datetime
    end: datetime
    headers: str
    trailers: str
    raw_content: str
    size: Optional[int] = None
    truncated: bool = False


class RequestModel(MessageModel):
    scheme: str
    host: str
    port: int
    path: str
    method: str
    is_junk: bool = False


class ResponseModel(MessageModel):
    status_code: int
    reason: str


class GetFlowResponse(BaseModel):
    request: RequestModel
    response: ResponseModel
