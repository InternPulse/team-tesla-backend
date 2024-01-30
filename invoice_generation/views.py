'''
Views for invoice generation app
'''
import pdfkit
import random
import string
from datetime import datetime

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import exceptions

from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import Client, Invoice
from .serializers import ClientSerializer, InvoiceSerializer, ListInvoiceSerializer
from account.authentication import CustomAuthentication
from notification.notify import notify_user


class AllUserClientsView(APIView):
    '''Returns all clients associated with user and create one for user'''

    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer

    def get(self, request):
        '''Get list of all user clients'''
        clients = Client.objects.filter(user_id=request.user)
        serializer = self.serializer_class(clients, context={'request': request}, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        '''Add client for a user'''
        context = {}

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user)

            context['status'] = 'success'
            context['message'] = 'Client created successful'
            context.update(serializer.data)
            notify_user(request.user, 'client-success', context['message'])
            return Response(context, status=status.HTTP_200_OK)

        context['status'] = 'error'
        context.update(serializer.errors)
        notify_user(request.user, 'client-failure', 'Client failed to create')

        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    

class GetUpdateClientView(APIView):
    '''Returns client details and  associated with user'''

    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer

    def get_object(self, request, pk):
        context = {}
        try:
            client = Client.objects.get(user_id=request.user, pk=pk)
            return client
        except Client.DoesNotExist:
            context['status'] = 'error'
            context['message'] = 'Client not found'
            return exceptions.ParseError(context)
        
    def get(self, request, pk):
        '''Gets the details for a client'''
        context = {}

        client = self.get_object(request, pk)
        serializer = self.serializer_class(client)
        context['status'] = 'success'
        context.update(serializer.data)

        return Response(context, status.HTTP_200_OK)

    def put(self, request, pk):
        '''Update detail of a client'''
        context = {}

        client = self.get_object(request, pk)
        serializer = self.serializer_class(client, data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user,)

            context['status'] = 'success'
            context['message'] = 'Client updated successful'
            context.update(serializer.data)
            notify_user(request.user, 'client-updated', context['message'])
            return Response(context, status=status.HTTP_200_OK)

        context['status'] = 'error'
        context.update(serializer.errors)
        notify_user(request.user, 'client-failure', 'Client failed to update')

        return Response(context, status=status.HTTP_400_BAD_REQUEST)


def transaction_id(tag='iv'):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[12:-1]  # Format: YYYYMMDDHHMMSSmmm
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{tag}{timestamp}{random_string}"


class CreateClientInvoiceView(APIView):
    '''Returns all and create invoices associated with user and client'''

    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer

    def post(self, request):
        '''Create invoice for a client and user'''
        context = {}

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            invoice_no = transaction_id()
            serializer.save(user_id=request.user, transaction_id=invoice_no)

            context['status'] = 'success'
            context['message'] = 'Invoice created successful'
            context.update(serializer.data)
            notify_user(request.user, 'invoice-success', context['message'])
            return Response(context, status=status.HTTP_200_OK)

        context['status'] = 'error'
        context.update(serializer.errors)
        notify_user(request.user, 'invoice-failure', 'Invoice failed to create')

        return Response(context, status=status.HTTP_400_BAD_REQUEST)


class GetUpdateInvoiceView(APIView):
    '''Returns invoice details associated with a client and user'''

    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer

    def get_object(self, request, pk):
        context = {}
        try:
            invoice = Invoice.objects.get(pk=pk, user_id=request.user)
            return invoice
        except Client.DoesNotExist:
            context['status'] = 'error'
            context['message'] = 'Invoice not found'
            return exceptions.ParseError(context)

    def get(self, request, pk):
        '''Gets the details for a client'''
        context = {}

        invoice = self.get_object(request, pk)
        serializer = self.serializer_class(invoice)
        context['status'] = 'success'
        context.update(serializer.data)

        return Response(context, status.HTTP_200_OK)


    def put(self, request, pk):
        '''Update detail of a client'''
        context = {}

        invoice = self.get_object(request, pk)
        serializer = self.serializer_class(invoice, data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user,)

            context['status'] = 'success'
            context['message'] = 'Invoice updated successful'
            context.update(serializer.data)
            notify_user(request.user, 'invoice-updated', context['message'])
            return Response(context, status=status.HTTP_200_OK)

        context['status'] = 'error'
        context.update(serializer.errors)
        notify_user(request.user, 'invoice-failure', 'Client failed to update')

        return Response(context, status=status.HTTP_400_BAD_REQUEST)


class AllUserClientInvoiceView(APIView):
    '''Returns all and create invoices associated with user and client'''

    authentication_classes = [CustomAuthentication,]
    permission_classes = [IsAuthenticated]
    serializer_class = ListInvoiceSerializer

    def get(self, request):
        '''Get list of all user invoices associated with it\'s clients'''
        invoices = Invoice.objects.filter(user_id=request.user)
        serializer = self.serializer_class(invoices, context={'request': request}, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


def generate_pdf(html_string):
	return pdfkit.from_string(
        html_string,
        configuration=pdfkit.configuration(
            wkhtmltopdf=r'C:\Users\DELL\wkhtmltopdf\bin\wkhtmltopdf.exe'),
            options={"enable-local-file-access": ""}
        )


class GenerateInvoicePDFView(APIView):
    '''Returns a download pdf format of invoice'''
    authentication_classes = [CustomAuthentication,]

    def get_object(self, request, client_id, pk):
        context = {}
        try:
            invoice = Invoice.objects.get(pk=pk, user_id=request.user, client_id__id=client_id)
            return invoice
        except Invoice.DoesNotExist:
            context['status'] = 'error'
            context['message'] = 'Invoice not found'
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, client_id, pk):
        context = {}
        invoice = self.get_object(request, client_id, pk)

        context = {
            "business_name": invoice.user_id.business_name,
            "email": invoice.user_id.email,
            "client_first_name": invoice.client_id.first_name,
            "client_last_name": invoice.client_id.last_name,
            "transaction_id": invoice.transaction_id,
            "amount": invoice.amount,
            "description": invoice.description,
            "customer_note": invoice.customer_note,
            "draft": invoice.draft,
            "status": invoice.status,
            "created_at": invoice.created_at,
            "due_at": invoice.due_at
        }

        try:
            html_string = 'invoice/invoice.html'
            html_string = render_to_string(html_string, context)
            generated_pdf = generate_pdf(html_string)

            response = HttpResponse(generated_pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="invoice-internpulse.pdf"'

            notify_user(request.user, 'download-success', 'Invoice downloaded successful')
            return response
        except Exception as e:
            context['status'] = 'error'
            context['message'] = f'Error Downloading: {e}'
            notify_user(request.user, 'download-failure', 'Invoice failed to download')
            return exceptions.ParseError(context)
