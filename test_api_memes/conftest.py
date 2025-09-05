import pytest
from endpoints.create_meme import CreateMeme
from endpoints.get_memes import GetMemes
from endpoints.get_meme_by_id import GetMemeById
from endpoints.put_meme import UpdateMeme
from endpoints.delete_meme import DeleteMeme
from tests.test_meme import TEST_DATA_AUTHORIZE_VALID
from endpoints.authorize import Authorize
from tests.test_meme import TEST_DATA_UPDATE


@pytest.fixture()
def auth_token(authorize_endpoint):
    token = authorize_endpoint.authorize(payload=TEST_DATA_AUTHORIZE_VALID[0])
    return token


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
def new_meme_id(auth_token, create_meme_endpoint):
    payload = {
        "text": "new_text",
        "url": "https://img.freepik.com/darmowe-wektory/prosty-wibrujacy-kwadratowy-mem-z-kotem_742173-4493.jpg",
        "tags": ["tag_one", "tag_two", "tag_five"],
        "info": {"topics": ["surprised", "funny"]}
    }
    response_json = create_meme_endpoint.create_meme(payload, token=auth_token)
    meme_id = response_json["id"]
    yield meme_id
    deleter = DeleteMeme()
    deleter.delete_meme(meme_id=meme_id, token=auth_token)


@pytest.fixture()
def meme_created_by_user1(authorize_endpoint, create_meme_endpoint):
    token_user1 = authorize_endpoint.authorize(payload={"name": "user_1"})
    response = create_meme_endpoint.create_meme(payload=TEST_DATA_UPDATE, token=token_user1)
    meme_id = response["id"]
    yield meme_id, token_user1  # возвращаем ID мема и токен первого пользователя
    deleter = DeleteMeme()
    deleter.delete_meme(meme_id=meme_id, token=token_user1)


@pytest.fixture()
def deleted_meme(authorize_endpoint, create_meme_endpoint):
    token = authorize_endpoint.authorize(payload={"name": "user_1"})
    payload = {
        "text": "to_delete",
        "url": "https://img.freepik.com/darmowe-wektory/"
               "prosty-вибрующий-kwadratowy-mem-z-kotem_742173-4493.jpg",
        "tags": ["delete", "test"],
        "info": {"topics": ["funny"]}
    }
    response = create_meme_endpoint.create_meme(payload=payload, token=token)
    meme_id = response["id"]
    deleter = DeleteMeme()
    deleter.delete_meme(meme_id=meme_id, token=token)
    deleter.check_that_status_is_200()
    yield meme_id, token
