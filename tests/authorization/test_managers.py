import pytest

from shopping_mate.apps.authentication.models import User
from . import data as d
from .helpers import assert_user_created


@pytest.mark.django_db
class TestVanillaUserCreation:
    def test_when_staff_enabled_for_vanilla_user_then_raise_value_error(self):
        with pytest.raises(ValueError):
            User.objects.create_vanilla_user(**d.staff_user)

    def test_when_superuser_enabled_for_vanilla_user_then_raise_value_error(self):
        with pytest.raises(ValueError):
            User.objects.create_vanilla_user(**d.superuser)

    def test_when_missing_email_then_raise_value_error(self):
        with pytest.raises(ValueError):
            User.objects.create_vanilla_user(**d.vanilla_user_none_email)

    def test_when_success_then_a_user_object_is_returned(self):
        user = User.objects.create_vanilla_user(**d.vanilla_user)

        assert_user_created(user, d.vanilla_user)

@pytest.mark.django_db
class TestStaffUserCreation:
    def test_when_superuser_enabled_for_staff_user_then_raise_value_error(self):
        with pytest.raises(ValueError):
            User.objects.create_staff_user(**d.superuser)

    def test_when_success_then_a_user_object_is_returned(self):
        user = User.objects.create_staff_user(**d.staff_user)

        assert_user_created(user, d.staff_user)

@pytest.mark.django_db
class TestSuperuserCreation:
    def test_when_success_then_a_user_object_is_returned(self):
        user = User.objects.create_superuser(**d.superuser)

        assert_user_created(user, d.superuser)
        assert user.is_staff
