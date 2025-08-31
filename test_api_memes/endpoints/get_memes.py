import requests
from endpoints.endpoint import Endpoint


class GetMemes(Endpoint):

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
