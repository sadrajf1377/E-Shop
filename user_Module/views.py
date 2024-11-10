from math import ceil

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView, ListView, DetailView
from .models import normal_user,user_notifications,user_ticket,ticket_message
from utils.email_services import send_email
# Create your views here.
from product_module.models import products
from admin_module.models import debts

from .forms import ticket_form
from custom_decorators import login_required_api

@method_decorator(login_required,name='dispatch')
class edit_user_info(UpdateView):
    model =normal_user
    fields= ['first_name','last_name','phone_number','city','postal_code','address','avatar']
    template_name = 'edit_user_information.html'
    context_object_name = 'form'
    success_url = reverse_lazy('load_index_Page')
    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.request.user.id)

class ask_for_password_reset(View):
    def get(self,request):
        return render(request,'ask_for_password_reset.html',{'asked':False,'error':''})
    def post(self,request:HttpRequest):
        try:
         user=normal_user.objects.filter(email=request.POST.get('email')).first()
         code=get_random_string(72)
         user.reset_password_code=code
         user.save()
         sent_email=send_email(template_name= 'redirect_to_reste_password.html',to=request.POST.get('email'),subject='تغییر رمز عبور',contex={'reset_code':code})
         if sent_email:
             return render(request, 'ask_for_password_reset.html', {'asked': True})
         else:
             return render(request, 'ask_for_password_reset.html', {'asked': False,'error':'خطا در ارسال ایمیل'})
        except:
            return render(request, 'ask_for_password_reset.html', {'asked': False, 'error': 'ایمیل وارد شده صحیح نمی باشد'})




def change_password(request,reset_code):
    if request.method=="POST":

        error=''
        user=normal_user.objects.filter(reset_password_code__iexact=reset_code).first()


        new_pass=request.POST.get('password')
        new_pass_repeat=request.POST.get('password_repeat')

        if new_pass==new_pass_repeat and not user.check_password(new_pass):
            user.set_password(new_pass)
            user.user_status='normal'
            user.save()

            logout(request)
            return render(request, 'login_page.html')
        else:
            if new_pass!=new_pass_repeat:

                error='تکرار رمز عبور اشتباه است'
            elif new_pass==new_pass_repeat and user.check_password(new_pass):

                error = 'رمز عبور جدید نمی تواند با رمز قبلی یکسان باشد'
            return render(request,'reset_password_page.html',{'error':error,'reset_code_value':reset_code})

    elif request.method=="GET":
        return render(request,'reset_password_page.html',{'reset_code_value':reset_code,'error':''})



@method_decorator(login_required,name='dispatch')
class show_user_tickects(ListView):
    template_name = 'user_tickets.html'
    model = user_ticket
    context_object_name = 'tickets'
    paginate_by = 2
    ordering = '-creation_date'
    def get_queryset(self):
        used_id=self.request.user.id
        query_set=super().get_queryset().filter(created_by_id=used_id).all()
        print(query_set)
        return query_set

@method_decorator(login_required,name='dispatch')
class ticket_details(ListView):
    model=ticket_message
    template_name = 'ticket_details.html'
    context_object_name = 'messages'
    paginate_by = 6
    ordering = '-date'
    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        contex['ticket_title']=self.kwargs['title']
        return contex
    def get_queryset(self):
        query_set=super().get_queryset()
        user_id=self.request.user.id
        title=self.kwargs['title']
        query_set=query_set.filter(parent_ticket__title=title,parent_ticket__created_by_id=user_id,parent_message_id__isnull=True).all()
        return query_set


@method_decorator(login_required_api(),name='dispatch')
class new_ticket(View):
    def post(self,request):
        title=request.POST.get('ticket_title')
        if title =='' or title == None:
            return JsonResponse({'status':'fail','error_message':'عنوان تیکت نمی تواند خالی باشد'})

        user_id=request.user.id
        user_ticket.objects.create(title=title,created_by_id=user_id).save()
        return JsonResponse({'status':'success','url':reverse('my_tickets')})


@method_decorator(login_required_api,name='dispatch')
class create_new_ticket_message(View):
    def post(self,request:HttpRequest):

        message=request.POST.get('tkmessage')
        parent_ticket_title=request.POST.get('parent_ticket_title')
        print(message,parent_ticket_title)
        try:
          if message !='' or message != None:
            par_id=user_ticket.objects.get(title=parent_ticket_title,created_by_id=request.user.id).id
            ticket_message.objects.create(message=message,parent_ticket_id=par_id,parent_message_id=None).save()

            return JsonResponse({'status':'success'})
          else:
              print('dd')
              return JsonResponse({'status': 'fail','e_message':'بخش پیام نمی تواند خالی باشد'})
        except Exception as e:
            print(f'{e}')
            return JsonResponse({'status':'fail','e_message':'مشکلی در ارسال پیام به وجود آمد!لطفا دورباره تلاش کنید'})

@method_decorator(login_required_api,name='dispatch')
class show_user_notficitations(View):
    def get(self,request):
        page_number=request.GET.get('pagenumber')
        if page_number=='0':
            page_number = int(page_number)
        elif page_number=='1':
            page_number = int(page_number)+1
        else:
            page_number = int(page_number)+2
        pages_count=ceil(user_notifications.objects.filter(receiver_id=request.user.id).count()/2)
        objs=user_notifications.objects.filter(receiver_id=request.user.id).order_by('-notif_date')[page_number:page_number+2:1]
        result=[{'notif_message':x.notif_message,'notif_date':x.notif_date.date(),'notif_stat':x.is_read,'notif_id':x.id} for x in objs]
        page_numbers=list(range(0,pages_count,1))
        return JsonResponse({'result':result,'pages_count':pages_count,'page_numbers':page_numbers})


@method_decorator(login_required,name='dispatch')
class my_favourites(ListView):
    model = products
    template_name = 'user_favourite_products.html'
    context_object_name = 'products'
    def get_queryset(self):
        id=self.request.user.id
        user=normal_user.objects.get(id=id)
        query=super().get_queryset().filter(product_wish_list__users__in=[user])
        return query


@method_decorator(login_required,name='dispatch')
class my_debts(ListView):
    template_name = 'user_debts.html'
    model=debts
    context_object_name = 'debts'
    def get_queryset(self):
        query=super().get_queryset().filter(user_id=self.request.user.id).all()
        return query


@method_decorator(login_required_api,name='dispatch')
class mark_notif_as_read(View):
    def get(self,request):
        user_id=request.user.id
        notif_id=request.GET.get('notifid')
        print(user_id,notif_id)
        try:
         notif=user_notifications.objects.get(receiver_id=user_id,id=notif_id)
         notif.is_read=True
         notif.save()
         return JsonResponse({'status':'succeed'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'failed'})
