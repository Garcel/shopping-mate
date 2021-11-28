from rest_framework import viewsets

from .models import ShoppingList
from .serializers import ShoppingListSerializer


class ShoppingListViewSet(viewsets.ModelViewSet):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer

    def get_queryset(self):
        user = self.request.user
        return ShoppingList.objects.filter(owner=user)

    def create(self, request, *args, **kwargs):
        owner = request.user
        request.data._mutable = True
        request.data['owner'] = owner.pk
        request.data._mutable = False

        return super().create(request, *args, **kwargs)
