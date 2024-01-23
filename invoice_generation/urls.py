# invoice_generation/urls.py

from django.urls import path
from .views import get_invoices, create_invoice, update_invoice, delete_invoice

urlpatterns = [
    path('invoices/', get_invoices, name='get_invoices'),
    path('invoices/create/', create_invoice, name='create_invoice'),
    path('invoices/<int:invoice_id>/update/', update_invoice, name='update_invoice'),
    path('invoices/<int:invoice_id>/delete/', delete_invoice, name='delete_invoice'),
]
