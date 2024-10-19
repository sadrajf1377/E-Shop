from django.db import models
from product_module.models import products
from user_Module.models import normal_user
# Create your models here.
class comment(models.Model):
    parent=models.ForeignKey('comment',verbose_name='والد',on_delete=models.CASCADE,null=True,blank=True)
    subject=models.CharField(max_length=20,verbose_name='عنوان نظر',null=True,blank=True)
    comment_text=models.TextField(max_length=100,verbose_name='متن نظر',null=True,blank=True)
    product=models.ForeignKey(products,verbose_name='محصول',on_delete=models.CASCADE)
    user=models.ForeignKey(normal_user,on_delete=models.CASCADE,verbose_name='کاربر',null=True,blank=True)
    def __str__(self):
        return f'{self.product} /{self.user}'
