import requests


class LibrarianClient:
    def __init__(self):
        self.base_url = "http://librarian/api"

    def dispatch(self, flow_id: int) -> None:
        url = f"{self.base_url}/flows/{flow_id}/"
        response = requests.post(url)
        if response.status_code != 200:
            raise Exception(f"Failed to dispatch flow: {response.text}")
