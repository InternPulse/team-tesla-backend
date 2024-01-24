from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import CustomUser


# Create your models here.
class NotificationType(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Notification(models.Model):
    user_id = models.ForeignKey(CustomUser, related_name="user_notification", on_delete=models.CASCADE)
    type = models.ForeignKey(NotificationType, related_name="type_of_notification", on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
