'''
Tests all notification API endpoints.
'''

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from notification.models import Notification, NotificationType


GET_ALL_NOTIFICATIONS = reverse('notification:all_notifications')
GET_UNREAD_NOTIFICATIONS = reverse('notification:unread_notifications')
MARK_NOTIFICATION_READ = reverse('notification:mark_notification_read', args=[1])
CLEAR_ALL_NOTIFICATION = reverse('notification:clear_all_notifications')


# function for creating new user account
def create_user(**params):
    '''Creates and return a new user account.'''
    return get_user_model().objects.create_user(**params)


class NotificationTests(TestCase):
    '''Tests all notification app API endpoints privately.'''

    def setUp(self):
        self.user = get_user_model().objects.create(
            first_name='Ephraim',
            last_name='Daniel',
            email='test@gmail.com',
            password='MyPass12345',
            accepted_terms=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_all_notification_endpoint(self):
        '''Tests the all notification API endpoint.'''
        response = self.client.get(GET_ALL_NOTIFICATIONS)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_unread_notification_endpoint(self):
        '''Tests the unread notification API endpoint.'''
        response = self.client.get(GET_UNREAD_NOTIFICATIONS)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_notification_read_endpoint(self):
        '''Tests the mark notificationa read API endpoint.'''
        type = NotificationType.objects.create(name="Message read")
        Notification.objects.create(
            user_id = self.user,
            type = type,
            message = 'Testing message'

        )
        response = self.client.get(MARK_NOTIFICATION_READ)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_clear_notifications_endpoint(self):
        '''Tests clear all notifications API endpoint.'''
        response = self.client.get(CLEAR_ALL_NOTIFICATION)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class NoAuthNotificationTests(TestCase):
    '''Tests all notification API endpoints publicly.'''

    def setUp(self):
        self.client = APIClient()

    def test_get_all_notification(self):
        '''Tests the get all notification API endpoint without authorization.'''
        response = self.client.get(GET_ALL_NOTIFICATIONS)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_unread_notification(self):
        '''Tests the get all unread notification API endpoint without authorization.'''
        response = self.client.get(GET_UNREAD_NOTIFICATIONS)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mark_notification_read(self):
        '''Tests the mark notification read API endpoint without authorization.'''
        response = self.client.get(MARK_NOTIFICATION_READ)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_clear_notifications(self):
        '''Tests the clear all notifications API endpoint without authorization.'''
        response = self.client.get(CLEAR_ALL_NOTIFICATION)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
