import requests
from endpoints.endpoint import Endpoint


class Authorize(Endpoint):
    token = None

    def authorize(self):
        self.response = requests.post(
            f"{self.url}/authorize",
            json={"name": "name_test"}
        )
        self.response.raise_for_status()
        self.token = self.response.json().get("token")
        return self.token


    def check_token(self):
        """Проверка валидности токена"""
        if not self.token:
            return False
        response = requests.get(f"{self.url}/authorize/{self.token}")
        return response.status_code == 200
