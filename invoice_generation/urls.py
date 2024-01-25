# invoice_generation/urls.py

from django.urls import path
from . import views


app_name = 'invoice_generation'

urlpatterns = [
    path('', views.AllUserClientsView.as_view(), name='get_user_clients'),
    path('detail/<int:pk>/', views.UpdateDeleteClientView.as_view(), name='get_client_detail'),
    path('client/', views.AllUserClientInvoiceView.as_view(), name='get_user_clients'),
    path('client/detail/<int:pk>/', views.UpdateDeleteInvoiceView.as_view(), name='get_client_detail')
]
