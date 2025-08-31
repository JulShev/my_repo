import requests
import json
from endpoints.endpoint import Endpoint

class CreateMeme(Endpoint):

    def create_meme(self, payload, token=None):
        headers = {}
        if token:
            headers["Authorization"] = token
        elif hasattr(self, "token") and self.token:
            headers["Authorization"] = self.token

        self.response = requests.post(
            f"{self.url}/meme",
            headers=headers,
            json=payload
        )
        try:
            self.json = self.response.json()
        except json.JSONDecodeError:
            self.json = {}
        return self.json
