from rest_framework import serializers

from .constants import DATETIME_FORMAT
from .models import ShoppingList, ShoppingItem


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ['name', 'description', 'owner', 'creation_date', 'last_update']

    creation_date = serializers.DateTimeField(format=DATETIME_FORMAT, read_only=True)
    last_update = serializers.DateTimeField(format=DATETIME_FORMAT, read_only=True)

    def validate_owner_id(self, value):
        if self.instance and value != self.instance.owner.pk:
            raise serializers.ValidationError("Owner id is immutable once set.")

        return value


class ShoppingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingItem
        fields = ['name', 'description', 'data', 'list', 'creation_date', 'last_update', 'due_date']

    creation_date = serializers.DateTimeField(format=DATETIME_FORMAT, read_only=True)
    due_date = serializers.DateTimeField(format=DATETIME_FORMAT)
    last_update = serializers.DateTimeField(format=DATETIME_FORMAT, read_only=True)

    def validate_list_id(self, value):
        if self.instance and value != self.instance.list.pk:
            raise serializers.ValidationError("List id is immutable once set.")

        return value