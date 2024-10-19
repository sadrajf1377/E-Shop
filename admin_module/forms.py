from django.forms import ModelForm, forms, Textarea,CharField
from product_module.models import products,product_article
from django import forms
class Product_edit_form(ModelForm):
    class Meta:
        model=products
        fields=['title','price','short_description','main_description','category','brand','is_active']
        labels={'title':'عنوان محصول','price':'قیمت محصول','short_description':'توضیحات کوتاه محصول'
        ,'main_description':'توضیحات اصلی محصول','category':'دسته بندی محصول','brand':'برند محصول','is_active':'فعال/غیرفعال'}
        widgets={'short_description':forms.TextInput(),'main_description':forms.Textarea()}

class Article_form(ModelForm):
    class Meta:
        model=product_article
        fields=['product','text']
        labels={'product':'محصول والد','text':'متن مقاله'}
        widgets={'text':forms.Textarea()}

