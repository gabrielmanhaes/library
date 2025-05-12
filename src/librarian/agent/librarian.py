from openai import OpenAI

class Librarian:
    def __init__(self, api_key, model):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def feed(self, input):
        response = self.client.responses.create(
            model=self.model,
            input=input,
        )
        return response
