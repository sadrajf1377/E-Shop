from django.core.validators import MinLengthValidator
from django.db import models

from user_Module.models import normal_user


# Create your models here.
class user_notifications(models.Model):
    receiver=models.ForeignKey(normal_user,on_delete=models.CASCADE,verbose_name='گیرنده اعلان')
    notif_message=models.CharField(max_length=100,verbose_name='پیام اعلان',validators=([MinLengthValidator(20)]))
    notif_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ اعلان')
    is_read=models.BooleanField(verbose_name='خوانده شده',default=False)
    class Meta:
        verbose_name='اعلان کاربر'
        verbose_name_plural='اعلانات کاربران'
        db_table='user notifications'