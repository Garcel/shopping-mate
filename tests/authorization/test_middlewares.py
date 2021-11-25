from unittest.mock import Mock

import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.request import Request

from shopping_mate.apps.authentication.constants import WWW_AUTH_HEADER, HTTP_AUTHORIZATION_HEADER
from shopping_mate.apps.authentication.middleware import AuthMiddleware
from shopping_mate.apps.authentication.models import User
from tests.authorization.factories import UserFactory


@pytest.fixture
def auth_middleware() -> AuthMiddleware:
    return AuthMiddleware(Mock())

@pytest.mark.django_db
class TestAuthMiddleware:
    def test_excluded_request_bypasses_middleware(self, auth_middleware: AuthMiddleware, middleware_excluded_request):
        request = Mock()
        request.user = None

        assert self.call_auth_middleware(auth_middleware, request) is None
        assert request.user is None

    def test_when_token_is_not_included_in_header_return_401(self, auth_middleware: AuthMiddleware):
        request = Mock()
        request.META = {}

        response = self.call_auth_middleware(auth_middleware, request)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert WWW_AUTH_HEADER in response.headers

    def test_when_included_token_is_invalid_return_401(self, auth_middleware):
        request = Mock()
        request.META = {HTTP_AUTHORIZATION_HEADER: 'cat'}

        response = self.call_auth_middleware(auth_middleware, request)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert WWW_AUTH_HEADER in response.headers

    def test_when_included_token_is_valid_then_nothing_is_returned(self, auth_middleware: AuthMiddleware):
        user: User = UserFactory()
        token, created = Token.objects.get_or_create(user=user)
        request = Mock()
        request.META = {HTTP_AUTHORIZATION_HEADER: token.key}

        assert self.call_auth_middleware(auth_middleware, request) is None
        assert request.user == user

    @staticmethod
    def call_auth_middleware(middleware: AuthMiddleware, request: Request):
        return middleware.process_view(request, Mock(), Mock(), Mock())