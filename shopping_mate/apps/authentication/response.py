from django.http import HttpResponse
from rest_framework import status

from .constants import WWW_AUTH_HEADER


class HttpBasic401(HttpResponse):
    def __init__(self):
        super().__init__('401 Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        self[WWW_AUTH_HEADER] = 'Basic'
