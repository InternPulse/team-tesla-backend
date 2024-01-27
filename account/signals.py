from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save

from django_rest_passwordreset.signals import reset_password_token_created

from .models import CustomUser, OTP
from .utils import generate_otp, send_email


@receiver(post_save, sender=CustomUser)
def create_otp(sender, instance, created=False, **kwargs):
    if created:
        otp = generate_otp()
        OTP.objects.create(user_id=instance, generated_otp=otp)
        email = instance.email

        context = {
            'email': email,
            'otp': otp
        }

        subject = "OTP Resent by {title}".format(title="Invoice Pulse")
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email,]
        email_html_message = render_to_string('account/otp.html', context)
        send_email(subject, email_html_message, from_email, recipient_list)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('account:forgot_password')),
            reset_password_token.key)
    }

    subject = "Password Reset for {title}".format(title="Invoice Pulse")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [reset_password_token.user.email,]

    # render email html format to string
    email_html_message = render_to_string('account/forgot_password.html', context)
    send_email(subject, email_html_message, from_email, recipient_list)
