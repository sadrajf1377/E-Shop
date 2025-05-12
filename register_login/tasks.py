from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from foroush_gah_postgresql.settings import EMAIL_HOST_USER
from user_Module.models import normal_user

@shared_task
def send_email_to_user(subject,template_name,to,context):
    html_message1 = render_to_string(template_name, context)
    plain_message = strip_tags(html_message1)
    from_email = EMAIL_HOST_USER
    result=send_mail(subject, plain_message, from_email, [to], html_message=html_message1)
    if result==0:
        normal_user.objects.get(activation_code=context['code'])


