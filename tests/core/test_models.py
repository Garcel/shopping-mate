import datetime

import pytest
from django.utils import timezone

from shopping_mate.apps.core.models import ShoppingItem
from . import factories as f


@pytest.mark.django_db
class TestShoppingItem:
    def test_get_seconds_to_expiration_returns_zero_when_due_date_is_none(self):
        item: ShoppingItem = f.ShoppingItemFactory()

        assert item.due_date is None
        assert item.get_seconds_to_expiration() is None

    @pytest.mark.freeze_time('2021-08-31')
    def test_get_seconds_to_expiration_returns_seconds_to_expiration_when_due_date_is_none(self):
        item: ShoppingItem = f.ShoppingItemFactory(due_date=timezone.now() + datetime.timedelta(1))

        assert item.due_date is not None
        assert item.get_seconds_to_expiration() == 86400.0