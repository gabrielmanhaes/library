import uuid
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MessageModel(BaseModel):
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


class RequestData(BaseModel):
    timestamp_start: datetime
    timestamp_end: datetime
    scheme: str
    host: str
    port: int
    path: str
    method: str
    headers: str
    trailers: str
    raw_content: str


class ResponseData(BaseModel):
    timestamp_start: datetime
    timestamp_end: datetime
    status_code: int
    reason: str
    headers: str
    trailers: str
    raw_content: str


class TransactionData(BaseModel):
    flow_id: uuid.UUID
    request: RequestData
    response: ResponseData


class FlowModel(BaseModel):
    request_id: int
    response_id: int


class RequestReadModel(RequestModel):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ResponseReadModel(ResponseModel):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class FlowReadModel(FlowModel):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class GetFlowResponse(BaseModel):
    request: RequestReadModel
    response: ResponseReadModel
