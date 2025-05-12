from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
choices=(('mashhad','مشهد'),('tehran','تهران'),('shiraz','شیراز'),('isfahan','اصهان'),('rasht','رشت'),('sarry','ساری'),
             ('az','یزد'),('mashhad','کرمان'))
# Create your models here.

class normal_user(AbstractUser):
    activation_code=models.CharField(max_length=100,verbose_name='کد فعال سازی',null=True,blank=True)
    phone_number=models.CharField(max_length=20,verbose_name='شماره موبایل',null=True,blank=True)
    email = models.EmailField(verbose_name='ایمیل',null=True,blank=True)
    address=models.TextField(max_length=300,verbose_name='آدرس محل سکونت',null=True,blank=True)
    first_name = models.CharField(max_length=300, verbose_name='نام', null=True, blank=True)
    last_name =models.CharField(max_length=300, verbose_name='نام خانوادگی', null=True, blank=True)
    city=models.CharField(max_length=20,choices=choices, null=True, blank=True,verbose_name='شهر')
    postal_code=models.IntegerField(verbose_name='کد پستی', default=0)
    avatar=models.ImageField(upload_to='profiles',null=True,blank=True,verbose_name='تصویر پروفایل')
    reset_password_code=models.CharField(max_length=100,verbose_name='کد تغییر رمز عبور',default='')
    user_types=(('normal','عادی'),('admin','ادمین'))
    user_type=models.CharField(max_length=10,default='عادی',choices=user_types)
    admin_levels=((1,1),(2,2),(3,3))
    admin_level=models.IntegerField(default=None,choices=admin_levels,null=True)
    status_modes=(('normal','عادی')
    ,('partially_banned','مسدودیت ناقص')
                  ,('fully_banned','مسدودیت کامل'))
    user_status=models.CharField(max_length=20,default='normal',verbose_name='وضعیت کاربر',choices=status_modes)
    def save(self,*args,**kwargs):
        if self.admin_level != None and self.user_type=='noraml':
            raise ValidationError('normal users cannot have admin level')
        super().save(*args,**kwargs)

    def notfis_count(self):
        count=self.user_notifications_set.filter(is_read=False).count()
        return count
    def delete_all_false_attemps(self):
        self.user_false_password_attemp_set.all().delete()
    def delete_out_dated_attemps(self):
        attemps = self.user_false_password_attemp_set.all()
        for atem in attemps:
            now=timezone.now()
            if (now-atem.attemp_date).total_seconds()>10000:
                atem.delete()

    class Meta:
        verbose_name='کاربر'
        verbose_name_plural='کاربرها'


class user_false_password_attemp(models.Model):
    attemp_date=models.DateTimeField(auto_now_add=True,verbose_name='date of attemp')
    user=models.ForeignKey(normal_user,on_delete=models.CASCADE,verbose_name='suspicious user')



