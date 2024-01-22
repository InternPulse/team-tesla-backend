'''Serializers for the user account API View'''

from django.contrib.auth import get_user_model
from rest_framework import serializers


class SignUpSerializer(serializers.ModelSerializer):
    '''Serialiser for user account.'''

    class Meta:
        model = get_user_model()
        fields = ['email', 'email_verified', 'accepted_terms', 'business', 'password']
        extra_kwargs = {
            'email': {'write_only': True},
            'email_verified': {'write_only': True},
            'accepted_terms': {'write_only': True},
            'business': {'write_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        '''Create and return a user account'''
        return get_user_model().objects.create_user(**validated_data)


class SignInSerializer(serializers.Serializer):
    '''Serializer for user login.'''
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=True,
    )


class RefreshTokenSerializer(serializers.Serializer):
    '''Refresh token serializer.'''
    refresh = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    '''User profile serializer.'''

    class Meta:
        model = get_user_model()
        fields = ['email', 'email_verified', 'accepted_terms', 'business']
        extra_kwargs = {
            'email': {'read_only': True},
            'email_verified': {'read_only': True},
            'accepted_terms': {'read_only': True},
            'business': {'read_only': True}
        }
