from .app import app
from librarian.factories import get_archiver_client, get_librarian_instance

archiver_client = get_archiver_client()
librarian = get_librarian_instance()


@app.task(name="hermes.dispatch")
def dispatch(flow_id: int) -> None:
    flow = archiver_client.get_flow(flow_id)
    if flow is None:
        raise Exception(f"Flow with ID {flow_id} not found.")
    librarian.dispatch(flow)
