import pytest
from endpoints.authorize import Authorize
from endpoints.create_meme import CreateMeme
from endpoints.get_memes import GetMemes
from endpoints.get_meme_by_id import GetMemeById
from endpoints.put_meme import UpdateMeme
from endpoints.delete_meme import DeleteMeme


@pytest.fixture(scope="session")
def authorize_endpoint():
    return Authorize()


@pytest.fixture()
def get_meme_by_id_endpoint():
    return GetMemeById()


@pytest.fixture()
def create_meme_endpoint():
    return CreateMeme()


@pytest.fixture()
def get_memes_endpoint():
    return GetMemes()


@pytest.fixture()
def put_meme_endpoint():
    return UpdateMeme()


@pytest.fixture()
def delete_meme_endpoint():
    return DeleteMeme()


@pytest.fixture()
def new_meme_id(authorize_endpoint, create_meme_endpoint):
    token = authorize_endpoint.authorize()
    payload = {
        "text": "new_text",
        "url": "https://img.freepik.com/darmowe-wektory/prosty-wibrujacy-kwadratowy-mem-z-kotem_742173-4493.jpg",
        "tags": ["tag_one", "tag_two", "tag_five"],
        "info": {"topics": ["surprised", "funny"]}
    }
    response_json = create_meme_endpoint.create_meme(payload, token=token)
    return response_json["id"]
