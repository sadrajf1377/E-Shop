from django.http import JsonResponse, HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse


def login_required_api(func):
    def wrapper(*args):
        is_authenticated=args[0].user.is_authenticated
        if is_authenticated:
            print('user is authenticated')
            return func(*args)
        else:
            print('user is not authenticated')
            return JsonResponse({'error':'برای دسترسی به این بخش ابتدا وارد شوید'},status=403)
    return wrapper


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