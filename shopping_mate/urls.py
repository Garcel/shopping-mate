from django.contrib import admin
from django.urls import path, include

from shopping_mate.apps.core import urls as core_urls

urlpatterns = [
    path('', include(core_urls)),
    path('auth/', include('shopping_mate.apps.authentication.urls')),
    path('admin/', admin.site.urls),
]
