import requests
import allure
from endpoints.endpoint import Endpoint


class UpdateMeme(Endpoint):

    def update_meme(self, token=None, meme_id=None):
        headers = {}
        if token:
            headers["Authorization"] = token
        elif hasattr(self, "token") and self.token:
            headers["Authorization"] = self.token
        payload = {
            "id": meme_id,
            "text": "text_upd",
            "url": "https://img.freepik.com/darmowe-wektory/prosty-wibrujacy-kwadratowy-mem-z-kotem_742173-4493.jpg",
            "tags": ["tag_upd1", "tag_upd2", "tag_upd3"],
            "info": {"topics": ["surprisedUPD", "funnyIPD"]}
        }
        self.response = requests.put(
            f"{self.url}/meme/{meme_id}",
            headers=headers,
            json=payload        )
        try:
            self.json = self.response.json()
        except requests.JSONDecodeError:
            self.json = None

        return self.response
    @allure.step('Check that text in response is the same as sent')
    def check_response_text_is_correct(self, expected_text="text_upd"):
        assert self.json['text'] == expected_text
