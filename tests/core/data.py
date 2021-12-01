import datetime

from django.utils import timezone

shopping_list = {
    "name": "shopping list test",
    "description": "My description test"
}

shopping_item_without_due_date = {
    "name": "shopping list test",
    "description": "My description test",
    "due_date": timezone.now() + datetime.timedelta(1)
}

shopping_item = {
    **shopping_item_without_due_date,
    "due_date": timezone.now() + datetime.timedelta(1)
}
