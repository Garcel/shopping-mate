from datetime import datetime

from shopping_mate.apps.core.constants import DATETIME_FORMAT

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
    "due_date": datetime.strptime("29/01/22 15:00:00", DATETIME_FORMAT)
}

shopping_item_with_list = {
    "name": "shopping list test",
    "description": "My description test",
    "owner": 2,
    "list": 999
}
