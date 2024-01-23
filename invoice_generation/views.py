# invoice_generation/views.py

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Invoice
from .serializer import InvoiceSerializer
from account.authentication import CustomAuthentication

@api_view(['GET', 'POST'])
@authentication_classes([CustomAuthentication])
@permission_classes([IsAuthenticated])
def get_invoices(request):
    if request.method == 'GET':
        invoices = Invoice.objects.filter(user=request.user)
        serializer = InvoiceSerializer(invoices, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['POST'])
@authentication_classes([CustomAuthentication])
@permission_classes([IsAuthenticated])
def create_invoice(request):
    serializer = InvoiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
@authentication_classes([CustomAuthentication])
@permission_classes([IsAuthenticated])
def update_invoice(request, invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id, user=request.user)
    except Invoice.DoesNotExist:
        return Response({'detail': 'Invoice not found.'}, status=404)

    serializer = InvoiceSerializer(invoice, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@authentication_classes([CustomAuthentication])
@permission_classes([IsAuthenticated])
def delete_invoice(request, invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id, user=request.user)
    except Invoice.DoesNotExist:
        return Response({'detail': 'Invoice not found.'}, status=404)

    invoice.delete()
    return Response({'detail': 'Invoice deleted successfully.'}, status=204)
