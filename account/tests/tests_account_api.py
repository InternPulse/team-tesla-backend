'''
Tests for the user account API.
'''

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
# import time

from rest_framework.test import APIClient
from rest_framework import status


SIGN_UP_URL = reverse('account:sign_up')
SIGN_IN_URL = reverse('account:sign_in')
REFRESH_TOKEN_URL = reverse('account:refresh_token')
PROFILE_URL = reverse('account:profile')


# function for creating new user account
def create_user(**params):
    '''Create and return a new user.'''
    return get_user_model().objects.create_user(**params)


class AccountAPITests(TestCase):
    '''Test the features of the user account API.'''

    def setup(self):
        self.client = APIClient()

    def test_signup_user_account(self):
        '''Test signing up a new user'''
        user_details = {
            'email': 'test@gmail.com',
            'password': 'MyPass12345',
            'accepted_terms': True
        }

        response = self.client.post(SIGN_UP_URL, user_details)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=user_details['email'])
        self.assertTrue(user.accepted_terms)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password(user_details['password']))

    def test_signin_user_account(self):
        '''Test token generation for valid user.'''
        user_details = {
            'email': 'test@gmail.com',
            'password': 'MyPass12345'
        }
        create_user(**user_details)

        payload = {
            'email': 'test@gmail.com',
            'password': 'MyPass12345'
        }
        response = self.client.post(SIGN_IN_URL, payload)

        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.cookies)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        refresh_token_cookie = response.cookies['refresh_token']

        self.assertEqual(refresh_token_cookie['max-age'], 86400)

    def test_generate_token_with_bad_credentials(self):
        '''Test returns error if invalid credential is provided'''

        payload = {
            'email':'test1@gmail.com'
        }
        response = self.client.post(SIGN_IN_URL, payload)

        self.assertNotIn('access_token', response.data)
        self.assertNotIn('refresh_token', response.cookies)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_email_address_provided(self):
        '''Test returns error if no email is provided'''
        payload = {
            'email':'',
        }
        response = self.client.post(SIGN_IN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access_token', response.data)

    def test_get_new_access_token(self):
        '''Test returns new access in response and refresh token in cookie for user'''
        user_details = {
            'email': 'test@gmail.com',
            'password': 'MyPass12345'
        }
        create_user(**user_details)

        payload = {
            'email': 'test@gmail.com',
            'password': 'MyPass12345'
        }

        response = self.client.post(SIGN_IN_URL, payload)

        payload = {
            'refresh': response.cookies['refresh_token'],
        }
        
        response2 = self.client.get(REFRESH_TOKEN_URL, payload)

        self.assertIn('access_token', response2.data)
        self.assertIn('refresh_token', response2.cookies)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_retrieve_user_unauthorized(self):
        '''Test user authentication required.'''
        response = self.client.get(PROFILE_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProfileAPITests(TestCase):
    '''Test API requests that require user authentication.'''

    def setUp(self):
        self.user = create_user(
            email = 'test@gmail.com',
            password = 'MyPass12345',
            accepted_terms = True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_authenticated_user_success(self):
        '''Test retrieve profile for signed in user.'''
        response = self.client.get(PROFILE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['accepted_terms'], self.user.accepted_terms)
        self.assertEqual(response.data['business'], self.user.business)

    def test_post_in_profile(self):
        '''Test POST request not allowed for the profile endpoint.'''
        response = self.client.post(PROFILE_URL, {})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
