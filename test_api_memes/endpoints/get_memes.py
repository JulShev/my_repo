import requests
import allure
from endpoints.endpoint import Endpoint


class GetMemes(Endpoint):

    @allure.step('Get memes')
    def get_memes(self, token=None):
        headers = {}
        if token:  # если передали токен явно — используем его
            headers["Authorization"] = token
        elif hasattr(self, "token") and self.token:  # иначе пробуем взять из объекта
            headers["Authorization"] = self.token
        self.response = requests.get(
            f"{self.url}/meme",
            headers=headers
        )
        return self.response

    @allure.step('Check response is not empty')
    def check_response_is_not_empty(self):
        json_response = self.response.json()
        assert json_response, 'response is empty'
