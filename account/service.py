from collections.abc import Callable, Iterable, Mapping
import threading
from typing import Any

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


class EmailThread(threading.Thread):
    def __init__(self, mail):
        self.mail = mail
        threading.Thread.__init__(self)

    def run(self):
        self.mail.send()


class EmailService():
    def send_email(self, subject, email_template, from_email, recipient_list, context):
        html_message =  render_to_string(email_template, context)
        message = strip_tags(html_message)

        mail = EmailMultiAlternatives(subject, message, from_email, recipient_list)
        mail.attach_alternative(html_message, 'text/html')

        EmailThread(mail).start()
        print("Email Sent Succesfully!")
