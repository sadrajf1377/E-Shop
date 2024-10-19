from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from foroush_gah_postgresql import settings


def send_email(template_name,to,subject,contex):
    try:
        html_message1=render_to_string(template_name,contex)
        plain_message=strip_tags(html_message1)
        from_email=settings.EMAIL_HOST_USER
        send_mail(subject, plain_message, from_email, [to],html_message= html_message1)
        return 1
    except:
        return 0
