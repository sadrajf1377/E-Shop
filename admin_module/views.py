import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

import comments_module.models
from product_module.models import products,product_article,article_picture
from .forms import Product_edit_form,Article_form
from product_module.models import images,product_category,colors,brands,product_color_avalibity
from order_module.models import order,order_detail
from user_Module.models import normal_user, user_ticket, ticket_message, user_notifications
from .models import debts
def user_is_admin(admin_lvl):
  def Wrapper(func):
          def To_do(*args, **kwargs):
              request: HttpRequest = args[0]

              if not request.user.is_authenticated:
                  return redirect(reverse('login-user'))
              if request.user.admin_level <= admin_lvl and request.user.user_type == 'admin':
                  return func(*args,**kwargs)
              else:
                  return render(request,'404.html',context={})
          return To_do
  return Wrapper


@method_decorator(user_is_admin(admin_lvl=3),name='dispatch')
class admin_page_index(ListView):
    def get(self,request):
        return render(request,'admin_page_index.html')

@method_decorator(user_is_admin(admin_lvl=1),name='dispatch')
class products_view_edit_delete(ListView):
    model = products
    template_name = 'admin_edit_delete_products.html'
    context_object_name = 'products'
    paginate_by = '4'
    ordering = ['-add_date']

@method_decorator(user_is_admin(admin_lvl=1),name='dispatch')
class edit_product(UpdateView):
    model = products
    template_name = 'admin_edit_product.html'
    fields =list( {'title':0,'price':0,'short_description':0,'main_description':0,'category':0,'brand':0,'is_active':0}.keys())
    def get_success_url(self):
        id=self.kwargs['pk']
        url=reverse('edit-product',args=id)
        request:HttpRequest=self.request
        photos_to_delete=list(request.POST.get('photos_to_delete').split(','))
        colors_to_change=request.POST.get('colors_to_change').split(',')
        colors_to_change.pop()
        for index in range(0,len(colors_to_change),2):
            obj=product_color_avalibity.objects.get(id=colors_to_change[index])
            obj.amount_left=colors_to_change[index+1]
            obj.save()
        if '' not in photos_to_delete:
         images.objects.filter(id__in=photos_to_delete).delete()
        for file in list(request._files.getlist('photos_to_add')):
            new_image=images(product_id=id,picture=file)
            new_image.save()
        return url
    def get_context_data(self, **kwargs):
        contex=super().get_context_data()
        contex['product']=products.objects.get(id=self.kwargs['pk'])
        contex['colors']=product_color_avalibity.objects.filter(product_id=self.kwargs['pk'])
        return contex




@method_decorator(user_is_admin(admin_lvl=1),name='dispatch')
class create_product(View):
    def post(self,request:HttpRequest):

        form=Product_edit_form(request.POST)
        print(request._files.getlist('pr_imgs_final'))
        if form.is_valid():
         obj=form.save()

         for img in list(request._files.getlist('pr_imgs_final')):
             image=images(picture=img,product=obj)
             image.save()
         return  redirect(reverse('create-product'))
        else:
            return redirect(reverse('create-product'))


    def get(self,request):
        new_form = Product_edit_form()

        return render(request, 'admin_create_product.html', context={'fields': new_form})
@method_decorator(user_is_admin(admin_lvl=1),name='dispatch')
class add_color_brand_category_ajax(View):
    def get(self,request):
        model=request.GET.get('model')
        title = request.GET.get('title')
        id=''
        print(title)
        if model == 'brand':
            brand = brands(title=title)
            brand.save()
            id=brand.id
        elif model == 'color':
            color = colors(color=title)
            color.save()
            id =color.id
        elif model == 'category':
            cat = product_category(title=title)
            cat.save()
            id = cat.id
        return JsonResponse({'id':id})

@method_decorator(user_is_admin(admin_lvl=1),name='dispatch')
class remove_cat_brand_color(View):
    def get(self,request):
        type=request.GET.get('type')
        if type == 'brand':
           br=brands.objects.filter(id=request.GET.get('id'))
           br.delete()
        elif type == 'category':
            cat =product_category.objects.filter(id=request.GET.get('id'))
            cat.delete()
        elif type == 'color':
            clr = colors.objects.filter(id=request.GET.get('id'))
            clr.delete()
        return HttpResponse('')

@method_decorator(user_is_admin(admin_lvl=1),name='dispatch')
class remove_prdocut(DeleteView):
    model=products
    success_url = reverse_lazy('admin-index-page')
    template_name = 'admin_page_index.html'
@method_decorator(user_is_admin(admin_lvl=2),name='dispatch')
class view_orders(ListView):
    model = order
    template_name = 'orders.html'
    context_object_name = 'orders'
    ordering = ['order_date']
    def get_queryset(self):
        status=self.kwargs['status']
        print(status)
        query=super().get_queryset().filter(is_paid=True,status=status).all()
        print(query)
        return query
    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        contex['status']=self.kwargs['status']
        return contex

@method_decorator(user_is_admin(admin_lvl=3),name='dispatch')
class show_comments(ListView):
    model = comments_module.models.comment
    template_name = 'comments.html'
    context_object_name = 'comments'
    paginate_by = '4'
    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        safe=mark_safe('<script type="text/javascript"> var a =`${{user}}`; alert(a);</script>')
        print(safe)
        contex.update({'cmnt':safe})
        return contex

@method_decorator(user_is_admin(admin_lvl=2),name='dispatch')
class confirm_reject_order(View):
    def get(self,request:HttpRequest,status):
     if status=='confirm':
         change_details=list(request.GET.get('change-details').split(','))
         delete_details=list(request.GET.get('delete-details').split(','))
         result=[]
         debt_value = request.GET.get('debtvalue')
         user_id = request.GET.get('userid')
         if ''  not in change_details or '' not in delete_details:
          if ''  not in change_details:
             for number in list(range(0, len(change_details), 2)):
                 index = number + 1
                 result.append([change_details[number], change_details[index]])
             details = order_detail.objects.filter(id__in=list([x[0] for x in result])).all()
             number = 0
             for y in details:
                 y.count = int(result[number][1])
                 y.save()
                 number += 1
          if '' not in delete_details:
             delete_details_list=order_detail.objects.filter(id__in=delete_details)
             for detail in delete_details_list:
                 detail.delete()
          new_debt = debts(user_id=user_id, amount=debt_value)
          new_debt.save()

         order_id = request.GET.get('orderid')
         order1=order.objects.filter(id=order_id).first()
         order1.status = 'confirmed'
         order1.save()
         message = request.GET.get('message')
         new_message=user_notifications(receiver_id=user_id,notif_message=message)
         new_message.save()
         print('confiremd')
     elif status=='reject':
         message=request.GET.get('message')
         user_id=request.GET.get('userid')
         order_number=request.GET.get('ordernumber')
         print('rejected')
         user_notifications.objects.create(receiver_id=user_id,notif_message=message).save()
         debts.objects.create(user_id=user_id,amount=request.GET.get('amount')).save()
         ord=order.objects.filter(order_number=order_number).first()

         ord.status='rejected'

         ord.save()
         print(ord.status)
     return HttpResponse('')

@method_decorator(user_is_admin(admin_lvl=1),name='dispatch')
class add_new_category_color_brand_new(CreateView):
    template_name='add_new_brand_color_category.html'
    fields='__all__'
    def get_success_url(self):
        success_url=reverse_lazy('add_brand_color_category_new',args=[self.kwargs['model_type']])
        return success_url
    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        contex['title']=self.model._meta.verbose_name
        contex['model_type']=self.kwargs['model_type']
        return contex

    def get(self,request,model_type):
        if model_type == 'category':
            self.model=product_category
        elif model_type == 'color':
            self.model=colors
        elif model_type =='brand':
            self.model=brands
        return super().get(request)

@method_decorator(user_is_admin(admin_lvl=1),name='dispatch')
class Create_New_Article(View):
    def get(self,request):
        form=Article_form(None)
        return render(request,'admin_add_new_article.html',context={'form':form})
    def post(self,request):
        form = Article_form(request.POST)
        if form.is_valid():
         obj=form.save()
         text:str=obj.text
         files=request._files.getlist('article_images')
         counter=0
         for file in files:
            picture=article_picture(parent_product_id=obj.product_id,picture=file)
            picture.save()
            text=text.replace(f'p{counter}',f'<br> <img src="{picture.picture.url}" style="height:150px;width:150px"><br>')
            counter+=1
         obj.text=text
         obj.save()
         return render(request,'admin_add_new_article.html',context={'form':Article_form(None)})
        else:
            return render(request, 'admin_add_new_article.html', context={'form': Article_form(None)})

@method_decorator(user_is_admin(admin_lvl=3),name='dispatch')
class show_tickets(ListView):
    model=user_ticket
    template_name = 'admin_user_tickets.html'
    paginate_by = 8
    ordering = '-creation_date'
    context_object_name = 'tickets'
    def get_queryset(self):
        query_set=super().get_queryset()
        return query_set

@method_decorator(user_is_admin(admin_lvl=3),name='dispatch')
class show_ticket_details(ListView):
    template_name = 'admin_user_ticket_details.html'
    model = ticket_message
    paginate_by = 10
    ordering = '-date'
    context_object_name = 'messages'
    def get_queryset(self):
        query_set=super().get_queryset()
        ticket_tile=self.kwargs['title']
        query_set=query_set.filter(parent_ticket__title=ticket_tile,parent_message_id=None).all()
        return query_set
    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        parent_tick=user_ticket.objects.get(title=self.kwargs['title'])
        contex['username']=parent_tick.created_by.username
        contex['ticket_id']=parent_tick.id
        return contex

@method_decorator(user_is_admin(admin_lvl=3),name='dispatch')
class answer_ticket(View):
    def post(self,request:HttpRequest):
        parent_ticket_id=request.POST.get('parent_ticket_id')
        parent_message_id=request.POST.get('parent_message_id')
        message=request.POST.get('message')
        title=user_ticket.objects.get(id=parent_ticket_id).title
        ticket_message.objects.create(parent_ticket_id=parent_ticket_id,parent_message_id=parent_message_id,message=message,is_answered=True).save()
        parent_mes=ticket_message.objects.get(id=parent_message_id)
        parent_mes.is_answered=True
        parent_mes.save()
        return redirect(reverse('show_ticket_detaails',kwargs={'title':title}))