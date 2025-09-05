import json
import allure
import requests
from endpoints.endpoint import Endpoint


class GetMemeById(Endpoint):

    @allure.step('Get meme')
    def get_meme_by_id(self, token=None, meme_id=None):
        headers = {}
        if token:
            headers["Authorization"] = token
        elif hasattr(self, "token") and self.token:
            headers["Authorization"] = self.token
        self.response = requests.get(
            f"{self.url}/meme/{meme_id}",
            headers=headers
        )
        try:
            self.json = self.response.json()
        except json.JSONDecodeError:
            self.json = None
        return self.json

    @allure.step('Check that id is correct')
    def check_that_id_is_correct(self, new_meme_id):
        json_response = self.response.json()
        assert json_response['id'] == new_meme_id, 'id is not correct'
