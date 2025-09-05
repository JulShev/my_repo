import requests
from endpoints.endpoint import Endpoint
import allure
import json


class DeleteMeme(Endpoint):

    def delete_meme(self, token=None, meme_id=None):
        headers = {}
        if token:
            headers["Authorization"] = token
        elif hasattr(self, "token") and self.token:
            headers["Authorization"] = self.token

        self.response = requests.delete(
            f"{self.url}/meme/{meme_id}",
            headers=headers
        )

        return self.response

    @allure.step("Check that success message is correct for meme_id={meme_id}")
    def check_response_message_is_correct(self, meme_id):
        expected_message = f"Meme with id {meme_id} successfully deleted"
        actual_message = self.response.text
        assert actual_message == expected_message
