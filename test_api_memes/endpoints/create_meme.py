import requests
import json
import allure
from endpoints.endpoint import Endpoint


class CreateMeme(Endpoint):

    @allure.step('Create meme')
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
            self.json = None
        return self.json

    @allure.step('Check that id is not null')
    def check_response_id_is_not_none(self):
        assert self.json['id'] is not None
