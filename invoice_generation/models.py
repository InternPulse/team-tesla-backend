from django.db import models

from account.models import CustomUser


# Create your models here.
class Client(models.Model):
    TITLE_CHOICE = (
        ('1', 'Mr'),
        ('2', 'Mrs'),
        ('3', 'Miss')
    )

    user_id = models.ForeignKey(CustomUser, related_name='user_client', on_delete=models.CASCADE)
    title = models.CharField(max_length=1, choices=TITLE_CHOICE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    customer_email = models.EmailField()
    work_phone = models.CharField(max_length=255, blank=True, null=True)
    personal_phone = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Invoice(models.Model):
    user_id = models.ForeignKey(CustomUser, related_name='user_invoice', on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client, related_name='client_invoice', on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=55)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    customer_note = models.TextField()
    draft = models.BooleanField(default=False)
    status = models.CharField(max_length=55)
    created_at = models.DateField(auto_now_add=True)
    due_at = models.DateField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.invoice_id} for {self.user_id.email}"
