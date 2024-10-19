from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum

from user_Module.models import normal_user
from product_module.models import products
from product_module.models import colors
from django.forms.models import model_to_dict
# Create your models here.
class order(models.Model):
    user=models.ForeignKey(normal_user,verbose_name='کاربر',on_delete=models.CASCADE,null=True,blank=True)
    order_date=models.DateTimeField(auto_now_add=True,verbose_name='زمان سثبت سفارش',null=True,blank=True)
    is_paid=models.BooleanField(verbose_name='وضعیت پرداخت',default=False)
    total_price=models.FloatField(verbose_name='قیمت نهایی سفارش',null=True,blank=True)
    recive_info=models.ForeignKey('reciver_info',verbose_name='مشخصات گیرنده',on_delete=models.CASCADE,null=True,blank=True)
    order_number=models.CharField(verbose_name='order number',max_length=100,unique=True,null=True,blank=True)
    choices=(('confirmed','تایید شده'),('rejected','رد شده'),('not confirmed','تایید نشده'))
    status=models.CharField(verbose_name='وضعیت سفارش',max_length=100,default=choices[2],choices=choices)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
      if self.is_paid and not self.order_number:
         self.order_number=str(self.id)+self.user.username+str(self.order_detail_set.count())+str(self.user.id)
      print('saved')
      super().save()
    class Meta:
        verbose_name='سفارش کاربر'
        verbose_name_plural='سفارش های کاربران'
    def __str__(self):

        return self.user.username
    def get_children(self):

        return self.order_detail_set.all()
    def get_total_price(self):
        value=self.get_children().aggregate(sum_price=Sum('total_price'))['sum_price'] if self.get_children().count()!=0 else 0
        return value


    def get_fields(self):

        fields=self._meta.fields
        result={}
        for field in fields:
            verbose_name=self._meta.get_field(field.name).verbose_name
            value=self.__getattribute__(field.name)
            result.update({verbose_name:value})
        print(result)
        return result

def detail_count_validator(value):
    if value<=0:
        raise ValidationError('The count of a detail cannot be less than zero!',params={'value':value})
class order_detail(models.Model):
    parent_order=models.ForeignKey(order,on_delete=models.CASCADE,verbose_name='والد',null=True,blank=True)
    product=models.ForeignKey(products,on_delete=models.CASCADE,verbose_name='محصول',null=True,blank=True)
    count=models.IntegerField(max_length=90,verbose_name='تعداد',default=1,validators=[detail_count_validator])
    total_price=models.IntegerField(verbose_name='قیمت نهایی',default=0)
    color=models.ForeignKey(colors,on_delete=models.CASCADE,verbose_name='رنگ محصول',null=True)
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.total_price=self.product.price*self.count
        super().save()

class reciver_info(models.Model):
    first_name=models.CharField(max_length=50,verbose_name='نام',default='',null=False,blank=False)
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی', default='',null=False,blank=False)
    phone=models.IntegerField(max_length=100,verbose_name='شماره تلفن',null=False,blank=False,default=0)
    email=models.EmailField(max_length=50,verbose_name='ایمیل',null=True,blank=True)
    address=models.CharField(max_length=100,verbose_name='آدرس',null=False,blank=False,default='')
    city=models.CharField(max_length=60,verbose_name='شهر',null=False,blank=False,default='')
    postal_code= models.IntegerField(max_length=10,verbose_name='کد پستی',null=False,blank=False,default=0)
    def __str__(self):
        return str(self.id)

