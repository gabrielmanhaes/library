from archiver.factories import get_archiver_instance
from archiver.schemas import RequestModel, ResponseModel
from .app import app

archiver = get_archiver_instance()


@app.task(name="merlin.collect")
def collect(event: dict) -> None:
    request = RequestModel(
        external_id=event["flow_id"],
        start=event["request"]["timestamp_start"],
        end=event["request"]["timestamp_end"],
        scheme=event["request"]["scheme"],
        host=event["request"]["host"],
        port=event["request"]["port"],
        path=event["request"]["path"],
        method=event["request"]["method"],
        headers=event["request"]["headers"],
        trailers=event["request"]["trailers"],
        raw_content=event["request"]["raw_content"],
    )

    response = ResponseModel(
        external_id=event["flow_id"],
        start=event["response"]["timestamp_start"],
        end=event["response"]["timestamp_end"],
        status_code=event["response"]["status_code"],
        reason=event["response"]["reason"],
        headers=event["response"]["headers"],
        trailers=event["response"]["trailers"],
        raw_content=event["response"]["raw_content"],
    )
    archiver.store(request)
    archiver.store(response)
