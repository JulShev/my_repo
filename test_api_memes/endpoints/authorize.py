import requests
from endpoints.endpoint import Endpoint


class Authorize(Endpoint):
    token = None

    def authorize(self, payload):
        self.response = requests.post(
            f"{self.url}/authorize",
            json=payload
        )
        # Успешная авторизация → сохраняем токен
        if self.response.status_code == 200:
            try:
                self.token = self.response.json().get("token")
            except ValueError:
                self.token = None
            return self.token

        # Негативный сценарий → просто возвращаем None
        self.token = None
        return None


    def check_token(self):
        """Проверка валидности токена"""
        if not self.token:
            return False
        response = requests.get(f"{self.url}/authorize/{self.token}")
        return response.status_code == 200
