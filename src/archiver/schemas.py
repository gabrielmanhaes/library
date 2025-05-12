from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TraceType(str, Enum):
    REQUEST = "request"
    RESPONSE = "response"


class BaseTraceModel(BaseModel):
    proxy_id: str
    start: datetime
    end: Optional[datetime] = None
    headers: str
    size: int
    body: Optional[str] = None
    raw: str
    type: TraceType
    truncated: bool = False


class RequestModel(BaseTraceModel):
    url: str
    method: str
    path: str


class ResponseModel(BaseTraceModel):
    status_code: int


class FlowModel(BaseModel):
    request_id: int
    response_id: int


class RequestReadModel(RequestModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ResponseReadModel(ResponseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FlowReadModel(FlowModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
