from rest_framework import serializers
from .models import Client, Invoice


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'title', 'first_name', 'last_name', 'company_name',
                  'customer_email', 'work_phone', 'personal_phone',
                  'created_at']

        extra_kwargs = {
            'id': {'read_only': True},
            'title': {'read_only': True},
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
            'company_name': {'read_only': True},
            'customer_email': {'read_only': True},
            'work_phone': {'read_only': True},
            'personal_phone': {'read_only': True},
            'created_at': {'read_only': True}
        }


class InvoiceSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(source='client_id.first_name', read_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'client_id', 'transaction_id', 'amount',
                  'description', 'customer_note', 'draft', 'status',
                  'created_at', 'due_at']

        extra_kwargs = {
            'id': {'read_only': True},
            'transaction_id': {'read_only': True},
            'amount': {'read_only': True},
            'description': {'read_only': True},
            'customer_note': {'read_only': True},
            'draft': {'read_only': True},
            'status': {'read_only': True},
            'created_at': {'read_only': True},
            'due_at': {'read_only': True}
        }
