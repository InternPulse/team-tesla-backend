'''
Views for user API.
'''
from django.db import transaction
from django.contrib.auth import authenticate

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from account.models import Token
from account.models import CustomUser

from .authentication import CustomAuthentication

from account.serializers import (
        SignUpSerializer,
        SignInSerializer,
        RefreshTokenSerializer,
        ProfileSerializer,
    )


class SignUpView(APIView):
    '''Creates a new user in database.'''
    serializer_class = SignUpSerializer

    def post(self, request):
        context = {}

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        context['status'] = 'success'
        context['message'] = 'Account created successfully.'
        context.update(serializer.data)

        return Response(context, status.HTTP_201_CREATED)

class SignInView(APIView):
    '''Sign in user with valid credential'''
    serializer_class = SignInSerializer
    auth = CustomAuthentication()

    def post(self, request):
        '''User validation and authentication.'''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if user is None:
            return Response({
                'status': 'error',
                'message': 'Invalid account credentials'
            }, status=400)

        access = self.auth.get_access_token({'user_id': user.id})
        refresh = self.auth.get_refresh_token()

        # check if user have prev tokens & then delete it
        Token.objects.filter(user_id=user).delete()

        # create tokens for user
        Token.objects.create(
            user_id=user,
            access=access,
            refresh=refresh
        )

        response = Response({
            'status': 'success',
            'access_token': access
        })

        # cookie setting
        response.set_cookie(
            'refresh_token', refresh, secure=True, samesite='None', max_age=86400
        )

        return response


class RefreshTokenView(APIView):
    '''Provides a new access token for user.'''

    auth = CustomAuthentication()

    def get(self, request):
        '''Creates new tokens for user with valid refresh token.'''
        refresh_token_cookie = request.COOKIES.get('refresh_token') # get cookies

        try:
            active_token = Token.objects.get(refresh=refresh_token_cookie)
        except Token.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Refresh token not found.'
            }, status=400)

        if not self.auth.verify_token(refresh_token_cookie):
            return Response({
                'status': 'error',
                'message': 'Refresh token invalid or expired.'
            }, status=400)

        access = self.auth.get_access_token({'user_id': active_token.id})
        refresh = self.auth.get_refresh_token()

        active_token.access = access
        active_token.refresh = refresh

        active_token.save()

        response = Response({
            'status': 'success',
            'access_token': access
        })

        # cookie setting
        response.set_cookie(
            'refresh_token', refresh, secure=True, samesite='None', max_age=86400
        )

        return response


class ProfileView(APIView):
    '''Returns user profile.'''
    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProfileSerializer

    def get(self, request):
        context = {}
        serializer = self.serializer_class(request.user)
        context['status'] = 'success'
        context.update(serializer.data)

        return Response(context)

    def put(self, request):
        context = {}
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            context['status'] = 'success'
            context.update(serializer.data)
            return Response(context, status.HTTP_200_OK)

        context['status'] = 'error'
        context.update(serializer.errors)

        return Response(context, status.HTTP_400_BAD_REQUEST)
