from django.contrib.auth import login, logout
from django.contrib.messages.storage import session
from django.db import transaction
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View

import polls.templatetags.polls_extra
from .forms import register_form,login_form
from user_Module.models import normal_user
from .tasks import send_email_to_user
# Create your views here.
from user_Module.models import user_false_password_attemp

from django.utils import timezone
class register_user(View):
    def post(self,request:HttpRequest):
        rg_form=register_form(request.POST)
        if rg_form.is_valid():
            try:
                with transaction.atomic():
                    act_code=get_random_string(length=16)
                    user:normal_user=rg_form.instance
                    user.activation_code=act_code
                    user.set_password(rg_form.cleaned_data.get('password'))
                    user.save()
                    send_email_to_user.delay(template_name='activate_account.html',subject='فعالسازی حساب کاربری',to=user.email,context={'code':act_code})
                    return render(request,'register_done.html',status=201)
            except Exception as e:
                rg_form.add_error('password_repeat','مشکلی در ثبت نام شما به وجود آمد!لطفا مجدد تلاش بفرمایید')
                return render(request, 'register_page.html', {'register_form':rg_form},status=500)

        else:
            return render(request, 'register_page.html', {'register_form':rg_form},status=401)

    def get(self,request:HttpRequest):
        contex={'register_form':register_form(None)}

        return render(request, 'register_page.html', contex,status=200)

def activate_user(request,activate_code):
    user_custom=normal_user.objects.all().get(activation_code=activate_code)
    user_custom.is_active=True
    user_custom.save()
    print(user_custom.get_full_name())
    return HttpResponse("اکانت شما با موفقیت فعال شد")


class login_user(View):
    def post(self,request:HttpRequest):
        frm=login_form(request.POST)
        if frm.is_valid():
            try:
                username_email=frm.cleaned_data.get('username_email')
                user=normal_user.objects.get(Q(username=username_email)|Q(email=username_email))
                password=frm.cleaned_data.get('password')
                if user.user_status!='partially_banned':
                    if user.check_password(password):
                        user.delete_all_false_attemps()
                        login(request, user)
                        return redirect(reverse('load_index_Page'))
                    else:
                        new_attemp = user_false_password_attemp(user=user)
                        new_attemp.save()
                        if user.user_false_password_attemp_set.all().count() >= 15:
                            return ban_user(user)

                        frm.add_error('password', 'کاربری با این مشخصات پیدا نشد')
                        return render(request, 'login_page.html', context={'login_form': frm}, status=404)
                else:

                    frm.add_error('password','اکانت شما به طور موقت مسدود شده است،برای تغییر پسوورد خود به ایمیل خود مراجعه نمایید')
                    return render(request, 'login_page.html', context={'login_form': frm}, status=400)


            except Exception as e:
                if isinstance(e,normal_user.DoesNotExist):
                    frm.add_error('password','کاربری با این مشخصات پیدا نشد')
                    return render(request,'login_page.html',context={'login_form':frm},status=404)
                else:
                    frm.add_error('password','مشکلی در احراز هویت شما به وجود آمد!لطفا مجدد تلاش بفرمایید')
                    return render(request, 'login_page.html', context={'login_form': frm}, status=500)
        else:
            return render(request, 'login_page.html', context={'login_form': frm}, status=401)
    def get(self,request:HttpRequest):
        frm=login_form()
        return render(request,'login_page.html',context={'login_form':frm},status=200)
def ban_user(user):
    user.user_status = 'partially_banned'
    reset_code = get_random_string(72)
    user.reset_password_code = reset_code
    user.save()
    send_email_to_user.delay(template_name='redirect_to_reste_password.html', to=user.email, subject='تغییر رمز عبور',
               contex={'reset_code': reset_code})
    return HttpResponse('اکانت شما به طور موقت مسدود شده است،برای تغییر پسوورد خود به ایمیل خود مراجعه نمایید')

def logout_user(request):
    logout(request)
    polls.templatetags.polls_extra.current_user = None
    return redirect(reverse('load_index_Page'))