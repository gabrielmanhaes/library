from librarian.agent import Librarian
from librarian.client import ArchiverClient, OllamaClient


def get_ollama_client() -> OllamaClient:
    return OllamaClient()


def get_archiver_client() -> ArchiverClient:
    return ArchiverClient()


def get_librarian_instance() -> Librarian:
    return Librarian(get_ollama_client())
