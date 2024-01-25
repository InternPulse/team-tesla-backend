# invoice_generation/urls.py

from django.urls import path
from . import views


app_name = 'invoice_generation'

urlpatterns = [
    path('', views.AllUserClientInvoiceView.as_view(), name='get_user_client_invoice'),
    path('create/', views.CreateClientInvoiceView.as_view(), name='post_user_clients_invoice'),
    path('detail/<int:pk>/', views.GetUpdateInvoiceView.as_view(), name='get_invoice_detail'),
    path('client/', views.AllUserClientsView.as_view(), name='get_user_clients'),
    path('client/detail/<int:pk>/', views.GetUpdateClientView.as_view(), name='get_client_detail')
]
