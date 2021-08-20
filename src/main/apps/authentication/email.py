from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from threading import Thread
from typing import (
    Generic,
    List,
    TypeVar,
)
SelfClass = TypeVar('SelfClass')


class EmailThread(Thread):

	def __new__(cls, email, *args, **kwargs) -> Generic[SelfClass]:
		return super(EmailThread, cls).__new__(cls, *args, **kwargs)


	def __init__(self, email, *args, **kwargs):
		self.email = email
		Thread.__init__(self)


	def run(self):
		self.email.content_subtype = "html"
		self.email.send()


class EmailPreparation:

	@staticmethod
	def send(data):
		email = EmailMessage(
			subject=data['subject'], body=data['body'], to=[data['to']])
		EmailThread(email).start()


def send_email(request, user=None):
	if user:
		acc_hash = str(user.acc_hash)
		username = str(user.username)
		email = str(user.email)
	else:
		acc_hash = str(request.user.acc_hash)
		username = str(request.user.username)
		email = str(request.user.email)
	current_site = str(get_current_site(request))
	relative_link = str(reverse('verify_account'))
	abs_url = f"http://{current_site}{relative_link}?verify={acc_hash}"
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
	EmailPreparation.send(data)