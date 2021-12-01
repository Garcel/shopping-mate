from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

def authenticate_user(client: APIClient, token: Token):
    client.credentials(HTTP_AUTHORIZATION=f"{TokenAuthentication.keyword} {token.key}")

    return client