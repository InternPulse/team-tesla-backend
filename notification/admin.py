from django.contrib import admin
from notification.models import NotificationType, Notification

admin.site.site_header = 'Invoice Pulse'


class NotificationTypeAdminView(admin.ModelAdmin):
    """Modifies Notification Type model admin view."""
    ordering = ['id']
    list_display = [
            'id', 'name',
            'is_active', 'created_at',
            'updated_at'
        ]
    
admin.site.register(NotificationType, NotificationTypeAdminView)


class NotificationAdminView(admin.ModelAdmin):
    """Modifies Notification model admin view."""
    ordering = ['-id']
    list_display = [
        'id', 'user_id', 'type',
        'message', 'is_read', 'is_active', 'created_at'
    ]
    list_filter = [
        'type', 'message', 'is_read', 'is_active', 'created_at'
    ]
    search_fields = ['type', 'message']

admin.site.register(Notification, NotificationAdminView)
