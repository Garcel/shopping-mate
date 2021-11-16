import factory
from faker import Faker

from shopping_mate.apps.authentication.models import User

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Sequence(lambda n: f'User{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.first_name}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')