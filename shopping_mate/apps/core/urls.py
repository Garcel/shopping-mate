from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'lists', views.ShoppingListViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lists/<int:list_pk>/items', views.ShoppingItemViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='item-list'),
    path('items/<int:pk>', views.ShoppingItemViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'update',
        'patch': 'partial_update'
    }), name='item-detail')
]
