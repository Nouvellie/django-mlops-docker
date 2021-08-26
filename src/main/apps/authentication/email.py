import uuid

from .models import User
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from main.exceptions import CustomError
from main.settings import DEBUG
from threading import Thread
from typing import (
    Generic,
    TypeVar,
)
SELFCLASS = TypeVar('SELFCLASS')


class EmailThread(Thread):
    """Class for sending e-mails at the thread level."""

    def __new__(cls, email, *args, **kwargs) -> Generic[SELFCLASS]:
        return super(EmailThread, cls).__new__(cls, *args, **kwargs)

    def __init__(self, email, *args, **kwargs) -> None:
        self.email = email
        Thread.__init__(self)

    def run(self) -> None:
        """Sending e-mail, parallel to the main process."""
        self.email.content_subtype = "html"
        self.email.send()


class EmailPreparation:
    """Preparation class for sending e-mails at the thread level."""

    @staticmethod
    def send(data: list, thread: bool) -> None:
        """Send all the necessary parameters that make up the e-mail."""

        email = EmailMessage(
            subject=data['subject'], body=data['body'], to=[data['to']])
        if thread:
            EmailThread(email).start()
        else:
            email.content_subtype = "html"
            email.send()


def send_email(request: dict, user=None, thread: bool = True, task: int = 0) -> None:
    if user:
        username = str(user.username)
        email = str(user.email)
    else:
        username = str(request.user.username)
        email = str(request.user.email)

    user = User.objects.get(username=username)
    # if DEBUG:
    #   pre_url = 'http://'
    # else:
    #   pre_url = 'https://'
    pre_url = 'http://'
    current_site = str(get_current_site(request))
    user.acc_hash = uuid.uuid4()
    user.acc_hash_expiration = datetime.now(timezone.utc)
    user.pass_token = uuid.uuid4()
    user.pass_token_expiration = datetime.now(timezone.utc)
    user.save()
    acc_hash = user.acc_hash
# Account verification.
    if task == 1:
        relative_info = 'account_verification'
        relative_pre = 'Account verification link:'
        new_info = 'verify'
        new_pre = 'Request new link:'
        url_end = f"?verify={acc_hash}"
        subject = "Nouvellie: Account verification"
        main_msg = "Use the link below to verify your account. This link allows you to verify your account within 24 hours of its generation, after which you will have to generate another link. (Each time a session is started, the verification link will change)"

# Password reset.
    elif task == 2:        
        relative_info = 'password_reset'
        relative_pre = 'Password reset link:'
        new_info = 'reset'
        new_pre = 'Request new link:'
        token = user.pass_token
        url_end = f"?token={token}&password=newpassword"
        subject = "Nouvellie: Password reset"
        main_msg = "Send us the new password by replacing the value 'newpassword' in the url indicated. This link allows you to change your password within 2 hours of its generation, after which you will have to generate another link. (The password must contain at least 8 characters and cannot contain the initials of your username or email address, special characters are allowed)"
        
    data = email_preparation(pre_url, current_site, relative_info, new_info, relative_pre, new_pre, url_end, username, email, subject, main_msg)
        
    EmailPreparation.send(data=data, thread=thread)


def email_preparation(pre_url: str, current_site: str, relative_info: str, new_info: str , relative_pre: str, new_pre: str, url_end: str, username: str, email: str, subject: str, main_msg: str) -> dict:

    relative_link = str(reverse(relative_info))
    new_link = str(reverse(new_info))
    abs_url = f"{pre_url}{current_site}{relative_link}{url_end}"
    new_url = f"{pre_url}{current_site}{new_link}"

    body = f"""
        <html align="center" style="font-family: Arial">
          <head></head>
          <body style="background-color: rgb(12, 14, 19); color: white;" >
            <br><br><br>
            <h2>Hi {username}.</h2>
            <p>{main_msg}</p>
            <h5>Validate: {abs_url}</h5>
            <h5>New link: {new_url}</h5>
            <br><br><br>
            <br><br>
          </body>
        </html>
    """

    data = {
        'body': body,
        'to': email,
        'subject': subject,
    }
    return data