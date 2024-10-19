from django.contrib.auth import login, logout
from django.contrib.messages.storage import session
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View

import polls.templatetags.polls_extra
from .forms import register_form
from user_Module.models import normal_user
from utils.email_services import send_email
# Create your views here.
from user_Module.models import user_false_password_attemp

from django.utils import timezone
class register_user(View):
    def post(self,request:HttpRequest):
        rg_form=register_form(request.POST)
        if rg_form.is_valid():

            passwords_matches:bool=rg_form.cleaned_data.get('password')==rg_form.cleaned_data.get('password_repeat')
            email_exists:bool=normal_user.objects.filter(email__iexact=rg_form.cleaned_data.get('email')).first()

            activate_code = get_random_string(72)
            special_character=['!','@','#','%','^','_','-','&']
            password=rg_form.cleaned_data.get('password')
            password_is_strong=passwords_matches and any(x.isupper() for x in password) and any(x in special_character for x in password)
            email_valid= send_email(template_name='activate_account.html',to=rg_form.cleaned_data.get('email'),subject='فعال سازی اکانت',contex={'code':activate_code}) ==1
            if passwords_matches and not email_exists and email_valid and password_is_strong:

                new_user:normal_user=normal_user(email=rg_form.cleaned_data.get('email'),activation_code=activate_code
                                                 ,username=rg_form.cleaned_data.get('email'),is_active=False)

                new_user.set_password(rg_form.cleaned_data.get('password'))
                new_user.save()
                return render(request,'register_done.html')
            else:
                if not passwords_matches:
                 rg_form.add_error('password_repeat','تکرار پسوورد اشتباه است')
                if email_exists:
                 rg_form.add_error('email', 'این ایمیل قبلا ثبت شده است')
                if not email_valid:
                 rg_form.add_error('email', 'ایمیل وارد شده معتبر نمی باشد')
                if not password_is_strong:
                 rg_form.add_error('password', 'رمز باید شامل یک حرف بزرگ و یک کاراکتر خاص مثل @،#،- ویا _ باشد')
                return render(request, 'register_page.html', {'register_form':rg_form})
        else:
            return self.get(request)

    def get(self,request:HttpRequest):
        contex={'register_form':register_form(None)}

        return render(request, 'register_page.html', contex)

def activate_user(request,activate_code):
    user_custom=normal_user.objects.all().get(activation_code=activate_code)
    user_custom.is_active=True
    user_custom.save()
    print(user_custom.get_full_name())
    return HttpResponse("اکانت شما با موفقیت فعال شد")


class login_user(View):
    def post(self,request:HttpRequest):
        email_or_username=request.POST.get('email_username')
        email_check = normal_user.objects.all().filter(Q(username=email_or_username)|Q(email=email_or_username)).first()
        if email_check:
            user_is_fine=email_check.user_status!='partially_banned'
            if user_is_fine:
             email_check.delete_out_dated_attemps()
             check_password=email_check.check_password(request.POST.get('password'))
             if check_password:
                email_check.delete_all_false_attemps()
                login(request,email_check)
                return redirect(reverse('load_index_Page'))
             else:
                new_attemp = user_false_password_attemp(user=email_check)
                new_attemp.save()
                if email_check.user_false_password_attemp_set.all().count() >= 15:
                    return ban_user(email_check)
                else:
                    contex = {'error': 'ایمیل یا کلمه عبور اشتباه است!'}
                    return render(request, 'login_page.html', contex)
            else:
                return HttpResponse('اکانت شما به طور موقت مسدود شده است،برای تغییر پسوورد خود به ایمیل خود مراجعه نمایید')

        else:
            contex = {'error': 'ایمیل یا کلمه عبور اشتباه است!'}
            return render(request, 'login_page.html', contex)
    def get(self,request:HttpRequest):
        return render(request,'login_page.html')
def ban_user(user):
    user.user_status = 'partially_banned'
    reset_code = get_random_string(72)
    user.reset_password_code = reset_code
    user.save()
    send_email(template_name='redirect_to_reste_password.html', to=user.email, subject='تغییر رمز عبور',
               contex={'reset_code': reset_code})
    return HttpResponse('اکانت شما به طور موقت مسدود شده است،برای تغییر پسوورد خود به ایمیل خود مراجعه نمایید')

def logout_user(request):
    logout(request)
    polls.templatetags.polls_extra.current_user = None
    return redirect(reverse('load_index_Page'))