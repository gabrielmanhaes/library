from librarian.schemas import GetFlowResponse
from librarian.client import OllamaClient


class Librarian:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client

    def dispatch(self, flow: GetFlowResponse):
        self.ollama_client.dispatch(flow)
