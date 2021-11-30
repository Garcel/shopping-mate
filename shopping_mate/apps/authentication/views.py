from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from shopping_mate.apps.authentication.response import HttpBasic401


@extend_schema_view(
    post=extend_schema(
        summary='User login',
        description='Allows users to login.',
    ),
)
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        if not serializer.is_valid():
            return HttpBasic401()

        user = serializer.validated_data['user']
        Token.objects.filter(user=user).delete()
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.email
        })
