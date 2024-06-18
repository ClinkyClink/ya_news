from http import HTTPStatus
import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture


pytestmark = pytest.mark.django_db
ADMIN = lazy_fixture('admin_client')
AUTHOR = lazy_fixture('author_client')
CLIENT = lazy_fixture('client')
HOME_URL = pytest.lazy_fixture('home_url')
DETAIL_URL = pytest.lazy_fixture('detail_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')
EDIT_URL = pytest.lazy_fixture('edit_url')
DELETE_URL = pytest.lazy_fixture('delete_url')


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (HOME_URL, CLIENT, HTTPStatus.OK),
        (DETAIL_URL, CLIENT, HTTPStatus.OK),
        (LOGIN_URL, CLIENT, HTTPStatus.OK),
        (LOGOUT_URL, CLIENT, HTTPStatus.OK),
        (SIGNUP_URL, CLIENT, HTTPStatus.OK),
        (EDIT_URL, AUTHOR, HTTPStatus.OK),
        (DELETE_URL, AUTHOR, HTTPStatus.OK),
        (EDIT_URL, ADMIN, HTTPStatus.NOT_FOUND),
        (DELETE_URL, ADMIN, HTTPStatus.NOT_FOUND),
    ),
)
def test_pages_available_for_anonymous_user(
    url, parametrized_client, expected_status, comment
):
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url, login_url, expected_status',
    [
        (EDIT_URL, '/auth/login/', HTTPStatus.FOUND),
        (DELETE_URL, '/auth/login/', HTTPStatus.FOUND)]
)
def test_redirect_for_anonymous_client(client,
                                       url,
                                       login_url,
                                       comment,
                                       expected_status):
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url, status_code=expected_status)
