import jwt
from django.conf import settings
from django.utils import timezone
import random
import string

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import CustomUser


class CustomAuthentication(BaseAuthentication):
    '''Custom DRF authentication using PyJWT.'''

    def authenticate(self, request):
        '''Authenticates incoming user request.'''
        context = {}
        client_token = request.META.get('HTTP_AUTHORIZATION', None)

        if not client_token:
            context['status'] = 'error'
            context['message'] = 'Authorization bearer token required.'
            raise exceptions.AuthenticationFailed(context)

        token = client_token[7:]

        # verify token
        decoded_data = self.verify_token(token)

        if not decoded_data:
            context['status'] = 'error'
            context['message'] = 'Invalid or expired token provided.'
            raise exceptions.AuthenticationFailed(context)
        return self.get_user(decoded_data['user_id']), None

    def get_user(self, user_id):
        '''Retrieves user using provided id.'''
        try:
            user = CustomUser.objects.get(id=user_id)
        except Exception:
            return None

        return user

    def verify_token(self, token):
        '''Verify provided bearer token.'''
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
        except Exception:
            return None

        # verify if token is expired
        exp = decoded_token['exp']

        if timezone.now().timestamp() > exp:
            return None

        return decoded_token

    def get_random(self, len):
        '''Generates a random string of given length.'''
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=len))

    def get_access_token(self, payload):
        '''Returns an access token for user sign in.'''
        return jwt.encode(
            {"exp": timezone.now() + timezone.timedelta(minutes=30), **payload},
            settings.SECRET_KEY,
            algorithm="HS256"
        )

    def get_refresh_token(self):
        '''Returns a refresh token for user sign in.'''
        return jwt.encode(
            {"exp": timezone.now() + timezone.timedelta(days=1), "data": self.get_random(10)},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
