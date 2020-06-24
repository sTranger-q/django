
from django.core.mail import send_mail

from comic_mlgm.celery import app


@app.task
def send_email(subject,email_address, content):

    send_mail(subject, '', '1916350942@qq.com', [email_address], html_message=content)
