'''
This file helps in creating notifications
'''

from notification.models import Notification, NotificationType


def notify_user(user_id, type, message):
    try:
        # define message type
        if str(type).casefold() == 'payment-failure':
            type = NotificationType.objects.get(name='Payment failure')
        elif str(type).casefold() == 'payment-success':
            type = NotificationType.objects.get(name='Payment successful')
        elif str(type).casefold() == 'invoice-success':
            type = NotificationType.objects.get(name='Invoice successful')
        elif str(type).casefold() == 'invoice-failure':
            type = NotificationType.objects.get(name='Invoice failure')
        elif str(type).casefold() == 'invoice-updated':
            type = NotificationType.objects.get(name='Invoice updated')
        elif str(type).casefold() == 'account-success':
            type = NotificationType.objects.get(name='Account successful')
        elif str(type).casefold() == 'account-failure':
            type = NotificationType.objects.get(name='Account failure')
        elif str(type).casefold() == 'account-updated':
            type = NotificationType.objects.get(name='Account updated')

        # send message
        Notification.objects.create(
            user_id_id=user_id,
            notification_type=type,
            message=message,
        )

        return True
    except:
        pass
