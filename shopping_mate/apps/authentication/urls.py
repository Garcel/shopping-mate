from django.urls import path

from shopping_mate.apps.authentication.views import CustomAuthToken

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='login'),
]
