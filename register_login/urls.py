from django.urls import path
from .views import register_user,activate_user,login_user,logout_user
urlpatterns=[path('login_page',register_user.as_view(),name='register_user')
             ,path('activate_user/<activate_code>',activate_user,name='activate_User')
             ,path('login_user',login_user.as_view(),name='login-user')
             ,path('logut_user',logout_user,name='logout_user')]