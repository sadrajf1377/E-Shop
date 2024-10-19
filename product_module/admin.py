from django.contrib import admin
from django.http import HttpRequest

from .models import products,images,colors,product_category,brands,product_wish_list,product_color_avalibity,product_article

# Register your models here.
class product_settings(admin.ModelAdmin):
    list_display = ['title','price','add_date','rating','short_description','main_description','brand','category']
    readonly_fields = ['url','rating','add_date','has_color_instances']

class image_settings(admin.ModelAdmin):
    list_display = ['__str__','picture']
    def delete_queryset(self, request, queryset:images):
         for obj in queryset:
             obj.picture.delete()
             obj.delete()
class products_cats(admin.ModelAdmin):
    list_display=['__str__','title','id']


admin.site.register(products,product_settings)
admin.site.register(images,image_settings)
admin.site.register(colors)
admin.site.register(product_category,products_cats)
admin.site.register(brands)
admin.site.register(product_wish_list)
admin.site.register(product_color_avalibity)
admin.site.register(product_article)