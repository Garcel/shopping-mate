import datetime

from django.utils import timezone

shopping_list = {
    "name": "shopping list test",
    "description": "My description test"
}

shopping_list_with_owner = {
    "name": "shopping list test",
    "description": "My description test",
    "owner": 2
}

shopping_item = {
    "name": "shopping list test",
    "description": "My description test",
    "due_date": timezone.now() + datetime.timedelta(1)
}

shopping_item_with_list = {
    "name": "shopping list test",
    "description": "My description test",
    "owner": 2,
    "list": 999
}
