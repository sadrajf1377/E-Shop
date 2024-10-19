from django.db import models
from user_Module.models import normal_user
# Create your models here.
class debts(models.Model):
    user=models.ForeignKey(normal_user,verbose_name='user whom you owe money',on_delete=models.DO_NOTHING,null=True)
    amount=models.IntegerField(verbose_name='amount of money you owe this use',default=0)
    paid_status=models.BooleanField(verbose_name='is the amount paid',default=False)
    pay_date=models.DateField(null=True,blank=True)
    pay_check_proof=models.ImageField(verbose_name='a photo of pay recid',blank=True,null=True,upload_to='recids')
