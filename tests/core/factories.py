import factory
from faker import Faker

from shopping_mate.apps.core.models import ShoppingList, ShoppingItem
from ..authorization import factories as auth_factories

fake = Faker()


class ShoppingListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShoppingList

    name = factory.Sequence(lambda n: f'ShoppingList{n}')
    owner = factory.SubFactory(auth_factories.UserFactory)


class ShoppingItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShoppingItem

    name = factory.Sequence(lambda n: f'ShoppingItem{n}')
    list = factory.SubFactory(ShoppingListFactory)
