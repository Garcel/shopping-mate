from rest_framework import viewsets

from .models import ShoppingList, ShoppingItem
from .serializers import ShoppingListSerializer, ShoppingItemSerializer


class ShoppingListViewSet(viewsets.ModelViewSet):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer

    def get_queryset(self):
        user = self.request.user
        return ShoppingList.objects.filter(owner=user)

    def create(self, request, *args, **kwargs):
        owner = request.user
        request.data['owner'] = owner.pk

        return super().create(request, *args, **kwargs)


class ShoppingItemViewSet(viewsets.ModelViewSet):
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer

    def get_queryset(self):
        user = self.request.user
        return ShoppingItem.objects.filter(list__owner=user)

    def create(self, request, *args, **kwargs):
        owner = request.user
        request.data['list'] = kwargs['list_pk']
        request.data['owner'] = owner.pk

        return super().create(request, *args, **kwargs)
