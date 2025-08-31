import requests
from endpoints.endpoint import Endpoint


class GetMemeById(Endpoint):

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
        except requests.JSONDecodeError:
            self.json = None
        return self.response
