import datetime
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
        acc_hash = str(user.acc_hash)
        username = str(user.username)
        email = str(user.email)
    else:
        acc_hash = str(request.user.acc_hash)
        username = str(request.user.username)
        email = str(request.user.email)
# Account verification.
    if task == 1:
        user = User.objects.get(username=username)
        timenow = datetime.now(timezone.utc)
        # if DEBUG:
        # 	pre_url = 'http://'
        # else:
        # 	pre_url = 'https://'
        pre_url = 'http://'
        work = 'verify'
        current_site = str(get_current_site(request))
        relative_link = relative_link = str(reverse('account_verification'))
        new_link = relative_link = str(reverse('verify'))
        new_url = f"{pre_url}{current_site}{new_link}"
        abs_url = f"{pre_url}{current_site}{relative_link}?{work}={acc_hash}"
        body = f"""
    		<html align="center" style="font-family: Arial">
    		  <head></head>
    		  <body style="background-color: rgb(12, 14, 19); color: white;" >
    		  	<br><br><br>
    		    <h2>Hi {username}.</h2>
    		    <p>Use the link below to verify your account. This link allows you to verify your account within 24 hours of its generation, after which you will have to generate another link. (Each time a session is started, the verification link will change)</p>
    		    <h5>Verify: {abs_url}</h5>
                <br>
                <h5>New link: {new_url}</h5>
    		    <br><br><br>
    		    <br><br>
    		  </body>
    		</html>
    	"""
        data = {
            'body': body,
            'to': email,
            'subject': f"Nouvellie: Account verification.",
            'url': abs_url,
        }
        EmailPreparation.send(data=data, thread=thread)

    elif task == 2:
        user = User.objects.get(username=username)
        timenow = datetime.now(timezone.utc)
        if timenow > (user.pass_token_expiration + timedelta(days=1)):
            raise CustomError(detail={'error': "invalid token."}, code=400)

        pre_url = 'http://'
        current_site = str(get_current_site(request))
        relative_link = relative_link = str(reverse('password_reset'))
        new_link = relative_link = str(reverse('reset'))
        new_url = f"{pre_url}{current_site}{new_link}"
        token = user.pass_token
        abs_url = f"{pre_url}{current_site}{relative_link}?token={token}&password=newpassword"
        body = f"""
            <html align="center" style="font-family: Arial">
              <head></head>
              <body style="background-color: rgb(12, 14, 19); color: white;" >
                <br><br><br>
                <h2>Hi {username}.</h2>
                <p>Send us the new password by replacing the value "newpassword" in the url indicated. This link allows you to change your password within 24 hours of its generation, after which you will have to generate another link. (The password must contain at least 8 characters and cannot contain the initials of your username or email address, special characters are allowed)</p>
                <h5>Validate: {abs_url}</h5>
                <br>
                <h5>New link: {new_url}</h5>
                <br><br><br>
                <br><br>
              </body>
            </html>
        """
        data = {
            'body': body,
            'to': email,
            'subject': f"Nouvellie: Password reset.",
            'url': abs_url,
        }

        EmailPreparation.send(data=data, thread=thread)
    else:
        raise CustomError(detail={'error': "Incorrect task."}, code=400)
