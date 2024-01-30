from django.contrib import admin
from .models import Client, Invoice
# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'title', 'first_name', 'last_name', 'company_name', 'customer_email',
                    'work_phone', 'personal_phone', 'created_at', 'updated_at',)
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('user_id__email', 'title', 'first_name', 'last_name', 'company_name', 'customer_email',
                    'work_phone', 'personal_phone',)

admin.site.register(Client, ClientAdmin)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'client_id', 'transaction_id', 'amount', 'description',
                    'customer_note', 'status', 'created_at', 'due_at', 'updated_at',)
    list_filter = ('amount', 'status', 'created_at', 'due_at', 'updated_at',)
    search_fields = ('user_id__email', 'client_id__first_name', 'client_id__last_name', 'transaction_id', 'amount', 'description',
                     'customer_note', 'status',)

admin.site.register(Invoice, InvoiceAdmin)
