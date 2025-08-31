import pytest

TEST_DATA = [
    {
        "text": "cat new aug",
        "url": "https://img.freepik.com/darmowe-wektory/prosty-wibrujacy-kwadratowy-mem-z-kotem_742173-4493.jpg",
        "tags": ["one", "two", "five"],
        "info": {"topics": ["boring", "happy"]}
    }
]

NEGATIVE_DATA = [
    {
        "text": 1,
        "url": "https://img.freepik.com/darmowe-wektory/prosty-wibrujacy-kwadratowy-mem-z-kotem_742173-4493.jpg",
        "tags": ["one", "two", "five"],
        "info": {"topics": ["surprised", "funny"]}
    }
]


def test_update_meme(authorize_endpoint, put_meme_endpoint, new_meme_id):
    token = authorize_endpoint.authorize()
    put_meme_endpoint.update_meme(token=token, meme_id=new_meme_id)
    put_meme_endpoint.check_that_status_is_200()


@pytest.mark.negative
def test_update_meme_with_invalid_token(authorize_endpoint, put_meme_endpoint, new_meme_id):
    put_meme_endpoint.update_meme(token="invalid_token", meme_id=new_meme_id)
    put_meme_endpoint.check_that_status_is_401()


@pytest.mark.negative
def test_update_meme_with_forbidden_access(authorize_endpoint, put_meme_endpoint, new_meme_id):
    token = authorize_endpoint.authorize()
    put_meme_endpoint.update_meme(token=token, meme_id=67)
    put_meme_endpoint.check_that_status_is_403()


@pytest.mark.negative
def test_update_meme_with_invalid_data(authorize_endpoint, put_meme_endpoint, new_meme_id):
    token = authorize_endpoint.authorize()
    put_meme_endpoint.update_meme(token=token) # не передали обязательное поле id
    put_meme_endpoint.check_that_status_is_404()


def test_update_meme_updated_values(authorize_endpoint, put_meme_endpoint, new_meme_id):
    token = authorize_endpoint.authorize()
    put_meme_endpoint.update_meme(token=token, meme_id=new_meme_id)
    put_meme_endpoint.check_response_text_is_correct("text_upd")


@pytest.mark.parametrize('data', TEST_DATA)
def test_add_meme(authorize_endpoint, create_meme_endpoint, data):
    token = authorize_endpoint.authorize()
    create_meme_endpoint.create_meme(token=token, payload=data)
    create_meme_endpoint.check_that_status_is_200()


@pytest.mark.parametrize('data', TEST_DATA)
def test_add_meme_with_invalid_token(authorize_endpoint, create_meme_endpoint, data):
    create_meme_endpoint.create_meme(token="invalid_token", payload=data)
    create_meme_endpoint.check_that_status_is_401()


@pytest.mark.parametrize('data', NEGATIVE_DATA)
def test_add_meme_with_invalid_data(authorize_endpoint, create_meme_endpoint, data):
    token = authorize_endpoint.authorize()
    create_meme_endpoint.create_meme(token=token, payload=data)
    create_meme_endpoint.check_that_status_is_400()


def test_get_memes(authorize_endpoint, get_memes_endpoint):
    token = authorize_endpoint.authorize()
    get_memes_endpoint.get_memes(token)
    get_memes_endpoint.check_that_status_is_200()


@pytest.mark.negative
def test_get_memes_with_invalid_token(authorize_endpoint, get_memes_endpoint):
    get_memes_endpoint.get_memes(token="invalid_token")
    get_memes_endpoint.check_that_status_is_401()


@pytest.mark.negative
def test_get_memes_without_token(get_memes_endpoint):
    get_memes_endpoint.get_memes()   # без токена
    get_memes_endpoint.check_that_status_is_401()


def test_get_meme_by_id(authorize_endpoint, get_meme_by_id_endpoint, new_meme_id):
    token = authorize_endpoint.authorize()
    get_meme_by_id_endpoint.get_meme_by_id(token=token, meme_id=new_meme_id)
    get_meme_by_id_endpoint.check_that_status_is_200()


@pytest.mark.negative
def test_get_meme_by_id_with_invalid_token(authorize_endpoint, get_meme_by_id_endpoint, new_meme_id):
    get_meme_by_id_endpoint.get_meme_by_id(token="invalid_token")
    get_meme_by_id_endpoint.check_that_status_is_401()


@pytest.mark.negative
def test_get_meme_by_id_not_found(authorize_endpoint, get_meme_by_id_endpoint, new_meme_id):
    token = authorize_endpoint.authorize()
    get_meme_by_id_endpoint.get_meme_by_id(token=token, meme_id=50000)
    get_meme_by_id_endpoint.check_that_status_is_404()


def test_delete_meme(authorize_endpoint, delete_meme_endpoint, new_meme_id):
    token = authorize_endpoint.authorize()
    delete_meme_endpoint.delete_meme(token=token, meme_id=new_meme_id)
    delete_meme_endpoint.check_that_status_is_200()


@pytest.mark.negative
def test_delete_meme_with_invalid_token(authorize_endpoint, delete_meme_endpoint, new_meme_id):
    authorize_endpoint.authorize()
    delete_meme_endpoint.delete_meme(token="invalid_token", meme_id=new_meme_id)
    delete_meme_endpoint.check_that_status_is_401()
