import pytest


TEST_DATA_AUTHORIZE_VALID = [
    {"name": "user_name"},  # valid value
    {"name": ""}  # empty string
]

TEST_DATA_AUTHORIZE_INVALID = [
    {},  # empty body
    {"wrong_field": "user_1"}, # invalid key
    {"name": 12345} # invalid format data
]

TEST_DATA_CREATE_VALID = [
    {
        "text": "cat new aug",
        "url": "https://img.freepik.com/darmowe-wektory/prosty-wibrujacy-kwadratowy-mem-z-kotem_742173-4493.jpg",
        "tags": ["one", "two", "five"],
        "info": {"topics": ["boring", "happy"]}
    },
    {
        "text": "", # empty field
        "url": "https://img.freepik.com/darmowe-wektory/prosty-wibrujacy-kwadratowy-mem-z-kotem_742173-4493.jpg",
        "tags": ["one", "two", "five"],
        "info": {"topics": ["boring", "happy"]}
    }
]

TEST_DATA_CREATE_INVALID = [
    {
        "text": 1, # incorrect data format
        "url": "https://img.freepik.com/darmowe-wektory/prosty-wibrujacy-kwadratowy-mem-z-kotem_742173-4493.jpg",
        "tags": ["one", "two", "five"],
        "info": {"topics": ["surprised", "funny"]}
    },
    {
        # "text": "cat new aug",
        "url": "https://img.freepik.com/darmowe-wektory/prosty-wibrujacy-kwadratowy-mem-z-kotem_742173-4493.jpg",
        "tags": ["one", "two", "five"],
        "info": {"topics": ["surprised", "funny"]}
    }
]

TEST_DATA_UPDATE_VALID = [
    {
        "id": None,
        "text": "text_upd",
        "url": "https://img.freepik.com/darmowe-wektory/prosty-wibrujacy-kwadratowy-mem-z-kotem_742173-4493.jpg",
        "tags": ["tag_upd1", "tag_upd2", "tag_upd3"],
        "info": {"topics": ["surprisedUPD", "funnyIPD"]}
    },
    {
        "id": None,
        "text": "text_upd",
        "url": "https://img.freepik.com/darmowe-wektory/prosty-wibrujacy-kwadratowy-mem-z-kotem_742173-4493.jpg",
        "tags": [],
        "info": {"topics": []}
    }
]

TEST_DATA_UPDATE_INVALID = [
    {
        "id": None,
        "invalid_key": "text_upd",
        "url": "https://img.freepik.com/darmowe-wektory/prosty-wibrujacy-kwadratowy-mem-z-kotem_742173-4493.jpg",
        "tags": ["tag_upd1", "tag_upd2", "tag_upd3"],
        "info": {"topics": ["surprisedUPD", "funnyIPD"]}
    },
    {
        "invalid_key": "text_upd",
        "url": "https://img.freepik.com/darmowe-wektory/"
               "prosty-wibrujacy-kwadratowy-mem-z-kotem_742173-4493.jpg",
        "tags": ["tag_upd1", "tag_upd2", "tag_upd3"],
        "info": {"topics": ["surprisedUPD", "funnyIPD"]}
    }
]

TEST_DATA_UPDATE = {
    "text": "text_upd",
    "url": "https://img.freepik.com/darmowe-wektory/"
           "prosty-wibrujacy-kwadratowy-mem-z-kotem_742173-4493.jpg",
    "tags": ["tag_upd1", "tag_upd2", "tag_upd3"],
    "info": {"topics": ["surprisedUPD", "funnyIPD"]}
}

@pytest.mark.parametrize('data', TEST_DATA_AUTHORIZE_VALID)
def test_authorize(authorize_endpoint, data):
    authorize_endpoint.authorize(payload=data)
    authorize_endpoint.check_that_status_is_200()

@pytest.mark.parametrize("data", TEST_DATA_AUTHORIZE_INVALID)
def test_authorize_negative(authorize_endpoint, data):
    token = authorize_endpoint.authorize(payload=data)
    assert token is None, f"Токен вернулся при невалидных данных: {token}"
    authorize_endpoint.check_that_status_is_400()

@pytest.mark.parametrize('data', TEST_DATA_AUTHORIZE_VALID)
def test_check_token(authorize_endpoint, data):
    authorize_endpoint.authorize(payload=data)
    authorize_endpoint.check_token()
    authorize_endpoint.check_that_status_is_200()

def test_check_token_positive(authorize_endpoint):
    payload = {"name": "user_valid"}
    authorize_endpoint.authorize(payload=payload)
    is_valid = authorize_endpoint.check_token()
    assert is_valid, f"Ожидали True для валидного токена, но получили {is_valid}"

@pytest.mark.parametrize("invalid_token", ["", None, "wrong_token"])
def test_check_token_negative(authorize_endpoint, invalid_token):
    authorize_endpoint.token = invalid_token
    is_valid = authorize_endpoint.check_token()
    assert not is_valid, f"Ожидали False для токена={invalid_token}, но получили {is_valid}"

@pytest.mark.parametrize('data', TEST_DATA_CREATE_VALID)
def test_add_meme(create_meme_endpoint, auth_token, data):
    create_meme_endpoint.create_meme(token=auth_token, payload=data)
    create_meme_endpoint.check_that_status_is_200()
    create_meme_endpoint.check_response_id_is_not_none()

@pytest.mark.parametrize('data', TEST_DATA_CREATE_INVALID)
def test_add_meme_with_invalid_data(create_meme_endpoint, auth_token, data):
    create_meme_endpoint.create_meme(token=auth_token, payload=data)
    create_meme_endpoint.check_that_status_is_400()

@pytest.mark.parametrize('data', TEST_DATA_CREATE_VALID)
def test_add_meme_with_invalid_token(create_meme_endpoint, data):
    create_meme_endpoint.create_meme(token="invalid_token", payload=data)
    create_meme_endpoint.check_that_status_is_401()

@pytest.mark.parametrize('data', TEST_DATA_UPDATE_VALID)
def test_update_meme(put_meme_endpoint, new_meme_id, auth_token, data):
    meme_id = new_meme_id
    data["id"] = meme_id
    put_meme_endpoint.update_meme(token=auth_token, meme_id=meme_id, payload=data)
    put_meme_endpoint.check_that_status_is_200()
    put_meme_endpoint.check_response_text_is_correct("text_upd")

@pytest.mark.parametrize('data', TEST_DATA_UPDATE_VALID)
@pytest.mark.negative
def test_update_meme_with_invalid_token(auth_token, put_meme_endpoint, new_meme_id, data):
    put_meme_endpoint.update_meme(token="invalid_token", meme_id=new_meme_id, payload=data)
    put_meme_endpoint.check_that_status_is_401()

@pytest.mark.parametrize('data', TEST_DATA_UPDATE_INVALID)
@pytest.mark.negative
def test_update_meme_with_invalid_data(auth_token, put_meme_endpoint, new_meme_id, data):
    put_meme_endpoint.update_meme(token=auth_token, meme_id=new_meme_id, payload=data)
    put_meme_endpoint.check_that_status_is_400()

@pytest.mark.negative
def test_update_meme_with_forbidden_access(authorize_endpoint, put_meme_endpoint, meme_created_by_user1):
    meme_id, token_user1 = meme_created_by_user1
    # Авторизуем второго пользователя и пытаемся обновить мем, созданный другим пользователем
    token_user2 = authorize_endpoint.authorize(payload={"name": "user_2"})
    put_meme_endpoint.update_meme(token=token_user2, meme_id=meme_id, payload=TEST_DATA_UPDATE)
    put_meme_endpoint.check_that_status_is_403()

def test_get_memes(auth_token, get_memes_endpoint):
    get_memes_endpoint.get_memes(auth_token)
    get_memes_endpoint.check_that_status_is_200()
    get_memes_endpoint.check_response_is_not_empty()

@pytest.mark.negative
def test_get_memes_with_invalid_token(auth_token, get_memes_endpoint):
    get_memes_endpoint.get_memes(token="invalid_token")
    get_memes_endpoint.check_that_status_is_401()

@pytest.mark.negative
def test_get_memes_without_token(auth_token, get_memes_endpoint):
    get_memes_endpoint.get_memes()
    get_memes_endpoint.check_that_status_is_401()

def test_get_meme_by_id(auth_token, get_meme_by_id_endpoint, new_meme_id):
    get_meme_by_id_endpoint.get_meme_by_id(token=auth_token, meme_id=new_meme_id)
    get_meme_by_id_endpoint.check_that_status_is_200()
    get_meme_by_id_endpoint.check_that_id_is_correct(new_meme_id)

@pytest.mark.negative
def test_get_meme_by_id_with_invalid_token(get_meme_by_id_endpoint, new_meme_id):
    get_meme_by_id_endpoint.get_meme_by_id(token="invalid_token", meme_id=new_meme_id)
    get_meme_by_id_endpoint.check_that_status_is_401()

@pytest.mark.negative
def test_get_meme_returns_404(get_meme_by_id_endpoint, deleted_meme):
    meme_id, token = deleted_meme
    get_meme_by_id_endpoint.get_meme_by_id(token=token, meme_id=meme_id)
    get_meme_by_id_endpoint.check_that_status_is_404()

def test_delete_meme(auth_token, delete_meme_endpoint, new_meme_id):
    delete_meme_endpoint.delete_meme(token=auth_token, meme_id=new_meme_id)
    delete_meme_endpoint.check_that_status_is_200()
    delete_meme_endpoint.check_response_message_is_correct(new_meme_id)

@pytest.mark.negative
def test_delete_meme_with_invalid_token(auth_token, delete_meme_endpoint, new_meme_id):
    delete_meme_endpoint.delete_meme(token="invalid_token", meme_id=new_meme_id)
    delete_meme_endpoint.check_that_status_is_401()
