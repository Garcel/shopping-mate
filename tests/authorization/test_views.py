import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from shopping_mate.apps.authentication.models import User
from tests.authorization.factories import UserFactory
from . import data as d


@pytest.mark.django_db
class TestLoginView:
    LOGIN_URL = 'login'

    def test_when_credential_are_invalid_then_return_401(self, client):
        url = reverse(self.LOGIN_URL)

        response = client.post(url, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_when_credential_are_valid_then_return_200_and_the_token(self, client):
        url = reverse(self.LOGIN_URL)
        user: User = UserFactory()
        user.set_password(d.user_password)
        user.save()
        data = {
            'username': user.email,
            'password': d.user_password
        }

        response = client.post(url, data)

        assert response.status_code == status.HTTP_200_OK