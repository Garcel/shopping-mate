from re import sub
from rest_framework.authtoken.models import Token

from .constants import HTTP_AUTHORIZATION_HEADER
from .response import HttpToken401



LOGIN_PATH = '/auth/login/'


class AuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if self.is_excluded(request):
            return

        header_token = request.META.get(HTTP_AUTHORIZATION_HEADER, None)
        if header_token is None:
            return HttpToken401()

        try:
            token = sub('Bearer ', '', request.META.get(HTTP_AUTHORIZATION_HEADER, None))
            token_obj = Token.objects.get(key = token)
            request.user = token_obj.user
        except Token.DoesNotExist:
            return HttpToken401()

    @staticmethod
    def is_excluded(request) -> bool:
        return request.path == LOGIN_PATH