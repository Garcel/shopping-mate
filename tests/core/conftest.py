import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from shopping_mate.apps.authentication.models import User
from tests.authorization.factories import UserFactory


@pytest.fixture()
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user_token() -> (User, Token):
    user: User = UserFactory()
    token, created = Token.objects.get_or_create(user=user)

    return user, token
