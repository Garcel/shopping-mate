from unittest.mock import patch

import pytest


@pytest.fixture
def middleware_excluded_request():
    with patch('shopping_mate.apps.authentication.middleware.AuthMiddleware.is_excluded', return_value=True):
        yield
