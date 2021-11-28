from rest_framework import serializers

from .constants import DATETIME_FORMAT
from .models import ShoppingList


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
