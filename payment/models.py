from django.db import models

from account.models import CustomUser
from invoice_generation.models import Client, Invoice


# Create your models here.
class Payment(models.Model):
    user_id = models.ForeignKey(CustomUser, related_name='user_payment', on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client, related_name='client_payment', on_delete=models.CASCADE)
    invoice_id = models.ForeignKey(Invoice, related_name='invoice_payment', on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=55)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    customer_note = models.TextField()
    method = models.CharField(max_length=55)
    status = models.CharField(max_length=55)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.invoice_id} for {self.user_id.email}"
