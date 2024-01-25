'''
Views for invoice generation app
'''
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import exceptions

from .models import Client, Invoice
from .serializers import ClientSerializer, InvoiceSerializer, ListInvoiceSerializer
from account.authentication import CustomAuthentication


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
            return Response(context, status=status.HTTP_200_OK)
        
        context['status'] = 'error'
        context.update(serializer.errors)

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
            return Response(context, status=status.HTTP_200_OK)

        context['status'] = 'error'
        context.update(serializer.errors)

        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    

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
            serializer.save(user_id=request.user)

            context['status'] = 'success'
            context['message'] = 'Invoice created successful'
            context.update(serializer.data)
            return Response(context, status=status.HTTP_200_OK)

        context['status'] = 'error'
        context.update(serializer.errors)

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
            return Response(context, status=status.HTTP_200_OK)

        context['status'] = 'error'
        context.update(serializer.errors)

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
