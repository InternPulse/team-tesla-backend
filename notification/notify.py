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
        elif str(type).casefold() == 'client-success':
            type = NotificationType.objects.get(name='Client successful')
        elif str(type).casefold() == 'client-failure':
            type = NotificationType.objects.get(name='Client failure')
        elif str(type).casefold() == 'client-updated':
            type = NotificationType.objects.get(name='Client updated')
        elif str(type).casefold() == 'account-success':
            type = NotificationType.objects.get(name='Account successful')
        elif str(type).casefold() == 'account-failure':
            type = NotificationType.objects.get(name='Account failure')
        elif str(type).casefold() == 'account-updated':
            type = NotificationType.objects.get(name='Account updated')
        elif str(type).casefold() == 'download-success':
            type = NotificationType.objects.get(name='Download successful')
        elif str(type).casefold() == 'download-failure':
            type = NotificationType.objects.get(name='Download failure')
        elif str(type).casefold() == 'password-success':
            type = NotificationType.objects.get(name='Password successful')
        elif str(type).casefold() == 'password-failure':
            type = NotificationType.objects.get(name='Password failure')
        elif str(type).casefold() == 'otp-success':
            type = NotificationType.objects.get(name='OTP success')
        elif str(type).casefold() == 'email-failure':
            type = NotificationType.objects.get(name='Email failure')
        elif str(type).casefold() == 'otp-failure':
            type = NotificationType.objects.get(name='OTP failure')
        elif str(type).casefold() == 'profile-success':
            type = NotificationType.objects.get(name='Profile updated')
        elif str(type).casefold() == 'profile-failure':
            type = NotificationType.objects.get(name='Profile failure')

        # send message
        Notification.objects.create(
            user_id=user_id,
            type=type,
            message=message,
        )

        return True
    except:
        pass
