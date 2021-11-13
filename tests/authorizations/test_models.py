import pytest

from shopping_mate.apps.authentication.models import User
from . import data as d


@pytest.mark.django_db
class TestUser:
    def test_get_full_name_returns_the_full_name(self):
        user = User.objects.create_vanilla_user(**d.vanilla_user)

        assert user.get_full_name() == f'{d.vanilla_user.get("first_name")} {d.vanilla_user.get("last_name")}'

    def test_get_short_name_returns_the_first_name(self):
        user = User.objects.create_vanilla_user(**d.vanilla_user)

        assert user.get_short_name() == d.vanilla_user.get("first_name")