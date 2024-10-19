from wsgiref.validate import validator

from django.core.exceptions import ValidationError
from django.db import models
from user_Module.models import normal_user, user_notifications
from django.utils.text import slugify
class colors(models.Model):
    color=models.CharField(verbose_name='رنگ',max_length=30,blank=True,null=True)
    color_to_display=models.CharField(max_length=30,verbose_name='رنگ html',default='white')
    assigned_to_all_products=models.BooleanField(default=False,verbose_name='به همه کالا ها نسبت داده شده')
    def save(self,*args):
        super().save(*args)
        if not self.assigned_to_all_products:
            prs=products.objects.all()
            for pr in prs:
                pr_availbility=product_color_avalibity(product_id=pr.id,color_id=self.id)
                pr_availbility.save()
            self.assigned_to_all_products=True
            self.save()
    class Meta:
        verbose_name='رنگ'
        verbose_name_plural='رنگ ها'
    def __str__(self):
        return self.color

# Create your models here.
class images(models.Model):
    picture=models.ImageField(upload_to='product_images')
    product=models.ForeignKey('products',on_delete=models.CASCADE,verbose_name='محصول')

    def __str__(self):
        return self.product.title
    class Meta:
        verbose_name='تصویر محصول'
        verbose_name_plural='تصاویر محصولات'
    def delete(self, using=None, keep_parents=False):
        self.picture.delete()
        super().delete()



class brands(models.Model):
    title=models.CharField(max_length=30,verbose_name='برند کالا')
    def __str__(self):return self.title
    class Meta:
        verbose_name='برند محصول'
        verbose_name_plural='برندهای محصولات'

def product_count_validator(value):
    if value<0:
        raise ValidationError('تعداد محصول نمی تواند منقی باشد!',params={'value':value})
class products(models.Model):
    title=models.CharField(max_length=30,verbose_name='عنوان کالا',null=True,blank=True,unique=True)
    price=models.IntegerField(verbose_name='قیمت کالا',default=0)
    is_active=models.BooleanField(verbose_name='فعال',default=True)
    add_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت محصول')
    short_description=models.CharField(max_length=100,verbose_name='خلاصه توضیحات',null=True,blank=True)
    main_description=models.TextField(max_length=300,verbose_name='توضیحات اصلی',null=True,blank=True)
    url=models.SlugField(max_length=300,verbose_name='slug_field',default='')
    has_color_instances=models.BooleanField(default=False,verbose_name='وجود رنگ های مختلف ازاین محصول')
    category=models.ForeignKey('product_category',on_delete=models.CASCADE,verbose_name='دسته بندی کالا',null=True)
    brand=models.ForeignKey('brands',on_delete=models.CASCADE,verbose_name='بند محصول',null=True)
    rating=models.IntegerField(verbose_name='امتیاز کالا',default=0)
    def get_avalible_colors(self):
        result=self.product_color_avalibity_set.filter(amount_left__gt=0).all()
        return result
    def chekc_if_ordered(self):
        return self.order_detail_set.filter(parent_order__is_paid=False).exists()
    def load_cooments(self):
        my_list=list(self.comment_set.all())
        return my_list
    def available_colors(self):

        return self.color.all()
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        url=''
        for char in self.title:
            url+=char+'-'
        self.url=url
        super().save()
        if not self.has_color_instances:
            colors_available=colors.objects.all()
            for clr in colors_available:
                availability=product_color_avalibity(product_id=self.id,color_id=clr.id)
                availability.save()
        self.has_color_instances=True
        super().save()
    class Meta:
        verbose_name='محصول'
        verbose_name_plural='محصولات'
    def __str__(self):

        return self.title
    def product_images(self):
        return self.images_set.all()
    def thumbnail_photo(self):
        thumbnail_photo=self.images_set.all().first().picture
        return thumbnail_photo


class product_category(models.Model):
    title=models.CharField(verbose_name='دسته بندی',max_length=60,unique=True)
    def __str__(self): return self.title
    class Meta:
        verbose_name='دسته بندی محصول'
        verbose_name_plural='دسته بندی محصولات'

class product_wish_list(models.Model):
    product=models.OneToOneField(products,on_delete=models.CASCADE,null=True,blank=True,editable=True,verbose_name='کالا')
    users=models.ManyToManyField(normal_user,verbose_name='کاربران علاقه مند به این کالا',null=True,blank=True)
    def __str__(self):
        return self.product.title
    class Meta:
        verbose_name='علاقه مندی کالا'
        verbose_name_plural='علاقه مندی های کالا ها'

class product_color_avalibity(models.Model):
    product=models.ForeignKey('products',on_delete=models.CASCADE,verbose_name='product',null=True)
    color = models.ForeignKey('colors', on_delete=models.CASCADE, verbose_name='product color', null=True)
    amount_left=models.IntegerField(default=0,verbose_name='amount left',validators=[product_count_validator])
    def save(self,*args):
     amount_changed=False
     try:
        old_amount=product_color_avalibity.objects.get(id=self.id).amount_left
        new_amount=self.amount_left
        amount_changed=new_amount-old_amount>0
     except:
        pass
     if amount_changed:
        wish_list,bb=product_wish_list.objects.get_or_create(product_id=self.product.id)
        for user in wish_list.users.all():
           user_notifications.objects.create(receiver_id=user.id,notif_message=f'کالای {self.product.title} با رنگ {self.color} موجود شد!').save()

     super(*args).save()
class product_article(models.Model):
    product=models.OneToOneField(products,verbose_name='محصول مقاله',on_delete=models.CASCADE,null=True,blank=True)
    text=models.TextField(max_length=2000,verbose_name='متن مقاله',default='')
    class Meta:
        verbose_name = 'مقاله کالا'
        verbose_name_plural = 'مقالات کالا ها'

class article_picture(models.Model):
    picture=models.ImageField(upload_to='article_images',verbose_name='تصویر مقاله')
    parent_product=models.ForeignKey(products,on_delete=models.CASCADE,verbose_name='محصول والد')
    class Meta:
        verbose_name = 'تصویر مقاله'
        verbose_name_plural = 'تصاویر مقالات'