from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularRedocView, SpectacularAPIView, SpectacularSwaggerView

from shopping_mate.apps.core import urls as core_urls

urlpatterns = [
    path('', include(core_urls)),
    path('auth/', include('shopping_mate.apps.authentication.urls')),
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'apidoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
]
