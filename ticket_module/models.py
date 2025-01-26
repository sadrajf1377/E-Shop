from django.db import models
from user_Module.models import normal_user
# Create your models here.
class user_ticket(models.Model):
    title=models.CharField(max_length=30,verbose_name='عنوان تیکت',null=False,blank=False)
    created_by=models.ForeignKey(normal_user,on_delete=models.CASCADE,verbose_name='ایجاد شده توسط',null=False,blank=False)
    creation_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد تیکت')
    def __str__(self):
        return self.title

class ticket_message(models.Model):
    parent_message=models.ForeignKey('ticket_message',null=True,blank=True,verbose_name='پیام والد',on_delete=models.CASCADE)
    parent_ticket=models.ForeignKey(user_ticket,null=False,blank=False,verbose_name='تیکت والد',on_delete=models.CASCADE)
    message=models.CharField(max_length=400,verbose_name=' متن پیام',blank=False,null=False)
    date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد پیام')
    is_answered=models.BooleanField(default=False,verbose_name='آیا این پیام پاسخ دارد')
    def __str__(self):

        return f'parent ticket/{self.parent_ticket.title}||parent message/{self.parent_message} '