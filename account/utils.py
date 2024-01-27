from collections.abc import Callable, Iterable, Mapping
import threading
from typing import Any

from django.template.loader import render_to_string
import string
import random

from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def generate_otp(length=6):
    # Ensure the length is 6
    length = max(6, length)

    # Generate an OTP within the specified range
    min_range = 10**(length - 1)
    max_range = 10**length - 1
    otp = random.randint(min_range, max_range)

    return int(otp)


class EmailThread(threading.Thread):
    def __init__(self, mail):
        self.mail = mail
        threading.Thread.__init__(self)

    def run(self):
        self.mail.send()


def send_email(subject, email_html_message, from_email, recipient_list):
    message = strip_tags(email_html_message)

    mail = EmailMultiAlternatives(subject, message, from_email, recipient_list)
    mail.attach_alternative(email_html_message, 'text/html')

    EmailThread(mail).start()
    print("Email Sent Succesfully!")
