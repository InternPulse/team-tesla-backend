'''
Tests all invoice_generation API endpoints.
'''
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


GET_ALL_USER_CLIENTS = reverse('invoice_generation:get_user_clients')
POST_USER_CLIENT_INVOICE = reverse('invoice_generation:post_user_clients_invoice')
GET_CLIENT_DETAIL = reverse('invoice_generation:get_client_detail', args=[1])
GET_USER_CLIENT_INVOICE = reverse('invoice_generation:get_user_client_invoice')
GET_INVOICE_DETAIL = reverse('invoice_generation:get_invoice_detail', args=[1])


# function for creating new user account
def create_user(**params):
    '''Creates and return a new user account.'''
    return get_user_model().objects.create_user(**params)


class ClientInvoiceTests(TestCase):
    '''Tests all invoice_generation app API endpoints with authorization.'''

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

    def test_get_user_clients_endpoint(self):
        '''Tests get user clients API endpoint.'''
        response = self.client.get(GET_ALL_USER_CLIENTS)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_client_detail_endpoint(self):
        '''Tests get client invoice API endpoint.'''

        payload = {
            "title": "1",
            "first_name": "Ephraim",
            "last_name": "Daniel",
            "company_name": "Larja Inc",
            "customer_email": "user@example.com",
            "work_phone": "7682154",
            "personal_phone": "6571242"
        }

        self.client.post(GET_ALL_USER_CLIENTS, payload)

        response = self.client.get(GET_CLIENT_DETAIL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_client_invoice_endpoint(self):
        '''Tests user client invoice API endpoint.'''

        response = self.client.get(GET_USER_CLIENT_INVOICE)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invoice_detail_endpoint(self):
        '''Tests invoice detail API endpoint.'''
        # Create a client
        payload = {
            "title": "1",
            "first_name": "Ephraim",
            "last_name": "Daniel",
            "company_name": "Larja Inc",
            "customer_email": "user@example.com",
            "work_phone": "7682154",
            "personal_phone": "6571242"
        }

        self.client.post(GET_ALL_USER_CLIENTS, payload)

        # Create an invoice
        payload = {
            "client_id": 1,
            "transaction_id": "gyd674rt73g6t72re",
            "amount": "1000",
            "description": "string description",
            "customer_note": "string customer note",
            "draft": False,
            "status": "success",
            "due_at": "2024-01-25"
        }
        self.client.post(POST_USER_CLIENT_INVOICE, payload)

        response = self.client.get(GET_INVOICE_DETAIL)

        # Assert the response and the updated values
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invoice_detail_endpoint(self):
        '''Tests invoice detail API endpoint.'''
        # Create a client
        payload = {
            "title": "1",
            "first_name": "Ephraim",
            "last_name": "Daniel",
            "company_name": "Larja Inc",
            "customer_email": "user@example.com",
            "work_phone": "7682154",
            "personal_phone": "6571242"
        }

        self.client.post(GET_ALL_USER_CLIENTS, payload)

        # Create an invoice
        payload = {
            "client_id": 1,
            "transaction_id": "gyd674rt73g6t72re",
            "amount": "1000",
            "description": "string description",
            "customer_note": "string customer note",
            "draft": False,
            "status": "success",
            "due_at": "2024-01-25"
        }
        self.client.post(POST_USER_CLIENT_INVOICE, payload)

        payload = {
            "client_id": 1,
            "transaction_id": "hgjhgjgygjgjg",
            "amount": "1000",
            "description": "string description",
            "customer_note": "string customer note",
            "draft": False,
            "status": "success",
            "due_at": "2024-01-25"
        }

        response = self.client.put(GET_INVOICE_DETAIL, payload)

        # Assert the response and the updated values
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['transaction_id'], 'hgjhgjgygjgjg')

    def test_update_client_detail_endpoint(self):
        '''Tests invoice detail API endpoint.'''
        # Create a client
        payload = {
            "title": "1",
            "first_name": "Ephraim",
            "last_name": "Daniel",
            "company_name": "Larja Inc",
            "customer_email": "user@example.com",
            "work_phone": "7682154",
            "personal_phone": "6571242"
        }

        self.client.post(GET_ALL_USER_CLIENTS, payload)

        payload = {
            "title": "1",
            "first_name": "Ephraim",
            "last_name": "Daniel",
            "company_name": "Larja Inc",
            "customer_email": "update@example.com",
            "work_phone": "7682154",
            "personal_phone": "6571242"
        }

        response = self.client.put(GET_CLIENT_DETAIL, payload)

        # Assert the response and the updated values
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_email'], 'update@example.com')


class NoAuthClientInvoiceTests(TestCase):
    '''Tests all invoice_generation API endpoints publicly.'''

    def setUp(self):
        self.client = APIClient()

    def test_get_user_clients(self):
        '''Tests get all user clients API endpoint without authorization.'''
        response = self.client.get(GET_ALL_USER_CLIENTS)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_client_detail(self):
        '''Tests the get client detail API endpoint without authorization.'''
        response = self.client.get(GET_CLIENT_DETAIL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_client_invoice(self):
        '''Tests get user client invoice endpoint without authorization.'''
        response = self.client.get(GET_USER_CLIENT_INVOICE)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_invoice_detail(self):
        '''Tests the get invoice detail without authorization.'''
        response = self.client.get(GET_INVOICE_DETAIL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
