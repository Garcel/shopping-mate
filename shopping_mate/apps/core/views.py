from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets

from .models import ShoppingList, ShoppingItem
from .serializers import ShoppingListSerializer, ShoppingItemSerializer


@extend_schema_view(
    list=extend_schema(
        summary='LIST ShoppingLists',
        description='List all the Shopping Lists created by the user making the request.',
    ),
    create=extend_schema(
        summary='CREATE ShoppingList',
        description='Create a Shopping Lists with the user making the request as its owner.',
    ),
    retrieve=extend_schema(
        summary='RETRIEVE ShoppingList',
        description='Retrieve a Shopping List created by the user making the request.',
    ),
    destroy=extend_schema(
        summary='DELETE ShoppingList',
        description='Delete a Shopping List created by the user making the request.',
    ),
    update=extend_schema(
        summary='UPDATE ShoppingList',
        description='Update a Shopping List created by the user making the request.',
    ),
    partial_update=extend_schema(
        summary='PARTIAL UPDATE ShoppingList',
        description='Partially update a Shopping List created by the user making the request.',
    ),
)
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


@extend_schema_view(
    list=extend_schema(
        summary='LIST ShoppingItems',
        description='List all the Shopping Items for a list created by the user making the request.',
    ),
    create=extend_schema(
        summary='CREATE ShoppingItem',
        description='Create a Shopping Item into the given list having user making the request as its owner.',
    ),
    retrieve=extend_schema(
        summary='RETRIEVE ShoppingItem',
        description='Retrieve a Shopping Item from a list created by the user making the request.',
    ),
    destroy=extend_schema(
        summary='DELETE ShoppingItem',
        description='Delete a Shopping Item from a list created by the user making the request.',
    ),
    update=extend_schema(
        summary='UPDATE ShoppingItem',
        description='Update a Shopping Item from a list created by the user making the request.',
    ),
    partial_update=extend_schema(
        summary='PARTIAL UPDATE ShoppingItem',
        description='Partially update a Shopping Item from a list created by the user making the request.',
    ),
)
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
