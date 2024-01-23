from django.db import models
from account.models import CustomUser

# Create your models here.
class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete= models.CASCADE, related_name="invoices")
    amount = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f"Invoice {self.id} for {self.user.email}"