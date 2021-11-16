from shopping_mate.apps.authentication.models import User


def assert_user_created(user: User, user_data: dict):
    assert user is not None
    assert user.pk is not None
    assert user.email ==user_data.get('email')
    assert user.first_name == user_data.get('first_name')
    assert user.last_name == user_data.get('last_name')
