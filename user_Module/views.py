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
from .models import normal_user
from register_login.tasks import send_email_to_user
# Create your views here.
from product_module.models import products
from admin_module.models import debts


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
    def get(self,request):
        return super().get(request)


def change_preferred_language(request,language):
    if request.method =='GET':
        if language=='fa' or language == 'en':
            request.session.update({'language':language})
            print(request.session)
            return redirect(reverse('load_index_Page'))


class ask_for_password_reset(View):
    def get(self,request):
        return render(request,'ask_for_password_reset.html',{'asked':False,'error':''})
    def post(self,request:HttpRequest):
        try:
         user=normal_user.objects.filter(email=request.POST.get('email')).first()
         code=get_random_string(72)
         user.reset_password_code=code
         user.save()
         sent_email=send_email_to_user.delay(template_name= 'redirect_to_reste_password.html',to=request.POST.get('email'),subject='تغییر رمز عبور',contex={'reset_code':code})
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



