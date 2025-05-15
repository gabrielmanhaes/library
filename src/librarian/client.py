import requests
from librarian.schemas import GetFlowResponse


class ArchiverClient:
    def __init__(self):
        self.base_url = "http://archiver/api"

    def get_flow(self, flow_id: int) -> GetFlowResponse | None:
        url = f"{self.base_url}/flows/{flow_id}/"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to get flow: {response.text}")
        return GetFlowResponse.model_validate(response.json())


class OllamaClient:
    def __init__(self):
        self.base_url = "http://ollama:11434/api"

    def dispatch(self, flow: GetFlowResponse) -> None:
        url = f"{self.base_url}/generate"
        data = {
            "model": "gemma3",
            "prompt": (
                "You are a data analyst. You will be given a HTTP request/response pair. "
                "Your task is to analyze the request and response, and provide a meaningful "
                "analysis of the data in the pair. You should categorize this data, analyze "
                "it for any anomalies, analyze it for possible security issues and also analyze "
                "it for attempts to bypass security measures. If there's nothing wrong with the pair, "
                "you should analyze it by being as specific as possible. Your response won't contain "
                "any written text, only JSON. The JSON should contain the following fields: meta, content, "
                "type, source. There's no specific requirements for the meta field, it should contain "
                "metadata, could be tags, could be anything. The content field should contain your analysis. "
                "The type field should contain one categorical value, it could be, for example: 'security', "
                "'trackers', 'ads', etc. The source field should contain the source of the data, which will always "
                "be 'gemma3', in your case. This is the request/response pair: \n\n"
                f"Request: {flow.request.model_dump_json()}\n\n"
                f"Response: {flow.response.model_dump_json()}\n\n"
            ),
        }
        response = requests.post(url, json=data)
        print(response.content)
        if response.status_code != 200:
            raise Exception(f"Failed to dispatch flow to Ollama: {response.text}")
