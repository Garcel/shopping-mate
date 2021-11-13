from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('auth/', include('shopping_mate.apps.authentication.urls')),
    path('admin/', admin.site.urls),
]
