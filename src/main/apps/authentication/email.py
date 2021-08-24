from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from main.settings import DEBUG
from threading import Thread
from typing import (
    Dict,
    Generic,
    List,
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
    def send(data: List, thread: bool) -> None:
        """Send all the necessary parameters that make up the e-mail."""
        
        email = EmailMessage(
            subject=data['subject'], body=data['body'], to=[data['to']])
        if thread:
            EmailThread(email).start()
        else:
            email.content_subtype = "html"
            email.send()


def send_email(request: Dict, user=None, thread: bool=True) -> None:
    if user:
        acc_hash = str(user.acc_hash)
        username = str(user.username)
        email = str(user.email)
    else:
        acc_hash = str(request.user.acc_hash)
        username = str(request.user.username)
        email = str(request.user.email)
    # if DEBUG:
    # 	pre_url = 'http://'
    # else:
    # 	pre_url = 'https://'
    pre_url = 'http://'
    current_site = str(get_current_site(request))
    relative_link = str(reverse('account_verification'))
    abs_url = f"{pre_url}{current_site}{relative_link}?verify={acc_hash}"
    body = f"""
		<html align="center" style="font-family: Arial">
		  <head></head>
		  <body style="background-color: rgb(12, 14, 19); color: white;" >
		  	<br><br><br>
		    <h2>Hi {username}.</h2>
		    <p>Use the link below to verify your account.</p>
		    <h5>{abs_url}</h5>
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
